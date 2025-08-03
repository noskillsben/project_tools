#!/usr/bin/env python3
"""
CLI Documentation Verification Script

This script systematically verifies that CLI commands documented in README files
match the actual implementation in the codebase. It generates detailed reports
of mismatches and verifies entry points and web GUI startup commands.

Configuration Support:
The script supports configuration files in JSON, YAML, or TOML formats to customize
its behavior for different projects. Use the --config parameter to specify a 
configuration file.

Configuration Structure:
- files: Paths to various files (README files, CLI implementation, setup files)
- commands: Command names and modules to test
- extraction: How to extract commands from documentation
- output: Output formatting options
- testing: Testing behavior and timeouts

Examples:
    python verify_cli_docs.py --config myproject.json
    python verify_cli_docs.py --config config.yaml --verbose
    python verify_cli_docs.py --project-root /path/to/project --no-color
"""

import argparse
import ast
import re
import sys
import subprocess
import importlib.util
import logging
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import json
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
try:
    import tomllib
    HAS_TOML = True
except ImportError:
    try:
        import tomli as tomllib
        HAS_TOML = True
    except ImportError:
        HAS_TOML = False


class VerifierConfig:
    """Configuration class for CLI doc verifier."""
    
    DEFAULT_CONFIG = {
        "files": {
            "readme_files": ["README.md", "WEB_GUI_README.md"],
            "cli_file": "project_tools/cli.py",
            "setup_files": ["setup.py", "pyproject.toml"],
            "web_gui_file": "start_web_gui.py"
        },
        "commands": {
            "cli_command_name": "project-tools",
            "web_gui_module": "project_tools.web_gui.app",
            "entry_points_to_test": ["project-tools", "project-tools-web"]
        },
        "extraction": {
            "code_block_languages": ["bash", "shell"],
            "inline_command_patterns": [],
            "ignore_command_patterns": []
        },
        "output": {
            "use_colors": None,
            "verbose_logging": False,
            "report_sections": ["summary", "entry_points", "web_gui", "missing", "undocumented", "detailed"]
        },
        "testing": {
            "test_timeout": 10,
            "test_web_gui": True,
            "test_entry_points": True
        }
    }
    
    def __init__(self, config_dict: Dict = None):
        """Initialize configuration with defaults and overrides."""
        self.config = self.DEFAULT_CONFIG.copy()
        if config_dict:
            self._merge_config(self.config, config_dict)
    
    def _merge_config(self, base: Dict, override: Dict) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, path: str, default=None):
        """Get configuration value using dot notation (e.g., 'files.readme_files')."""
        keys = path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    @classmethod
    def load_from_file(cls, config_path: Path) -> 'VerifierConfig':
        """Load configuration from file (JSON, YAML, or TOML)."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        content = config_path.read_text()
        suffix = config_path.suffix.lower()
        
        try:
            if suffix == '.json':
                config_dict = json.loads(content)
            elif suffix in ['.yaml', '.yml'] and HAS_YAML:
                config_dict = yaml.safe_load(content)
            elif suffix == '.toml' and HAS_TOML:
                config_dict = tomllib.loads(content)
            else:
                raise ValueError(f"Unsupported configuration format: {suffix}")
            
            return cls(config_dict)
        except Exception as e:
            raise ValueError(f"Failed to parse configuration file {config_path}: {e}")


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports color output."""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


class CLIDocVerifier:
    def __init__(self, project_root: Path, config: VerifierConfig = None, verbose: bool = False, use_colors: bool = None):
        self.project_root = project_root
        self.config = config or VerifierConfig()
        self.documented_commands = {}
        self.implemented_commands = {}
        self.web_gui_commands = []
        self.entry_points = {}
        self.verbose = verbose or self.config.get('output.verbose_logging', False)
        self.use_colors = use_colors if use_colors is not None else (
            self.config.get('output.use_colors') if self.config.get('output.use_colors') is not None 
            else Colors.supports_color()
        )
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging with appropriate levels."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(levelname)s: %(message)s' if not self.verbose 
            else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        return logger
        
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_colors:
            return f"{color}{text}{Colors.END}"
        return text
        
    def extract_documented_commands(self) -> Dict[str, List[str]]:
        """Extract all documented CLI commands from README files."""
        self.logger.info("📖 Extracting documented commands from README files...")
        readme_files = self.config.get('files.readme_files', ["README.md", "WEB_GUI_README.md"])
        documented = {}
        
        for readme_file in readme_files:
            documented[readme_file] = []
            readme_path = self.project_root / readme_file
            
            if readme_path.exists():
                self.logger.debug(f"Processing {readme_path}")
                content = readme_path.read_text()
                documented[readme_file] = self._extract_cli_commands_from_text(content)
                
                # Extract web GUI commands if this is a web GUI README
                if "web" in readme_file.lower():
                    self.web_gui_commands = self._extract_web_gui_commands(content)
                
                self.logger.info(self._colorize(f"✅ Found {len(documented[readme_file])} commands in {readme_file}", Colors.GREEN))
            else:
                self.logger.warning(self._colorize(f"{readme_file} not found at {readme_path}", Colors.YELLOW))
            
        self.documented_commands = documented
        return documented
        
    def _extract_cli_commands_from_text(self, text: str) -> List[str]:
        """Extract CLI commands from markdown text."""
        commands = []
        cli_command_name = self.config.get('commands.cli_command_name', 'project-tools')
        code_block_languages = self.config.get('extraction.code_block_languages', ['bash', 'shell'])
        ignore_patterns = self.config.get('extraction.ignore_command_patterns', [])
        
        # Build pattern for code blocks
        lang_pattern = '|'.join(code_block_languages) if code_block_languages else ''
        code_block_pattern = f'```(?:{lang_pattern})?\n(.*?)\n```'
        code_blocks = re.findall(code_block_pattern, text, re.DOTALL)
        
        for block in code_blocks:
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith(cli_command_name):
                    # Check if this command should be ignored
                    should_ignore = any(re.search(pattern, line) for pattern in ignore_patterns)
                    if not should_ignore:
                        commands.append(line)
                    
        # Also find inline code commands
        inline_pattern = f'`({cli_command_name}[^`]+)`'
        inline_commands = re.findall(inline_pattern, text)
        for cmd in inline_commands:
            should_ignore = any(re.search(pattern, cmd) for pattern in ignore_patterns)
            if not should_ignore:
                commands.append(cmd)
        
        return commands
        
    def _extract_web_gui_commands(self, text: str) -> List[str]:
        """Extract web GUI startup commands from text."""
        commands = []
        web_gui_file = self.config.get('files.web_gui_file', 'start_web_gui.py')
        web_gui_module = self.config.get('commands.web_gui_module', 'project_tools.web_gui.app')
        
        # Find python start_web_gui.py commands
        gui_file_name = Path(web_gui_file).name
        python_pattern = f'`(python[^`]*{re.escape(gui_file_name)}[^`]*)`'
        python_commands = re.findall(python_pattern, text)
        commands.extend(python_commands)
        
        # Find python -m module commands
        module_pattern = f'`(python[^`]*-m {re.escape(web_gui_module)}[^`]*)`'
        module_commands = re.findall(module_pattern, text)
        commands.extend(module_commands)
        
        return commands
        
    def analyze_cli_implementation(self) -> Dict[str, any]:
        """Analyze the actual CLI implementation from cli.py."""
        self.logger.info("🔍 Analyzing CLI implementation...")
        cli_file = self.config.get('files.cli_file', 'project_tools/cli.py')
        cli_path = self.project_root / cli_file
        
        if not cli_path.exists():
            self.logger.error(self._colorize(f"CLI implementation not found at {cli_path}", Colors.RED))
            return {"error": f"CLI implementation not found at {cli_path}"}
            
        try:
            self.logger.debug(f"Parsing {cli_path}")
            with open(cli_path, 'r') as f:
                content = f.read()
                
            tree = ast.parse(content)
            commands = self._extract_argparse_commands(tree, content)
            self.implemented_commands = commands
            
            subcommand_count = len(commands.get("subparsers", {}))
            self.logger.info(self._colorize(f"✅ Found {subcommand_count} implemented subcommands", Colors.GREEN))
            return commands
            
        except Exception as e:
            self.logger.error(self._colorize(f"Failed to parse CLI implementation: {e}", Colors.RED))
            return {"error": f"Failed to parse CLI implementation: {e}"}
            
    def _extract_argparse_commands(self, tree: ast.AST, content: str) -> Dict[str, any]:
        """Extract commands from argparse structure."""
        commands = {"main_parser": [], "subparsers": {}}
        
        # Look for ArgumentParser creation and add_argument calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr == 'add_argument':
                    # Extract argument details
                    args = []
                    for arg in node.args:
                        if isinstance(arg, ast.Constant):
                            args.append(arg.value)
                    if args:
                        commands["main_parser"].append(args[0])
                        
                elif hasattr(node.func, 'attr') and node.func.attr == 'add_subparsers':
                    # Found subparsers
                    pass
                    
        # Also use regex to find subparser definitions
        subparser_pattern = r'(\w+)_parser = subparsers\.add_parser\([\'"](\w+)[\'"]'
        subparser_matches = re.findall(subparser_pattern, content)
        
        for var_name, command_name in subparser_matches:
            commands["subparsers"][command_name] = []
            
            # Find arguments for this subparser
            arg_pattern = f'{var_name}\.add_argument\([\'"]([^\'\"]+)[\'"]'
            arg_matches = re.findall(arg_pattern, content)
            commands["subparsers"][command_name] = arg_matches
            
        return commands
        
    def verify_entry_points(self) -> Dict[str, any]:
        """Verify that entry points are properly configured."""
        self.logger.info("🔗 Verifying entry points configuration...")
        results = {}
        setup_files = self.config.get('files.setup_files', ['setup.py', 'pyproject.toml'])
        
        for setup_file in setup_files:
            setup_path = self.project_root / setup_file
            if setup_path.exists():
                self.logger.debug(f"Checking {setup_file} at {setup_path}")
                content = setup_path.read_text()
                
                if setup_file == 'setup.py':
                    results[setup_file] = self._extract_entry_points_from_setup(content)
                elif setup_file == 'pyproject.toml':
                    results[setup_file] = self._extract_entry_points_from_toml(content)
                
                self.logger.info(self._colorize(f"✅ Found {len(results[setup_file])} entry points in {setup_file}", Colors.GREEN))
            else:
                self.logger.debug(f"{setup_file} not found")
            
        # Test actual entry points if enabled
        if self.config.get('testing.test_entry_points', True):
            self.logger.info("🧪 Testing entry points...")
            results["entry_point_tests"] = self._test_entry_points()
        
        self.entry_points = results
        return results
        
    def _extract_entry_points_from_setup(self, content: str) -> Dict[str, str]:
        """Extract entry points from setup.py."""
        entry_points = {}
        
        # Look for console_scripts in entry_points
        console_scripts_pattern = r'[\'"]console_scripts[\'"]:\s*\[(.*?)\]'
        match = re.search(console_scripts_pattern, content, re.DOTALL)
        
        if match:
            scripts_content = match.group(1)
            script_pattern = r'[\'"]([^=]+)=([^\'\"]+)[\'"]'
            scripts = re.findall(script_pattern, scripts_content)
            for name, target in scripts:
                entry_points[name.strip()] = target.strip()
                
        return entry_points
        
    def _extract_entry_points_from_toml(self, content: str) -> Dict[str, str]:
        """Extract entry points from pyproject.toml."""
        entry_points = {}
        
        # Look for [project.scripts] section
        scripts_pattern = r'\[project\.scripts\](.*?)(?=\[|\Z)'
        match = re.search(scripts_pattern, content, re.DOTALL)
        
        if match:
            scripts_content = match.group(1)
            script_pattern = r'([^=\s]+)\s*=\s*[\'"]([^\'\"]+)[\'"]'
            scripts = re.findall(script_pattern, scripts_content)
            for name, target in scripts:
                entry_points[name.strip()] = target.strip()
                
        return entry_points
        
    def _test_entry_points(self) -> Dict[str, any]:
        """Test that entry points actually work."""
        results = {}
        entry_points_to_test = self.config.get('commands.entry_points_to_test', ["project-tools", "project-tools-web"])
        timeout = self.config.get('testing.test_timeout', 10)
        
        for entry_point in entry_points_to_test:
            try:
                result = subprocess.run(
                    [entry_point, "--help"],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                results[entry_point] = {
                    "success": result.returncode == 0,
                    "stdout": result.stdout[:500],
                    "stderr": result.stderr[:500]
                }
            except subprocess.TimeoutExpired:
                results[entry_point] = {"success": False, "error": "Timeout"}
            except FileNotFoundError:
                results[entry_point] = {"success": False, "error": "Command not found"}
            except Exception as e:
                results[entry_point] = {"success": False, "error": str(e)}
                
        return results
        
    def test_web_gui_commands(self) -> Dict[str, any]:
        """Test web GUI startup commands."""
        if not self.config.get('testing.test_web_gui', True):
            return {}
            
        self.logger.info("🌐 Testing web GUI startup commands...")
        results = {}
        timeout = self.config.get('testing.test_timeout', 10)
        web_gui_file = self.config.get('files.web_gui_file', 'start_web_gui.py')
        web_gui_module = self.config.get('commands.web_gui_module', 'project_tools.web_gui.app')
        
        # Test python start_web_gui.py --help
        start_gui_path = self.project_root / web_gui_file
        if start_gui_path.exists():
            self.logger.debug("Testing start_web_gui.py --help")
            try:
                result = subprocess.run(
                    ["python", str(start_gui_path), "--help"],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=self.project_root
                )
                success = result.returncode == 0
                results["start_web_gui.py"] = {
                    "success": success,
                    "stdout": result.stdout[:500],
                    "stderr": result.stderr[:500]
                }
                status = self._colorize("✅", Colors.GREEN) if success else self._colorize("❌", Colors.RED)
                self.logger.info(f"{status} start_web_gui.py test")
            except Exception as e:
                results["start_web_gui.py"] = {"success": False, "error": str(e)}
                self.logger.error(self._colorize(f"❌ start_web_gui.py test failed: {e}", Colors.RED))
        else:
            results["start_web_gui.py"] = {"success": False, "error": "File not found"}
            self.logger.warning(self._colorize("❌ start_web_gui.py not found", Colors.YELLOW))
            
        # Test python -m module --help
        self.logger.debug("Testing web_gui module --help")
        try:
            result = subprocess.run(
                ["python", "-m", web_gui_module, "--help"],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_root
            )
            success = result.returncode == 0
            results["web_gui_module"] = {
                "success": success,
                "stdout": result.stdout[:500],
                "stderr": result.stderr[:500]
            }
            status = self._colorize("✅", Colors.GREEN) if success else self._colorize("❌", Colors.RED)
            self.logger.info(f"{status} web_gui module test")
        except Exception as e:
            results["web_gui_module"] = {"success": False, "error": str(e)}
            self.logger.error(self._colorize(f"❌ web_gui module test failed: {e}", Colors.RED))
            
        return results
        
    def cross_reference_commands(self) -> Dict[str, any]:
        """Cross-reference documented vs implemented commands."""
        # Flatten documented commands
        all_documented = []
        for source, commands in self.documented_commands.items():
            all_documented.extend(commands)
            
        # Parse documented commands into structured format
        cli_command_name = self.config.get('commands.cli_command_name', 'project-tools')
        documented_parsed = []
        for cmd in all_documented:
            parts = cmd.split()
            if len(parts) >= 2 and parts[0] == cli_command_name:
                documented_parsed.append({
                    "full_command": cmd,
                    "base_command": parts[1] if len(parts) > 1 else "",
                    "subcommand": parts[2] if len(parts) > 2 else "",
                    "args": parts[3:] if len(parts) > 3 else []
                })
                
        # Get implemented subcommands
        implemented_subcommands = list(self.implemented_commands.get("subparsers", {}).keys())
        
        # Find mismatches
        documented_subcommands = set()
        for cmd in documented_parsed:
            if cmd["base_command"]:
                documented_subcommands.add(cmd["base_command"])
                
        missing_commands = documented_subcommands - set(implemented_subcommands)
        undocumented_commands = set(implemented_subcommands) - documented_subcommands
        
        return {
            "documented_commands": documented_parsed,
            "implemented_subcommands": implemented_subcommands,
            "missing_commands": list(missing_commands),
            "undocumented_commands": list(undocumented_commands)
        }
        
    def generate_report(self) -> str:
        """Generate a comprehensive verification report."""
        cross_ref = self.cross_reference_commands()
        web_gui_test = self.test_web_gui_commands()
        
        report = []
        report.append("# CLI Documentation Verification Report")
        report.append("=" * 50)
        report.append("")
        
        # Summary statistics
        report.append("## Summary")
        report.append(f"- Documented commands: {len(cross_ref['documented_commands'])}")
        report.append(f"- Implemented subcommands: {len(cross_ref['implemented_subcommands'])}")
        report.append(f"- Missing commands: {len(cross_ref['missing_commands'])}")
        report.append(f"- Undocumented commands: {len(cross_ref['undocumented_commands'])}")
        report.append("")
        
        # Entry points verification
        report.append("## Entry Points Verification")
        for source, entry_points in self.entry_points.items():
            if source == "entry_point_tests":
                for ep, result in entry_points.items():
                    status = "✅ PASS" if result.get("success") else "❌ FAIL"
                    report.append(f"- {ep}: {status}")
                    if not result.get("success"):
                        report.append(f"  Error: {result.get('error', 'Unknown error')}")
            else:
                report.append(f"### {source}")
                for name, target in entry_points.items():
                    report.append(f"- {name} = {target}")
        report.append("")
        
        # Web GUI commands verification
        report.append("## Web GUI Commands Verification")
        for cmd, result in web_gui_test.items():
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            report.append(f"- {cmd}: {status}")
            if not result.get("success"):
                report.append(f"  Error: {result.get('error', 'Unknown error')}")
        report.append("")
        
        # Missing commands
        if cross_ref['missing_commands']:
            report.append("## Missing Commands (Documented but not Implemented)")
            for cmd in cross_ref['missing_commands']:
                report.append(f"- project-tools {cmd}")
        report.append("")
        
        # Undocumented commands
        if cross_ref['undocumented_commands']:
            report.append("## Undocumented Commands (Implemented but not Documented)")
            for cmd in cross_ref['undocumented_commands']:
                report.append(f"- project-tools {cmd}")
        report.append("")
        
        # Detailed command analysis
        report.append("## Detailed Command Analysis")
        report.append("### Documented Commands:")
        for cmd in cross_ref['documented_commands']:
            report.append(f"- {cmd['full_command']}")
        report.append("")
        
        report.append("### Implemented Subcommands:")
        for cmd in cross_ref['implemented_subcommands']:
            args = self.implemented_commands.get("subparsers", {}).get(cmd, [])
            report.append(f"- {cmd}: {', '.join(args) if args else 'no arguments'}")
        
        return "\n".join(report)
        
    def run_verification(self) -> str:
        """Run complete verification and return report."""
        start_time = time.time()
        
        phase_start = time.time()
        self.extract_documented_commands()
        self.logger.debug(f"Documentation extraction completed in {time.time() - phase_start:.2f}s")
        
        phase_start = time.time()
        self.analyze_cli_implementation()
        self.logger.debug(f"CLI analysis completed in {time.time() - phase_start:.2f}s")
        
        phase_start = time.time()
        self.verify_entry_points()
        self.logger.debug(f"Entry point verification completed in {time.time() - phase_start:.2f}s")
        
        phase_start = time.time()
        self.logger.info("📋 Generating verification report...")
        report = self.generate_report()
        self.logger.debug(f"Report generation completed in {time.time() - phase_start:.2f}s")
        
        total_time = time.time() - start_time
        self.logger.info(self._colorize(f"🎉 Verification completed in {total_time:.2f}s", Colors.BOLD))
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Verify CLI documentation matches implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Configuration file support:
  The tool supports JSON, YAML, and TOML configuration files.
  Use --config to specify a configuration file path.
  
  Example configuration (JSON):
  {
    "files": {
      "readme_files": ["README.md", "docs/CLI.md"],
      "cli_file": "src/cli.py"
    },
    "commands": {
      "cli_command_name": "my-tool"
    }
  }
        """
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (JSON, YAML, or TOML)"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Path to project root directory"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for report (default: stdout)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging with timestamps"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output (only show errors)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = None
    if args.config:
        try:
            config = VerifierConfig.load_from_file(args.config)
            print(f"Loaded configuration from {args.config}")
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        config = VerifierConfig()
    
    # Handle quiet mode by adjusting logging
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    verifier = CLIDocVerifier(
        args.project_root,
        config=config,
        verbose=args.verbose, 
        use_colors=not args.no_color
    )
    
    if args.json:
        # Output raw data as JSON
        data = {
            "documented_commands": verifier.extract_documented_commands(),
            "implemented_commands": verifier.analyze_cli_implementation(),
            "entry_points": verifier.verify_entry_points(),
            "web_gui_tests": verifier.test_web_gui_commands(),
            "cross_reference": verifier.cross_reference_commands()
        }
        output = json.dumps(data, indent=2, default=str)
    else:
        # Generate human-readable report
        output = verifier.run_verification()
    
    if args.output:
        args.output.write_text(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()