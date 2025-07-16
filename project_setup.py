#!/usr/bin/env python3
"""
Project Tools Setup Guide

Interactive setup script to help users configure project_tools
based on their project needs and complexity preferences.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from project_tools import ProjectManager


class ProjectSetupGuide:
    """Guided setup for project_tools with different complexity levels"""
    
    def __init__(self):
        self.project_root = os.getcwd()
        self.responses = {}
        self.setup_mode = None
        
    def welcome(self):
        """Display welcome message and overview"""
        print("🚀 Welcome to Project Tools Setup Guide!")
        print("=" * 50)
        print("This setup will help you configure project_tools for your specific needs.")
        print("We'll ask a few questions to determine the best configuration for you.\n")
    
    def ask_project_type(self) -> str:
        """Ask about project type to suggest appropriate templates"""
        print("📋 What type of project are you working on?")
        print("1. Software Development (app, website, library)")
        print("2. Business/Startup (product launch, business development)")
        print("3. Research/Study (academic, personal learning, analysis)")
        print("4. Creative Project (content, design, writing)")
        print("5. Personal/Life Goal (skill development, habits)")
        print("6. Other/Custom")
        
        while True:
            try:
                choice = input("\nEnter choice (1-6): ").strip()
                types = {
                    "1": "software",
                    "2": "business", 
                    "3": "research",
                    "4": "creative",
                    "5": "personal",
                    "6": "custom"
                }
                if choice in types:
                    return types[choice]
                print("Please enter a number between 1-6")
            except KeyboardInterrupt:
                print("\nSetup cancelled.")
                exit(0)
    
    def ask_complexity_preference(self) -> str:
        """Ask about desired complexity level"""
        print("\n🎛️ How much project management complexity do you want?")
        print("1. Light - Just todos and version tracking (simple, focused)")
        print("2. Standard - Add strategic direction and reflection (balanced)")
        print("3. Full Intelligence - Complete AI-assisted system (powerful)")
        
        print("\n💡 Recommendations:")
        print("• Light: Good for simple projects, quick tasks, learning the system")
        print("• Standard: Best for most projects - strategic tracking without overwhelm")
        print("• Full: Complex projects, business ventures, research with lots of context")
        
        while True:
            try:
                choice = input("\nEnter choice (1-3): ").strip()
                modes = {"1": "light", "2": "standard", "3": "full"}
                if choice in modes:
                    return modes[choice]
                print("Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\nSetup cancelled.")
                exit(0)
    
    def ask_project_details(self, project_type: str) -> Dict:
        """Ask for project-specific details"""
        details = {}
        
        print(f"\n📝 Let's set up your {project_type} project:")
        
        # Project name
        default_name = os.path.basename(self.project_root)
        project_name = input(f"Project name (default: {default_name}): ").strip()
        details['name'] = project_name if project_name else default_name
        
        # Project description
        description = input("Brief project description: ").strip()
        details['description'] = description
        
        # Timeline (optional)
        timeline = input("Target timeline (e.g., '3 months', 'Q2 2024', optional): ").strip()
        if timeline:
            details['timeline'] = timeline
            
        return details
    
    def create_light_setup(self, details: Dict) -> ProjectManager:
        """Create light setup - todos + changelog only"""
        pm = ProjectManager(enable_intelligence=False)
        
        # Add some starter todos based on project type
        if self.responses['project_type'] == 'software':
            pm.add_todo("Set up development environment", 
                       "Configure tools, dependencies, and workspace", 7, "setup")
            pm.add_todo("Plan project architecture", 
                       "Define structure, components, and technical approach", 8, "planning")
            pm.add_todo("Implement core functionality", 
                       "Build main features and functionality", 9, "feature")
            
        elif self.responses['project_type'] == 'business':
            pm.add_todo("Define business model and goals", 
                       "Clarify value proposition and success metrics", 9, "planning")
            pm.add_todo("Research market and competition", 
                       "Understand target market and competitive landscape", 8, "research")
            pm.add_todo("Create initial implementation plan", 
                       "Define steps to reach first milestone", 7, "planning")
            
        else:  # research, creative, personal, custom
            pm.add_todo("Define project scope and goals", 
                       "Clarify what success looks like", 8, "planning")
            pm.add_todo("Research and gather resources", 
                       "Collect information, tools, and materials needed", 7, "research")
            pm.add_todo("Create action plan", 
                       "Break down project into actionable steps", 7, "planning")
        
        return pm
    
    def create_standard_setup(self, details: Dict) -> ProjectManager:
        """Create standard setup - todos + direction + reflection"""
        pm = ProjectManager(enable_intelligence=True, 
                          intelligence_features={
                              "compass": True,
                              "direction": True, 
                              "reflection": True,
                              "task_chains": False,
                              "portfolio": False
                          })
        
        # Initialize intelligence
        pm.initialize_intelligence(details['name'])
        
        # Set up direction based on project type
        direction = pm.get_direction_tracker()
        
        if self.responses['project_type'] == 'software':
            direction.set_current_direction(
                direction="Build working MVP with core features",
                rationale="Need to validate technical approach and user needs",
                success_indicators=["Working prototype", "User feedback", "Technical validation"],
                time_horizon=details.get('timeline', '3 months')
            )
            direction.add_assumption("Technical approach is feasible with available resources", "high", critical=True)
            direction.add_assumption("User needs match planned features", "medium", critical=True)
            
        elif self.responses['project_type'] == 'business':
            direction.set_current_direction(
                direction="Validate business model and achieve initial traction",
                rationale="Need to prove market fit before scaling",
                success_indicators=["Market validation", "Customer acquisition", "Revenue generation"],
                time_horizon=details.get('timeline', '6 months')
            )
            direction.add_assumption("Market demand exists for solution", "medium", critical=True)
            direction.add_assumption("Business model is viable", "medium", critical=True)
            
        else:
            direction.set_current_direction(
                direction=f"Complete {details['name']} with desired outcomes",
                rationale="Clear direction helps maintain focus and measure progress",
                success_indicators=["Project completion", "Learning objectives met", "Quality standards achieved"],
                time_horizon=details.get('timeline', '2 months')
            )
        
        # Add todos with more strategic context
        self.add_strategic_todos(pm, details)
        
        return pm
    
    def create_full_setup(self, details: Dict) -> ProjectManager:
        """Create full intelligence setup"""
        pm = ProjectManager(enable_intelligence=True)
        
        # Initialize all intelligence features
        pm.initialize_intelligence(details['name'])
        
        # Set up comprehensive direction tracking
        direction = pm.get_direction_tracker()
        compass = pm.get_compass()
        
        # Add business context to compass
        compass.add_context_entry("setup", f"Project initialized with full intelligence features")
        compass.add_context_entry("project_type", f"Project type: {self.responses['project_type']}")
        if details.get('timeline'):
            compass.add_context_entry("timeline", f"Target timeline: {details['timeline']}")
        
        # Set up direction with comprehensive assumptions
        self.setup_comprehensive_direction(pm, details)
        
        # Create task chains for organized workflow
        self.setup_task_chains(pm, details)
        
        # Initial reflection setup
        reflection = pm.get_reflection_manager()
        reflection.log_energy_level(8, "Excited to start project with full intelligence system",
                                   factors=["Clear setup", "Comprehensive tracking", "AI assistance"])
        reflection.capture_learning("Starting with structured intelligence system for better project outcomes", 
                                   "setup", actionable=True)
        
        return pm
    
    def add_strategic_todos(self, pm: ProjectManager, details: Dict):
        """Add todos with strategic context for standard setup"""
        project_type = self.responses['project_type']
        
        if project_type == 'software':
            todos = [
                ("Define technical requirements", "Specify technical constraints, dependencies, and architecture decisions", 8, "planning"),
                ("Set up development workflow", "Configure version control, testing, and deployment processes", 7, "infrastructure"),
                ("Implement core features", "Build primary functionality that delivers main value", 9, "feature"),
                ("Create user documentation", "Write guides and documentation for users", 6, "documentation"),
                ("Test and validate solution", "Comprehensive testing and user feedback collection", 8, "testing")
            ]
        elif project_type == 'business':
            todos = [
                ("Validate market opportunity", "Research market size, competition, and customer needs", 9, "research"),
                ("Develop business strategy", "Define business model, pricing, and go-to-market approach", 8, "planning"),
                ("Build initial offering", "Create minimum viable product or service", 9, "development"),
                ("Establish operational processes", "Set up systems for delivery, customer service, and operations", 7, "operations"),
                ("Measure and optimize", "Track metrics, gather feedback, and iterate", 8, "optimization")
            ]
        else:
            todos = [
                ("Research and planning", "Gather information and create detailed project plan", 8, "research"),
                ("Setup and preparation", "Organize tools, workspace, and resources", 7, "setup"),
                ("Core implementation", "Execute main project activities", 9, "implementation"),
                ("Review and refinement", "Evaluate progress and make improvements", 7, "review"),
                ("Completion and documentation", "Finalize project and document outcomes", 6, "completion")
            ]
        
        for title, desc, priority, category in todos:
            pm.add_todo(title, desc, priority, category)
    
    def setup_comprehensive_direction(self, pm: ProjectManager, details: Dict):
        """Set up comprehensive direction tracking for full setup"""
        direction = pm.get_direction_tracker()
        project_type = self.responses['project_type']
        
        if project_type == 'software':
            direction.set_current_direction(
                direction="Build high-quality software solution that meets user needs",
                rationale="Success requires balancing technical excellence with user value",
                success_indicators=[
                    "Working software with core features",
                    "Positive user feedback and adoption",
                    "Maintainable, scalable codebase",
                    "Comprehensive documentation and tests"
                ],
                time_horizon=details.get('timeline', '3-6 months')
            )
            
            # Add comprehensive assumptions
            direction.add_assumption("Chosen technology stack is appropriate for requirements", "high", critical=True)
            direction.add_assumption("Team has necessary skills for implementation", "medium", critical=True)
            direction.add_assumption("User requirements are well-understood", "medium", critical=True)
            direction.add_assumption("Timeline allows for quality development", "medium", critical=False)
            
        elif project_type == 'business':
            direction.set_current_direction(
                direction="Build sustainable business with proven market fit",
                rationale="Long-term success requires systematic validation and growth",
                success_indicators=[
                    "Clear value proposition validated by customers",
                    "Repeatable customer acquisition process",
                    "Positive unit economics and growth metrics",
                    "Operational systems that scale"
                ],
                time_horizon=details.get('timeline', '6-12 months')
            )
            
            direction.add_assumption("Market opportunity is large enough for viable business", "medium", critical=True)
            direction.add_assumption("Solution addresses real customer pain point", "high", critical=True)
            direction.add_assumption("Business model creates sustainable competitive advantage", "medium", critical=True)
            direction.add_assumption("Team can execute on business plan", "high", critical=False)
            
        else:  # research, creative, personal
            direction.set_current_direction(
                direction=f"Successfully complete {details['name']} with measurable outcomes",
                rationale="Clear direction and milestones ensure project completion and learning",
                success_indicators=[
                    "Project objectives fully achieved",
                    "New skills and knowledge acquired", 
                    "Quality output produced",
                    "Learnings documented for future projects"
                ],
                time_horizon=details.get('timeline', '2-4 months')
            )
            
            direction.add_assumption("Project scope is realistic for available time and resources", "medium", critical=True)
            direction.add_assumption("Required skills can be learned or accessed", "high", critical=False)
            direction.add_assumption("Project motivation will be sustained", "medium", critical=False)
    
    def setup_task_chains(self, pm: ProjectManager, details: Dict):
        """Set up logical task chains for full setup"""
        chains = pm.get_task_chains()
        project_type = self.responses['project_type']
        
        # Get current todos to organize into chains
        todos = pm.get_todos()
        
        if project_type == 'software':
            # Create planning chain
            planning_chain = chains.create_task_chain(
                "Project Planning & Setup",
                "Foundation planning and environment setup"
            )
            
            # Create development chain  
            dev_chain = chains.create_task_chain(
                "Core Development",
                "Implementation of main features and functionality"
            )
            
            # Create validation chain
            validation_chain = chains.create_task_chain(
                "Testing & Validation", 
                "Quality assurance and user validation"
            )
            
        elif project_type == 'business':
            # Create validation chain
            validation_chain = chains.create_task_chain(
                "Market Validation",
                "Validate market opportunity and business model"
            )
            
            # Create build chain
            build_chain = chains.create_task_chain(
                "Product Development",
                "Build initial offering and operational systems"
            )
            
            # Create growth chain
            growth_chain = chains.create_task_chain(
                "Launch & Growth",
                "Go to market and scale operations"
            )
        
        else:
            # Generic project chains
            plan_chain = chains.create_task_chain(
                "Planning & Preparation",
                "Project planning and resource preparation"
            )
            
            execute_chain = chains.create_task_chain(
                "Execution",
                "Core project implementation"
            )
            
            complete_chain = chains.create_task_chain(
                "Completion & Review",
                "Finalization and outcome documentation"
            )
    
    def save_setup_summary(self, pm: ProjectManager):
        """Save setup summary for user reference"""
        summary = {
            "setup_date": pm.get_current_version(),
            "setup_mode": self.setup_mode,
            "project_type": self.responses['project_type'],
            "intelligence_enabled": pm.intelligence is not None,
            "initial_todos": len(pm.get_todos()),
            "setup_responses": self.responses
        }
        
        # Save to project_management directory if it exists
        if pm.intelligence:
            summary_path = Path(self.project_root) / "project_management" / "setup_summary.json"
            summary_path.parent.mkdir(exist_ok=True)
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
        else:
            # Save to project root for light setup
            summary_path = Path(self.project_root) / "project_setup_summary.json"
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
        
        return summary_path
    
    def display_next_steps(self, pm: ProjectManager):
        """Show user what to do next"""
        print("\n🎉 Setup Complete!")
        print("=" * 30)
        
        print(f"✅ Mode: {self.setup_mode.title()}")
        print(f"✅ Project Type: {self.responses['project_type'].title()}")
        print(f"✅ Initial Todos: {len(pm.get_todos())}")
        
        if pm.intelligence:
            print(f"✅ Intelligence Features: Active")
        
        print("\n📋 Next Steps:")
        print("1. Review your initial todos:")
        
        todos = pm.get_todos()
        for i, todo in enumerate(todos[:3], 1):
            print(f"   {i}. {todo['title']} (Priority: {todo['priority']})")
        
        if len(todos) > 3:
            print(f"   ... and {len(todos) - 3} more")
        
        print("\n2. Useful commands:")
        print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); print(f'Status: {pm.get_integrated_status()}')\"")
        
        if pm.intelligence:
            print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); print(f'AI Opportunities: {pm.get_ai_enhancement_summary()}')\"")
        
        print(f"\n3. Your project data is stored in:")
        print(f"   - todo.json (your tasks)")
        print(f"   - changelog.json (version history)")
        
        if pm.intelligence:
            print(f"   - project_management/ (intelligence files)")
        
        print("\n🚀 You're ready to start managing your project with project_tools!")
    
    def offer_claude_integration(self, pm: ProjectManager):
        """Offer to create CLAUDE.md file for Claude Code integration"""
        print("\n🤖 Claude Code Integration")
        print("=" * 30)
        print("Would you like to create a CLAUDE.md file for Claude Code integration?")
        print("This file helps Claude Code understand how to use project_tools in your project.")
        
        create_claude = input("\nCreate CLAUDE.md file? (y/n): ").lower().strip()
        
        if create_claude in ['y', 'yes']:
            try:
                claude_path = pm.save_claude_md()
                print(f"✅ CLAUDE.md created at: {claude_path}")
                print("\n📝 This file contains:")
                print("• Essential project_tools commands")
                print("• Project-specific examples and workflows")
                print("• Current project status and configuration")
                print("• Best practices for Claude Code integration")
                
                # Show snippet option
                print("\n💡 Tip: You can also get a condensed snippet anytime with:")
                print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); print(pm.get_claude_snippet())\"")
                
            except Exception as e:
                print(f"❌ Failed to create CLAUDE.md: {e}")
                print("\n📋 You can create it manually later with:")
                print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); pm.save_claude_md()\"")
        else:
            print("\n📋 You can create CLAUDE.md later with:")
            print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); pm.save_claude_md()\"")
            print("\nOr get a snippet with:")
            print("   python -c \"from project_tools import ProjectManager; pm = ProjectManager(); print(pm.get_claude_snippet())\"")
    
    def run_setup(self):
        """Run the complete setup process"""
        try:
            self.welcome()
            
            # Gather requirements
            project_type = self.ask_project_type()
            complexity = self.ask_complexity_preference()
            details = self.ask_project_details(project_type)
            
            self.responses = {
                'project_type': project_type,
                'complexity': complexity,
                'details': details
            }
            self.setup_mode = complexity
            
            print(f"\n⚙️ Setting up {complexity} mode for {project_type} project...")
            
            # Create appropriate setup
            if complexity == 'light':
                pm = self.create_light_setup(details)
            elif complexity == 'standard':
                pm = self.create_standard_setup(details)
            else:  # full
                pm = self.create_full_setup(details)
            
            # Save summary and show next steps
            summary_path = self.save_setup_summary(pm)
            self.display_next_steps(pm)
            
            print(f"\n💾 Setup summary saved to: {summary_path}")
            
            # Ask about Claude Code integration
            self.offer_claude_integration(pm)
            
        except KeyboardInterrupt:
            print("\n\nSetup cancelled by user.")
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            print("You can still use project_tools manually with: ProjectManager()")


def main():
    """Main entry point for setup script"""
    setup = ProjectSetupGuide()
    setup.run_setup()


if __name__ == "__main__":
    main()