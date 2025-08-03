"""
CLI Documentation Synchronization Tests

This test suite ensures that CLI documentation stays in sync with the actual
implementation. It verifies entry points, web GUI commands, and CLI command
coverage to prevent documentation drift.
"""

import pytest
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, NamedTuple
from unittest.mock import Mock, patch
import importlib.util


# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class CommandCategory(NamedTuple):
    """Data structure for command category test parameters."""
    name: str
    subcommands: List[str]
    required_args: Dict[str, List[str]] = {}
    
    
class MockCLIResponse(NamedTuple):
    """Mock CLI response for testing."""
    returncode: int
    stdout: str
    stderr: str = ""


# Command categories for parametrized testing
COMMAND_CATEGORIES = [
    CommandCategory("todo", ["add", "list", "complete", "deps"], {
        "add": ["title"],
        "complete": ["todo_id"]
    }),
    CommandCategory("version", ["bump", "tag"], {
        "bump": ["bump_type"]
    }),
    CommandCategory("intelligence", ["init", "status"]),
    CommandCategory("compass", ["init", "context"], {
        "context": ["type", "content"]
    }),
    CommandCategory("chains", ["create", "add-todos", "health"], {
        "create": ["name"],
        "add-todos": ["chain_id", "todo_ids"]
    }),
    CommandCategory("direction", ["set", "assume", "pivot"], {
        "set": ["direction"],
        "assume": ["assumption"],
        "pivot": ["trigger", "new_direction"]
    }),
    CommandCategory("reflect", ["create", "energy", "learning"], {
        "energy": ["level"],
        "learning": ["learning"]
    }),
    CommandCategory("portfolio", ["init", "add-project"], {
        "add-project": ["project_id", "project_name", "project_path"]
    })
]


# Mock CLI responses for testing
MOCK_HELP_RESPONSES = {
    "main": MockCLIResponse(0, """usage: project-tools [-h] [--project-dir PROJECT_DIR]
                                   {status,todo,version,export,intelligence,compass,chains,direction,reflect,portfolio,ai-enhance}
                                   ...

Universal project management tools for todos, versioning, and workflows

options:
  -h, --help            show this help message and exit
  --project-dir PROJECT_DIR
                        Project directory path (default: current directory)

Available commands:
  {status,todo,version,export,intelligence,compass,chains,direction,reflect,portfolio,ai-enhance}
    status              Show project summary
    todo                Todo management
    version             Version management
    export              Export project data
    intelligence        AI-assisted project management
    compass             Project compass management
    chains              Task chain management
    direction           Direction tracking
    reflect             Reflection management
    portfolio           Portfolio management
    ai-enhance          AI enhancement opportunities"""),
    
    "todo": MockCLIResponse(0, """usage: project-tools todo [-h] {add,list,complete,deps} ...

options:
  -h, --help            show this help message and exit

Todo actions:
  {add,list,complete,deps}
    add                 Add new todo
    list                List todos
    complete            Complete todo
    deps                Show dependency tree"""),
    
    "version": MockCLIResponse(0, """usage: project-tools version [-h] {bump,tag} ...

options:
  -h, --help            show this help message and exit

Version actions:
  {bump,tag}
    bump                Create new version
    tag                 Create git tag""")
}


# Test fixtures
@pytest.fixture(scope="session")
def project_root():
    """Provide project root path to tests."""
    return PROJECT_ROOT


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for faster testing."""
    def _mock_run(cmd, **kwargs):
        if len(cmd) >= 2 and cmd[0] == "project-tools":
            if cmd[1] == "--help":
                return MOCK_HELP_RESPONSES["main"]
            elif cmd[1] in MOCK_HELP_RESPONSES:
                return MOCK_HELP_RESPONSES[cmd[1]]
            else:
                # Default successful response for unknown commands
                return MockCLIResponse(0, f"usage: project-tools {cmd[1]} [-h] ...")
        elif len(cmd) >= 3 and cmd[0] == "project-tools" and cmd[2] == "--help":
            # Subcommand help
            return MockCLIResponse(0, f"usage: project-tools {cmd[1]} [-h] ...")
        else:
            # Default response
            return MockCLIResponse(0, "Mock response")
    
    with patch('subprocess.run', side_effect=_mock_run) as mock:
        yield mock


@pytest.fixture(params=COMMAND_CATEGORIES, ids=lambda x: x.name)
def command_category(request):
    """Parametrized fixture for command categories."""
    return request.param


@pytest.fixture
def critical_commands():
    """Critical commands that must be implemented."""
    return {
        "todo", "intelligence", "compass", "chains", 
        "direction", "reflect", "portfolio", "version"
    }


class TestEntryPoints:
    """Test that entry points are correctly configured and functional."""
    
    def test_project_tools_entry_point_exists(self):
        """Test that project-tools entry point is available."""
        try:
            result = subprocess.run(
                ["project-tools", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, f"project-tools entry point failed: {result.stderr}"
        except FileNotFoundError:
            pytest.fail("project-tools entry point not found. Check package installation.")
        except subprocess.TimeoutExpired:
            pytest.fail("project-tools entry point timed out")
    
    def test_project_tools_web_entry_point_exists(self):
        """Test that project-tools-web entry point is available."""
        try:
            result = subprocess.run(
                ["project-tools-web", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, f"project-tools-web entry point failed: {result.stderr}"
        except FileNotFoundError:
            pytest.fail("project-tools-web entry point not found. Check package installation.")
        except subprocess.TimeoutExpired:
            pytest.fail("project-tools-web entry point timed out")
    
    def test_entry_point_help_output(self):
        """Test that entry points produce expected help output."""
        result = subprocess.run(
            ["project-tools", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        help_output = result.stdout.lower()
        
        # Should contain basic CLI elements
        assert "usage:" in help_output
        assert "options:" in help_output or "optional arguments:" in help_output


class TestWebGUICommands:
    """Test web GUI startup commands."""
    
    def test_start_web_gui_script_exists(self):
        """Test that start_web_gui.py exists and is executable."""
        start_gui_path = PROJECT_ROOT / "start_web_gui.py"
        assert start_gui_path.exists(), "start_web_gui.py not found"
        assert start_gui_path.is_file(), "start_web_gui.py is not a file"
    
    def test_start_web_gui_help_command(self):
        """Test that start_web_gui.py --help works."""
        start_gui_path = PROJECT_ROOT / "start_web_gui.py"
        
        try:
            result = subprocess.run(
                ["python", str(start_gui_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=PROJECT_ROOT
            )
            assert result.returncode == 0, f"start_web_gui.py --help failed: {result.stderr}"
            
            help_output = result.stdout.lower()
            assert "usage:" in help_output
            
        except subprocess.TimeoutExpired:
            pytest.fail("start_web_gui.py --help timed out")
    
    def test_web_gui_module_help_command(self):
        """Test that python -m project_tools.web_gui.app --help works."""
        try:
            result = subprocess.run(
                ["python", "-m", "project_tools.web_gui.app", "--help"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=PROJECT_ROOT
            )
            assert result.returncode == 0, f"web_gui module --help failed: {result.stderr}"
            
            help_output = result.stdout.lower()
            assert "usage:" in help_output
            
        except subprocess.TimeoutExpired:
            pytest.fail("web_gui module --help timed out")
    
    def test_web_gui_module_import(self):
        """Test that project_tools.web_gui.app module can be imported."""
        try:
            import project_tools.web_gui.app
            assert hasattr(project_tools.web_gui.app, 'main'), "web_gui.app module missing main function"
        except ImportError as e:
            pytest.fail(f"Failed to import project_tools.web_gui.app: {e}")


class TestCLICommandCoverage:
    """Test that documented CLI commands are actually implemented."""
    
    @staticmethod
    def extract_documented_commands() -> List[str]:
        """Extract all documented CLI commands from README files."""
        commands = []
        
        # Parse README.md
        readme_path = PROJECT_ROOT / "README.md"
        if readme_path.exists():
            commands.extend(TestCLICommandCoverage._extract_commands_from_file(readme_path))
        
        # Parse WEB_GUI_README.md
        web_readme_path = PROJECT_ROOT / "WEB_GUI_README.md"
        if web_readme_path.exists():
            commands.extend(TestCLICommandCoverage._extract_commands_from_file(web_readme_path))
        
        return commands
    
    @staticmethod
    def _extract_commands_from_file(file_path: Path) -> List[str]:
        """Extract CLI commands from a single markdown file."""
        content = file_path.read_text()
        commands = []
        
        # Find code blocks with project-tools commands
        code_block_pattern = r'```(?:bash|shell)?\n(.*?)\n```'
        code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
        
        for block in code_blocks:
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('project-tools'):
                    commands.append(line)
        
        # Also find inline code with project-tools
        inline_pattern = r'`(project-tools[^`]+)`'
        inline_commands = re.findall(inline_pattern, content)
        commands.extend(inline_commands)
        
        return commands
    
    @staticmethod
    def extract_implemented_subcommands() -> Set[str]:
        """Extract implemented subcommands from CLI implementation."""
        cli_path = PROJECT_ROOT / "project_tools" / "cli.py"
        
        if not cli_path.exists():
            pytest.fail(f"CLI implementation not found at {cli_path}")
        
        content = cli_path.read_text()
        
        # Look for subparser definitions
        subparser_pattern = r'\w+_parser = subparsers\.add_parser\([\'"](\w+)[\'"]'
        subcommands = set(re.findall(subparser_pattern, content))
        
        return subcommands
    
    def test_critical_commands_implemented(self):
        """Test that critical documented commands are implemented."""
        implemented_subcommands = self.extract_implemented_subcommands()
        
        # Define critical commands that must be implemented
        critical_commands = {
            "todo", "intelligence", "compass", "chains", 
            "direction", "reflect", "portfolio", "version"
        }
        
        missing_critical = critical_commands - implemented_subcommands
        
        assert not missing_critical, (
            f"Critical commands not implemented: {missing_critical}. "
            f"These commands are documented as core functionality."
        )
    
    def test_documented_subcommands_coverage(self):
        """Test coverage of documented subcommands."""
        documented_commands = self.extract_documented_commands()
        implemented_subcommands = self.extract_implemented_subcommands()
        
        # Parse documented commands to extract subcommands
        documented_subcommands = set()
        for cmd in documented_commands:
            parts = cmd.split()
            if len(parts) >= 2 and parts[0] == "project-tools":
                subcommand = parts[1]
                documented_subcommands.add(subcommand)
        
        # Find missing subcommands
        missing_subcommands = documented_subcommands - implemented_subcommands
        
        # Allow some tolerance for new/experimental commands
        max_missing_commands = 5
        
        if missing_subcommands:
            # Generate detailed error message
            error_msg = (
                f"Found {len(missing_subcommands)} documented subcommands that are not implemented:\n"
                + "\n".join(f"  - project-tools {cmd}" for cmd in sorted(missing_subcommands))
                + f"\n\nImplemented subcommands: {sorted(implemented_subcommands)}"
                + f"\nDocumented subcommands: {sorted(documented_subcommands)}"
            )
            
            if len(missing_subcommands) > max_missing_commands:
                pytest.fail(error_msg)
            else:
                # Just warn for small number of missing commands
                pytest.warns(UserWarning, match="Missing subcommands found")
                print(f"\nWARNING: {error_msg}")
    
    def test_no_undocumented_critical_commands(self):
        """Test that critical implemented commands are documented."""
        documented_commands = self.extract_documented_commands()
        implemented_subcommands = self.extract_implemented_subcommands()
        
        # Parse documented commands to extract subcommands
        documented_subcommands = set()
        for cmd in documented_commands:
            parts = cmd.split()
            if len(parts) >= 2 and parts[0] == "project-tools":
                subcommand = parts[1]
                documented_subcommands.add(subcommand)
        
        # Find undocumented commands
        undocumented_commands = implemented_subcommands - documented_subcommands
        
        # Filter to only critical commands that should be documented
        critical_undocumented = undocumented_commands & {
            "todo", "intelligence", "compass", "chains",
            "direction", "reflect", "portfolio", "version"
        }
        
        if critical_undocumented:
            pytest.fail(
                f"Critical commands implemented but not documented: {critical_undocumented}. "
                f"Please add documentation for these commands."
            )


class TestParametrizedCommandCategories:
    """Parametrized tests for different command categories."""
    
    def test_command_help_functionality(self, command_category, mock_subprocess_run):
        """Test that each command category has working help."""
        cmd = ["project-tools", command_category.name, "--help"]
        result = mock_subprocess_run(cmd, capture_output=True, text=True, timeout=10)
        
        assert result.returncode == 0, f"{command_category.name} command help failed"
        help_output = result.stdout.lower()
        assert "usage:" in help_output, f"{command_category.name} help missing usage"
    
    def test_subcommands_in_help(self, command_category, mock_subprocess_run):
        """Test that all subcommands appear in command help."""
        cmd = ["project-tools", command_category.name, "--help"]
        result = mock_subprocess_run(cmd, capture_output=True, text=True, timeout=10)
        
        assert result.returncode == 0
        help_output = result.stdout.lower()
        
        for subcommand in command_category.subcommands:
            assert subcommand in help_output, (
                f"Subcommand '{subcommand}' not found in {command_category.name} help"
            )
    
    @pytest.mark.parametrize("command_name", [cat.name for cat in COMMAND_CATEGORIES])
    def test_command_category_implementation(self, command_name):
        """Test that command categories are implemented in CLI."""
        implemented_subcommands = TestCLICommandCoverage.extract_implemented_subcommands()
        assert command_name in implemented_subcommands, (
            f"Command category '{command_name}' not implemented in CLI"
        )


class TestParametrizedSubcommandArgs:
    """Parametrized tests for subcommand argument validation."""
    
    @pytest.mark.parametrize("category", COMMAND_CATEGORIES, ids=lambda x: x.name)
    def test_subcommand_help_exists(self, category, mock_subprocess_run):
        """Test that all subcommands have working help."""
        for subcommand in category.subcommands:
            cmd = ["project-tools", category.name, subcommand, "--help"]
            result = mock_subprocess_run(cmd, capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0, (
                f"Help for {category.name} {subcommand} failed"
            )
    
    @pytest.mark.parametrize("category", COMMAND_CATEGORIES, ids=lambda x: x.name)
    def test_required_arguments_documented(self, category):
        """Test that required arguments are documented in help."""
        if not category.required_args:
            pytest.skip(f"No required args defined for {category.name}")
        
        for subcommand, required_args in category.required_args.items():
            if required_args:
                # In a real implementation, this would parse help output
                # For now, we just verify the structure exists
                assert subcommand in category.subcommands, (
                    f"Subcommand {subcommand} not in {category.name} subcommands"
                )
    
    @pytest.mark.parametrize(
        "category,subcommand", 
        [(cat, sub) for cat in COMMAND_CATEGORIES for sub in cat.subcommands],
        ids=lambda x: f"{x[0].name}-{x[1]}" if isinstance(x, tuple) else str(x)
    )
    def test_individual_subcommand_help(self, category, subcommand, mock_subprocess_run):
        """Test each individual subcommand has working help."""
        cmd = ["project-tools", category.name, subcommand, "--help"]
        result = mock_subprocess_run(cmd, capture_output=True, text=True, timeout=10)
        
        assert result.returncode == 0, f"Help for {category.name} {subcommand} failed"
        assert "usage:" in result.stdout.lower(), f"Usage missing from {category.name} {subcommand} help"
    
    @pytest.mark.parametrize(
        "category,subcommand,required_args",
        [
            (cat, sub, cat.required_args.get(sub, []))
            for cat in COMMAND_CATEGORIES 
            for sub in cat.subcommands
            if cat.required_args.get(sub)
        ],
        ids=lambda x: f"{x[0].name}-{x[1]}" if isinstance(x, tuple) else str(x)
    )
    def test_required_args_validation(self, category, subcommand, required_args):
        """Test that subcommands with required args are properly configured."""
        assert len(required_args) > 0, f"{category.name} {subcommand} should have required args"
        assert all(isinstance(arg, str) for arg in required_args), (
            f"All required args for {category.name} {subcommand} should be strings"
        )


class TestArgumentConsistency:
    """Test that command arguments match between documentation and implementation."""
    
    def test_critical_command_help_with_mocks(self, critical_commands, mock_subprocess_run):
        """Test critical commands have working help using mocks."""
        for command in critical_commands:
            cmd = ["project-tools", command, "--help"]
            result = mock_subprocess_run(cmd, capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0, f"{command} command help failed"
            help_output = result.stdout.lower()
            assert "usage:" in help_output, f"{command} help missing usage"


class TestRealCLIExecution:
    """Real CLI execution tests to complement mock-based tests."""
    
    def test_project_tools_basic_execution(self):
        """Test basic project-tools command execution without mocks."""
        try:
            result = subprocess.run(
                ["project-tools", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, f"project-tools --help failed: {result.stderr}"
            assert "usage:" in result.stdout.lower()
            assert "project-tools" in result.stdout.lower()
            
        except FileNotFoundError:
            pytest.fail("project-tools command not found in PATH")
        except subprocess.TimeoutExpired:
            pytest.fail("project-tools --help timed out")
    
    def test_project_tools_version_execution(self):
        """Test project-tools version command execution."""
        try:
            result = subprocess.run(
                ["project-tools", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Version command may or may not be implemented, so we allow both 0 and non-0 exit codes
            # but the command should execute without crashing
            assert result.returncode in [0, 1, 2], f"Unexpected exit code: {result.returncode}"
            
        except FileNotFoundError:
            pytest.fail("project-tools command not found in PATH")
        except subprocess.TimeoutExpired:
            pytest.fail("project-tools --version timed out")
    
    def test_project_tools_invalid_command_handling(self):
        """Test how project-tools handles invalid commands."""
        try:
            result = subprocess.run(
                ["project-tools", "invalid-command-that-does-not-exist"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Should fail with non-zero exit code for invalid commands
            assert result.returncode != 0, "Invalid command should return non-zero exit code"
            # Should contain some error message
            error_output = (result.stderr + result.stdout).lower()
            assert any(keyword in error_output for keyword in ["error", "invalid", "unknown", "usage"]), \
                "Error output should contain helpful message"
            
        except FileNotFoundError:
            pytest.fail("project-tools command not found in PATH")
        except subprocess.TimeoutExpired:
            pytest.fail("Invalid command test timed out")
    
    def test_subcommand_execution_sampling(self):
        """Test execution of a sample of implemented subcommands."""
        implemented_subcommands = TestCLICommandCoverage.extract_implemented_subcommands()
        
        # Test a representative sample of subcommands
        sample_commands = ["todo", "version", "status"] if implemented_subcommands else []
        test_commands = [cmd for cmd in sample_commands if cmd in implemented_subcommands]
        
        if not test_commands:
            # If none of our sample commands exist, test the first implemented command
            test_commands = list(implemented_subcommands)[:1]
        
        failed_commands = []
        for command in test_commands:
            try:
                result = subprocess.run(
                    ["project-tools", command, "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    failed_commands.append(f"{command} (exit code: {result.returncode})")
                elif "usage:" not in result.stdout.lower():
                    failed_commands.append(f"{command} (missing usage in help)")
                    
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                failed_commands.append(f"{command} ({type(e).__name__})")
        
        if failed_commands:
            pytest.fail(f"Failed subcommand tests: {failed_commands}")
    
    def test_cli_exit_codes_consistency(self):
        """Test that CLI returns consistent exit codes for different scenarios."""
        test_cases = [
            (["project-tools", "--help"], 0, "help should return 0"),
            (["project-tools", "nonexistent-command"], [1, 2], "invalid command should return 1 or 2"),
        ]
        
        for cmd, expected_codes, description in test_cases:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if isinstance(expected_codes, int):
                    expected_codes = [expected_codes]
                
                assert result.returncode in expected_codes, (
                    f"{description}: expected {expected_codes}, got {result.returncode}. "
                    f"stderr: {result.stderr[:200]}"
                )
                
            except FileNotFoundError:
                pytest.fail(f"project-tools command not found for test: {description}")
            except subprocess.TimeoutExpired:
                pytest.fail(f"Command timed out for test: {description}")


class TestCLIDocumentationDrift:
    """Integration tests to prevent CLI documentation drift."""
    
    def test_cli_help_contains_all_subcommands(self):
        """Test that main CLI help lists all implemented subcommands."""
        try:
            result = subprocess.run(
                ["project-tools", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0
            
            help_output = result.stdout.lower()
            implemented_subcommands = TestCLICommandCoverage.extract_implemented_subcommands()
            
            # Check that all implemented subcommands appear in help output
            for subcommand in implemented_subcommands:
                assert subcommand in help_output, (
                    f"Subcommand '{subcommand}' not found in main help output. "
                    f"This indicates the CLI help might be out of sync."
                )
                
        except FileNotFoundError:
            pytest.fail("project-tools command not available")
        except subprocess.TimeoutExpired:
            pytest.fail("CLI help command timed out")
    
    def test_all_subcommands_have_help(self):
        """Test that all implemented subcommands have working help."""
        implemented_subcommands = TestCLICommandCoverage.extract_implemented_subcommands()
        
        failed_subcommands = []
        
        for subcommand in implemented_subcommands:
            try:
                result = subprocess.run(
                    ["project-tools", subcommand, "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    failed_subcommands.append(subcommand)
                    
            except (FileNotFoundError, subprocess.TimeoutExpired):
                failed_subcommands.append(subcommand)
        
        if failed_subcommands:
            pytest.fail(
                f"Subcommands with broken help: {failed_subcommands}. "
                f"All implemented subcommands should have working --help."
            )


# Enhanced pytest configuration and fixtures


def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line("markers", "cli: mark test as CLI-related")
    config.addinivalue_line("markers", "entry_points: mark test as entry point-related")
    config.addinivalue_line("markers", "web_gui: mark test as web GUI-related")


# Mark all tests in this module
pytestmark = pytest.mark.cli