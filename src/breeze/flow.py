"""Flow orchestration and coordination logic."""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .nodes import (
    DocAgentNode, SummaryAgentNode, TestGenerationAgentNode,
    BugDetectionAgentNode, RefactorCodeAgentNode, TypeAnnotationAgentNode,
    MigrationAgentNode, OrchestratorNode, FileManagementNode,
    SafetyCheckNode, ContextAwarenessNode, ErrorHandlingNode
)
from .utils import read_file_content, write_file_content, get_output_filename


class FlowOrchestrator:
    """Main orchestrator for managing agent flows and task coordination."""
    
    def __init__(self):
        """Initialize the flow orchestrator with all agent nodes."""
        self.doc_agent = DocAgentNode()
        self.summary_agent = SummaryAgentNode()
        self.test_agent = TestGenerationAgentNode()
        self.bug_agent = BugDetectionAgentNode()
        self.refactor_agent = RefactorCodeAgentNode()
        self.type_agent = TypeAnnotationAgentNode()
        self.migration_agent = MigrationAgentNode()
        self.orchestrator = OrchestratorNode()
        self.file_manager = FileManagementNode()
        self.safety_check = SafetyCheckNode()
        self.context_aware = ContextAwarenessNode()
        self.error_handler = ErrorHandlingNode()
    
    def process_command(
        self,
        command: str,
        path: Optional[str] = None,
        output_mode: str = "console",
        secure: bool = False,
        verbose: bool = False,
        target: Optional[str] = None
    ) -> str:
        """Process a CLI command through the appropriate agent flow."""
        try:
            # Read file content if path is provided
            file_content = None
            if path:
                file_content = read_file_content(path)
                if verbose:
                    print(f"Read {len(file_content)} characters from {path}")
            
            # Add context awareness
            context = self.context_aware.analyze_context(file_content, path)
            if verbose and context:
                print(f"Context analysis: {context}")
            
            # Route to appropriate agent
            result = self._route_command(command, file_content, path, target, verbose)
            
            # Apply safety checks if modifications are involved
            if secure and command in ["refactor", "annotate", "migrate"]:
                if not self.safety_check.approve_changes(result, verbose):
                    return "Operation cancelled by user."
            
            # Handle output based on mode
            return self._handle_output(result, path, output_mode, command, verbose)
            
        except Exception as e:
            return self.error_handler.handle_error(e, command, path, verbose)
    
    def process_chat_input(self, user_input: str, verbose: bool = False) -> str:
        """Process natural language input in chat mode."""
        try:
            # Use orchestrator to understand intent
            intent = self.orchestrator.parse_intent(user_input, verbose)
            
            if intent.get("command"):
                return self.process_command(
                    command=intent["command"],
                    path=intent.get("path"),
                    output_mode=intent.get("output_mode", "console"),
                    secure=intent.get("secure", False),
                    verbose=verbose,
                    target=intent.get("target")
                )
            else:
                return self.orchestrator.handle_general_query(user_input, verbose)
                
        except Exception as e:
            return self.error_handler.handle_error(e, "chat", None, verbose)
    
    def _route_command(
        self, 
        command: str, 
        content: Optional[str], 
        path: Optional[str],
        target: Optional[str],
        verbose: bool
    ) -> str:
        """Route command to the appropriate agent node."""
        agents = {
            "doc": self.doc_agent,
            "summarize": self.summary_agent,
            "test": self.test_agent,
            "inspect": self.bug_agent,
            "refactor": self.refactor_agent,
            "annotate": self.type_agent,
            "migrate": self.migration_agent
        }
        
        agent = agents.get(command)
        if not agent:
            raise ValueError(f"Unknown command: {command}")
        
        # Special handling for migration agent
        if command == "migrate" and target:
            return agent.process(content, path, target=target, verbose=verbose)
        else:
            return agent.process(content, path, verbose=verbose)
    
    def _handle_output(
        self, 
        result: str, 
        path: Optional[str],
        output_mode: str,
        command: str,
        verbose: bool
    ) -> str:
        """Handle output based on the specified mode."""
        if output_mode == "console":
            return result
        elif output_mode == "in-place" and path:
            if command in ["doc", "refactor", "annotate", "migrate"]:
                write_file_content(path, result)
                return f"Changes applied to {path}"
            else:
                return "In-place output not supported for this command. Use console or new-file."
        elif output_mode == "new-file" and path:
            output_path = get_output_filename(path, command)
            write_file_content(output_path, result)
            return f"Output saved to {output_path}"
        else:
            return result
