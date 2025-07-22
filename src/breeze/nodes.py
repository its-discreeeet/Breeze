"""Agent node implementations for different code processing tasks."""

import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pathlib import Path

from .call_gemini import GeminiAPIProxy


class BaseAgentNode(ABC):
    """Base class for all agent nodes."""
    
    def __init__(self):
        """Initialize base agent with Gemini API proxy."""
        self.gemini = GeminiAPIProxy()
    
    @abstractmethod
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process the input and return results."""
        pass
    
    def _get_file_context(self, path: Optional[str]) -> str:
        """Get contextual information about the file."""
        if not path:
            return ""
        
        file_path = Path(path)
        return f"File: {file_path.name}\nPath: {path}\n"


class DocAgentNode(BaseAgentNode):
    """Agent for generating Google-style docstrings."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate docstrings for Python code."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for docstring generation."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please generate Google-style docstrings for all functions and classes in the following Python code.
Only return the complete code with docstrings added, no explanations.

Code:
{content}
"""
        
        if verbose:
            print("Generating docstrings...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class SummaryAgentNode(BaseAgentNode):
    """Agent for creating code summaries."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate a summary of the code."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for summarization."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please provide a concise summary of the following Python code, including:
- Main purpose and functionality
- Key classes and functions
- Dependencies and imports
- Notable patterns or design decisions

Code:
{content}
"""
        
        if verbose:
            print("Generating code summary...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class TestGenerationAgentNode(BaseAgentNode):
    """Agent for generating unit tests."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate unit tests for the code."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for test generation."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please generate comprehensive unit tests for the following Python code using pytest.
Include tests for edge cases, error conditions, and main functionality.
Only return the test code, no explanations.

Code:
{content}
"""
        
        if verbose:
            print("Generating unit tests...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class BugDetectionAgentNode(BaseAgentNode):
    """Agent for detecting bugs and issues."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Analyze code for potential bugs and issues."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for bug detection."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please analyze the following Python code for potential bugs, issues, and improvements:
- Logic errors
- Security vulnerabilities
- Performance issues
- Code smells
- Best practice violations

Provide specific recommendations for each issue found.

Code:
{content}
"""
        
        if verbose:
            print("Analyzing code for bugs and issues...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class RefactorCodeAgentNode(BaseAgentNode):
    """Agent for code refactoring."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Suggest and apply code refactorings."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for refactoring."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please refactor the following Python code to improve:
- Code readability and maintainability
- Performance where applicable
- Following Python best practices
- Reducing complexity

Return the refactored code with improvements applied.

Code:
{content}
"""
        
        if verbose:
            print("Refactoring code...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class TypeAnnotationAgentNode(BaseAgentNode):
    """Agent for adding type annotations."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Add or update type annotations in the code."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for type annotation."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please add comprehensive type annotations to the following Python code:
- Function parameters and return types
- Variable types where helpful
- Generic types where applicable
- Import necessary typing modules

Return the complete code with type annotations added.

Code:
{content}
"""
        
        if verbose:
            print("Adding type annotations...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class MigrationAgentNode(BaseAgentNode):
    """Agent for code migration tasks."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Migrate code to a target version or library."""
        verbose = kwargs.get("verbose", False)
        target = kwargs.get("target", "")
        
        if not content:
            return "No content provided for migration."
        
        if not target:
            return "No migration target specified."
        
        context = self._get_file_context(path)
        
        prompt = f"""
{context}
Please migrate the following Python code to be compatible with: {target}

Consider:
- Deprecated features that need updating
- New syntax and best practices
- Library/API changes
- Python version compatibility

Return the migrated code that works with {target}.

Code:
{content}
"""
        
        if verbose:
            print(f"Migrating code to {target}...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class OrchestratorNode(BaseAgentNode):
    """Agent for orchestrating complex workflows and understanding user intent."""
    
    def parse_intent(self, user_input: str, verbose: bool = False) -> Dict[str, Any]:
        """Parse user intent from natural language input."""
        
        prompt = f"""
Analyze the following user input and extract the intent. 
Respond with a JSON object containing:
- command: one of [doc, summarize, test, inspect, refactor, annotate, migrate] or null
- path: file path if mentioned or null
- output_mode: console, in-place, or new-file (default: console)
- secure: true if user wants confirmation (default: false)
- target: migration target if command is migrate

User input: "{user_input}"
"""
        
        if verbose:
            print("Parsing user intent...")
        
        response = self.gemini.call_gemini(prompt, verbose=verbose)
        
        # Simple intent parsing (could be more sophisticated)
        intent = {}
        
        # Basic command detection
        commands = ["doc", "summarize", "test", "inspect", "refactor", "annotate", "migrate"]
        for cmd in commands:
            if cmd in user_input.lower():
                intent["command"] = cmd
                break
        
        # Extract file path
        import re
        path_match = re.search(r'(\S+\.py)', user_input)
        if path_match:
            intent["path"] = path_match.group(1)
        
        # Extract output mode
        if "in-place" in user_input.lower():
            intent["output_mode"] = "in-place"
        elif "new-file" in user_input.lower():
            intent["output_mode"] = "new-file"
        
        # Extract security preference
        if "secure" in user_input.lower() or "confirm" in user_input.lower():
            intent["secure"] = True
        
        # Extract migration target
        if intent.get("command") == "migrate":
            target_match = re.search(r'--target\s+["\']?([^"\']+)["\']?', user_input)
            if target_match:
                intent["target"] = target_match.group(1)
        
        return intent
    
    def handle_general_query(self, query: str, verbose: bool = False) -> str:
        """Handle general queries about code or Breeze functionality."""
        
        prompt = f"""
You are Breeze, an AI-powered Python code assistant. Answer the following query about 
Python code analysis, best practices, or tool usage:

Query: {query}
"""
        
        if verbose:
            print("Handling general query...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process orchestration tasks."""
        return self.handle_general_query(content or "", kwargs.get("verbose", False))


class FileManagementNode(BaseAgentNode):
    """Agent for file management operations."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process file management tasks."""
        operation = kwargs.get("operation", "read")
        
        if operation == "read":
            return self._read_file(path)
        elif operation == "write":
            return self._write_file(path, content, kwargs.get("backup", True))
        elif operation == "backup":
            return self._backup_file(path)
        else:
            return f"Unknown file operation: {operation}"
    
    def _read_file(self, path: Optional[str]) -> str:
        """Read file content safely."""
        if not path:
            return "No file path provided."
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def _write_file(self, path: Optional[str], content: Optional[str], backup: bool = True) -> str:
        """Write content to file with optional backup."""
        if not path or not content:
            return "Missing file path or content."
        
        try:
            if backup and Path(path).exists():
                backup_path = f"{path}.backup"
                Path(path).rename(backup_path)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"
    
    def _backup_file(self, path: Optional[str]) -> str:
        """Create a backup of the file."""
        if not path:
            return "No file path provided."
        
        try:
            source = Path(path)
            if not source.exists():
                return f"File {path} does not exist."
            
            backup_path = f"{path}.backup"
            source.rename(backup_path)
            return f"Backup created: {backup_path}"
        except Exception as e:
            return f"Error creating backup: {e}"


class SafetyCheckNode(BaseAgentNode):
    """Agent for safety checks and user approval."""
    
    def approve_changes(self, changes: str, verbose: bool = False) -> bool:
        """Request user approval for changes."""
        if verbose:
            print("Changes to be applied:")
            print("-" * 50)
            print(changes)
            print("-" * 50)
        
        while True:
            response = input("Apply these changes? (y/n/v): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['v', 'view']:
                print("\nProposed changes:")
                print("-" * 50)
                print(changes)
                print("-" * 50)
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'v' to view changes.")
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process safety check requests."""
        changes = kwargs.get("changes", content or "")
        approved = self.approve_changes(changes, kwargs.get("verbose", False))
        return "approved" if approved else "rejected"


class ContextAwarenessNode(BaseAgentNode):
    """Agent for understanding code context and relationships."""
    
    def analyze_context(self, content: Optional[str], path: Optional[str]) -> Dict[str, Any]:
        """Analyze code context for better processing."""
        if not content:
            return {}
        
        context = {}
        
        # Basic analysis
        context["line_count"] = len(content.splitlines())
        context["char_count"] = len(content)
        
        # Extract imports
        import_pattern = r'^(?:from\s+\S+\s+)?import\s+.+$'
        imports = re.findall(import_pattern, content, re.MULTILINE)
        context["imports"] = imports
        
        # Extract functions and classes
        func_pattern = r'^def\s+(\w+)\s*\('
        class_pattern = r'^class\s+(\w+)\s*[\(:]'
        
        functions = re.findall(func_pattern, content, re.MULTILINE)
        classes = re.findall(class_pattern, content, re.MULTILINE)
        
        context["functions"] = functions
        context["classes"] = classes
        context["complexity"] = len(functions) + len(classes) * 2
        
        return context
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process context analysis requests."""
        context = self.analyze_context(content, path)
        return str(context)


class ErrorHandlingNode(BaseAgentNode):
    """Agent for handling errors and providing helpful messages."""
    
    def handle_error(self, error: Exception, command: Optional[str], path: Optional[str], verbose: bool = False) -> str:
        """Handle errors gracefully and provide helpful messages."""
        error_type = type(error).__name__
        error_message = str(error)
        
        if verbose:
            import traceback
            traceback.print_exc()
        
        # Provide specific error messages based on context
        if "API" in error_message or "gemini" in error_message.lower():
            return f"API Error: {error_message}\nPlease check your GEMINI_API_KEY and internet connection."
        elif "FileNotFoundError" in error_type:
            return f"File Error: Could not find file '{path}'. Please check the path."
        elif "PermissionError" in error_type:
            return f"Permission Error: Cannot access file '{path}'. Check file permissions."
        else:
            return f"Error in {command or 'operation'}: {error_message}"
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process error handling requests."""
        error = kwargs.get("error")
        if error:
            return self.handle_error(error, kwargs.get("command"), path, kwargs.get("verbose", False))
        return "No error to handle."
