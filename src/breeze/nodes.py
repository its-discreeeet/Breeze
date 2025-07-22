"""Agent node implementations for different code processing tasks."""

import re
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from .call_gemini import GeminiAPIProxy
from .utils import get_file_type 

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


def get_file_extension(file_path: str) -> str:
    """Get the file extension."""
    return Path(file_path).suffix.lower()

def get_file_type(file_path: str) -> str:
    """Determine file type based on extension."""
    ext = get_file_extension(file_path)
    
    # Map extensions to file types
    type_mapping = {
        '.py': 'python',
        '.js': 'javascript', 
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'css',
        '.sass': 'css',
        '.sql': 'sql',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.txt': 'text',
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
        '.bat': 'batch',
        '.cmd': 'batch',
        '.ps1': 'powershell'
    }
    
    return type_mapping.get(ext, 'text')



class DocAgentNode(BaseAgentNode):
    """Agent for generating documentation for any programming language."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate documentation for code in any language."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for documentation generation."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific documentation prompts
        doc_styles = {
            'python': 'Google-style docstrings',
            'javascript': 'JSDoc comments',
            'typescript': 'TSDoc comments', 
            'java': 'Javadoc comments',
            'cpp': 'Doxygen comments',
            'c': 'Doxygen comments',
            'csharp': 'XML documentation comments',
            'php': 'PHPDoc comments',
            'ruby': 'YARD documentation',
            'go': 'Go doc comments',
            'rust': 'Rust doc comments',
        }
        
        doc_style = doc_styles.get(file_type, 'appropriate inline comments')
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please generate {doc_style} for all functions, classes, and modules in the following {file_type} code.
Only return the complete code with documentation added, no explanations.

Code:
{content}
"""
        
        if verbose:
            print(f"Generating {doc_style} for {file_type} code...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)



class SummaryAgentNode(BaseAgentNode):
    """Agent for creating code summaries for any programming language."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate a summary of code in any language."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for summarization."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific terminology
        language_terms = {
            'python': 'modules, classes, functions, and methods',
            'javascript': 'modules, classes, functions, and objects',
            'typescript': 'modules, interfaces, classes, functions, and types',
            'java': 'packages, classes, methods, and interfaces',
            'cpp': 'namespaces, classes, functions, and templates',
            'c': 'functions, structures, and header dependencies',
            'csharp': 'namespaces, classes, methods, and properties',
            'php': 'classes, functions, methods, and traits',
            'ruby': 'modules, classes, methods, and mixins',
            'go': 'packages, functions, structs, and interfaces',
            'rust': 'modules, structs, functions, traits, and enums',
            'html': 'elements, structure, and semantic content',
            'css': 'selectors, properties, and styling rules',
            'sql': 'tables, queries, procedures, and schema',
            'json': 'structure, data fields, and nested objects',
            'yaml': 'configuration structure and key-value pairs'
        }
        
        terms = language_terms.get(file_type, 'main components and structure')
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please provide a concise summary of the following {file_type} code/content, including:
- Main purpose and functionality
- Key {terms}
- Dependencies and imports/includes
- Notable patterns, design decisions, or architectural choices
- Any configuration or setup requirements

Content:
{content}
"""
        
        if verbose:
            print(f"Generating summary for {file_type} content...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)



class TestGenerationAgentNode(BaseAgentNode):
    """Agent for generating tests for any programming language."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Generate tests for code in any language."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for test generation."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific test frameworks
        test_frameworks = {
            'python': 'pytest',
            'javascript': 'Jest',
            'typescript': 'Jest with TypeScript',
            'java': 'JUnit',
            'cpp': 'Google Test',
            'c': 'Unity Test Framework',
            'csharp': 'NUnit or MSTest',
            'php': 'PHPUnit',
            'ruby': 'RSpec',
            'go': 'Go testing package',
            'rust': 'Rust built-in test framework',
        }
        
        framework = test_frameworks.get(file_type, 'appropriate testing framework')
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please generate comprehensive unit tests for the following {file_type} code using {framework}.
Include tests for edge cases, error conditions, and main functionality.
Only return the test code, no explanations.

Code:
{content}
"""
        
        if verbose:
            print(f"Generating {framework} tests for {file_type} code...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class BugDetectionAgentNode(BaseAgentNode):
    """Agent for detecting bugs and issues in any programming language."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Analyze code for potential bugs and issues in any language."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for bug detection."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific analysis focuses
        analysis_focuses = {
            'python': 'indentation errors, variable scope, exception handling, type mismatches, import issues',
            'javascript': 'variable hoisting, async/await issues, callback hell, type coercion, DOM manipulation errors',
            'typescript': 'type annotations, interface compliance, generic constraints, module imports',
            'java': 'null pointer exceptions, memory leaks, concurrency issues, exception handling, type safety',
            'cpp': 'memory management, pointer arithmetic, buffer overflows, resource leaks, undefined behavior',
            'c': 'memory leaks, buffer overflows, pointer errors, uninitialized variables, compilation warnings',
            'csharp': 'null reference exceptions, resource disposal, async/await patterns, LINQ usage',
            'php': 'variable scope, SQL injection, XSS vulnerabilities, type juggling, error handling',
            'ruby': 'method visibility, block usage, exception handling, performance bottlenecks',
            'go': 'goroutine leaks, channel deadlocks, error handling patterns, memory usage',
            'rust': 'ownership violations, borrowing errors, lifetime issues, unsafe code blocks',
            'html': 'semantic markup, accessibility issues, missing attributes, nesting violations',
            'css': 'specificity conflicts, responsive design issues, performance problems',
            'sql': 'injection vulnerabilities, index usage, query performance, data integrity',
            'json': 'syntax errors, schema validation, data type inconsistencies',
            'yaml': 'indentation errors, data type issues, reference problems'
        }
        
        focus_areas = analysis_focuses.get(file_type, 'syntax errors, logic issues, and best practice violations')
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please analyze the following {file_type} code/content for potential bugs, issues, and improvements, focusing on:
- {focus_areas}
- Security vulnerabilities
- Performance issues
- Code smells and maintainability concerns
- Best practice violations for {file_type}

Provide specific recommendations for each issue found, including line numbers when possible.

Content:
{content}
"""
        
        if verbose:
            print(f"Analyzing {file_type} content for bugs and issues...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)



class RefactorCodeAgentNode(BaseAgentNode):
    """Agent for code refactoring in any programming language."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Suggest and apply code refactorings for any language."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for refactoring."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific refactoring focuses
        refactoring_focuses = {
            'python': 'PEP 8 compliance, function decomposition, list comprehensions, context managers, type hints',
            'javascript': 'ES6+ features, async/await, arrow functions, destructuring, modules',
            'typescript': 'type safety, interface usage, generic types, strict mode compliance',
            'java': 'OOP principles, design patterns, lambda expressions, stream API, exception handling',
            'cpp': 'modern C++ features, RAII, smart pointers, const correctness, template usage',
            'c': 'function modularity, memory management, error handling, header organization',
            'csharp': 'LINQ usage, async patterns, nullable reference types, property usage, dependency injection',
            'php': 'PSR standards, namespace usage, type declarations, error handling, security practices',
            'ruby': 'idiomatic Ruby patterns, block usage, metaprogramming, gem conventions',
            'go': 'idiomatic Go patterns, error handling, interface usage, goroutine patterns',
            'rust': 'ownership patterns, error handling with Result, trait usage, lifetime optimization',
            'html': 'semantic markup, accessibility improvements, performance optimization',
            'css': 'organization, specificity reduction, responsive design, performance optimization',
            'sql': 'query optimization, index usage, normalization, stored procedure organization'
        }
        
        focus_areas = refactoring_focuses.get(file_type, 'code organization, readability, and best practices')
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please refactor the following {file_type} code to improve:
- Code readability and maintainability
- Performance where applicable
- {focus_areas}
- Following {file_type} best practices and conventions
- Reducing complexity and improving structure

Return the refactored code with improvements applied. Explain major changes made.

Content:
{content}
"""
        
        if verbose:
            print(f"Refactoring {file_type} code...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)



class TypeAnnotationAgentNode(BaseAgentNode):
    """Agent for adding type annotations/declarations in supported languages."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Add or update type annotations for supported languages."""
        verbose = kwargs.get("verbose", False)
        
        if not content:
            return "No content provided for type annotation."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Language-specific type systems
        type_systems = {
            'python': 'Python type hints (typing module, generics, unions, optional)',
            'typescript': 'TypeScript type annotations (interfaces, unions, generics, utility types)',
            'java': 'Java type declarations (generics, wildcards, bounded types)',
            'cpp': 'C++ type specifications (templates, auto keyword, const correctness)',
            'c': 'C type declarations (const qualifiers, function pointers, struct definitions)',
            'csharp': 'C# type annotations (nullable reference types, generics, var inference)',
            'go': 'Go type declarations (interfaces, struct types, type assertions)',
            'rust': 'Rust type annotations (ownership types, lifetimes, trait bounds)',
            'php': 'PHP type declarations (scalar types, return types, property types)',
            'javascript': 'JSDoc type annotations (@param, @returns, @type)'
        }
        
        if file_type not in type_systems:
            return f"Type annotations are not typically applicable to {file_type} files. This command works best with programming languages that support static typing."
        
        type_system = type_systems[file_type]
        
        prompt = f"""
{context}
File type: {file_type.title()}

Please add comprehensive type annotations to the following {file_type} code using {type_system}:
- Function parameters and return types
- Variable types where helpful for clarity
- Generic/template types where applicable
- Import/include necessary type modules or headers
- Follow {file_type} typing best practices

Return the complete code with type annotations added.

Content:
{content}
"""
        
        if verbose:
            print(f"Adding {type_system} to {file_type} code...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)


class MigrationAgentNode(BaseAgentNode):
    """Agent for code migration tasks across languages and versions."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Migrate code to a target version, language, or framework."""
        verbose = kwargs.get("verbose", False)
        target = kwargs.get("target", "")
        
        if not content:
            return "No content provided for migration."
        
        if not target:
            return "No migration target specified."
        
        file_type = get_file_type(path) if path else "text"
        context = self._get_file_context(path)
        
        # Determine migration type
        migration_type = self._determine_migration_type(target, file_type)
        
        prompt = f"""
{context}
File type: {file_type.title()}
Migration target: {target}
Migration type: {migration_type}

Please migrate the following {file_type} code to be compatible with: {target}

Consider:
{self._get_migration_considerations(migration_type, file_type, target)}

Return the migrated code that works with {target}.

Content:
{content}
"""
        
        if verbose:
            print(f"Migrating {file_type} code to {target}...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)
    
    def _determine_migration_type(self, target: str, file_type: str) -> str:
        """Determine the type of migration being requested."""
        target_lower = target.lower()
        
        # Language conversion
        if any(lang in target_lower for lang in ['python', 'javascript', 'java', 'cpp', 'rust', 'go']):
            return "language_conversion"
        
        # Version upgrade
        if any(version in target_lower for version in ['3.', '2.', 'es6', 'es2020', 'c++17', 'c++20']):
            return "version_upgrade"
        
        # Framework migration
        if any(framework in target_lower for framework in ['react', 'vue', 'angular', 'django', 'flask', 'spring']):
            return "framework_migration"
        
        return "general_migration"
    
    def _get_migration_considerations(self, migration_type: str, file_type: str, target: str) -> str:
        """Get specific considerations for the migration type."""
        considerations = {
            "language_conversion": f"""
- Convert {file_type} syntax to target language syntax
- Adapt data types and type systems
- Replace language-specific libraries with equivalents
- Adjust naming conventions and code style
- Handle language-specific features and paradigms""",
            
            "version_upgrade": f"""
- Deprecated features that need updating
- New syntax and language features to adopt
- Library/API changes and replacements
- Performance improvements available in newer versions
- Breaking changes that need attention""",
            
            "framework_migration": f"""
- Framework-specific patterns and conventions
- Component/module structure changes
- API and method name changes
- Configuration and setup differences
- Best practices for the target framework""",
            
            "general_migration": f"""
- Compatibility requirements for {target}
- Syntax and API changes needed
- Library and dependency updates
- Performance and security improvements
- Modern best practices adoption"""
        }
        
        return considerations.get(migration_type, considerations["general_migration"])


class OrchestratorNode(BaseAgentNode):
    """Agent for orchestrating complex workflows and understanding user intent."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process orchestration tasks - required implementation of abstract method."""
        verbose = kwargs.get("verbose", False)
        
        # If content is provided, treat it as a general query
        if content:
            return self.handle_general_query(content, verbose)
        
        # If no content, return default message
        return "Orchestrator ready. Use parse_intent() or handle_general_query() methods for specific tasks."
    
    def parse_intent(self, user_input: str, verbose: bool = False) -> Dict[str, Any]:
        """Parse user intent from natural language input."""
        
        prompt = f"""
Analyze the following user input and extract the intent for a multi-language code analysis tool.
Respond with a JSON object containing:
- command: one of [doc, summarize, test, inspect, refactor, annotate, migrate] or null
- path: file path if mentioned or null
- output_mode: console, in-place, or new-file (default: console)
- secure: true if user wants confirmation (default: false)
- target: migration target if command is migrate

The tool supports: Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust, HTML, CSS, SQL, JSON, YAML, and more.

User input: "{user_input}"
"""
        
        if verbose:
            print("Parsing user intent...")
        
        response = self.gemini.call_gemini(prompt, verbose=verbose)
        
        # Enhanced intent parsing for multiple file types
        intent = {}
        
        # Basic command detection
        commands = ["doc", "summarize", "test", "inspect", "refactor", "annotate", "migrate"]
        for cmd in commands:
            if cmd in user_input.lower():
                intent["command"] = cmd
                break
        
        # Extract file path (support multiple extensions)
        import re
        extensions = r'\.(py|js|ts|java|cpp|c|cs|php|rb|go|rs|swift|kt|scala|html|css|sql|json|xml|yaml|yml|md|txt|sh|bat|ps1)'
        path_match = re.search(rf'(\S+{extensions})', user_input, re.IGNORECASE)
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
You are Breeze, an AI-powered multi-language code assistant. You can analyze and transform code in:
- Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust
- Web technologies: HTML, CSS, SQL
- Data formats: JSON, XML, YAML
- Scripts: Shell, Batch, PowerShell
- Documentation: Markdown

Answer the following query about code analysis, programming best practices, or tool usage:

Query: {query}
"""
        
        if verbose:
            print("Handling general query...")
        
        return self.gemini.call_gemini(prompt, verbose=verbose)




class FileManagementNode(BaseAgentNode):
    """Agent for file management operations across multiple file types."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process file management tasks for any file type."""
        operation = kwargs.get("operation", "read")
        
        if operation == "read":
            return self._read_file(path)
        elif operation == "write":
            return self._write_file(path, content, kwargs.get("backup", True))
        elif operation == "backup":
            return self._backup_file(path)
        elif operation == "validate":
            return self._validate_file(path)
        elif operation == "analyze":
            return self._analyze_file_structure(path)
        else:
            return f"Unknown file operation: {operation}"
    
    def _read_file(self, path: Optional[str]) -> str:
        """Read file content safely for any file type."""
        if not path:
            return "No file path provided."
        
        try:
            file_type = get_file_type(path)
            
            # Handle different encodings based on file type
            encoding = self._get_encoding_for_file_type(file_type)
            
            with open(path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            
            return content
            
        except Exception as e:
            return f"Error reading file: {e}"
    
    def _write_file(self, path: Optional[str], content: Optional[str], backup: bool = True) -> str:
        """Write content to file with optional backup for any file type."""
        if not path or not content:
            return "Missing file path or content."
        
        try:
            file_type = get_file_type(path)
            path_obj = Path(path)
            
            # Create backup if requested and file exists
            if backup and path_obj.exists():
                backup_path = self._create_backup_path(path, file_type)
                path_obj.rename(backup_path)
                print(f"Backup created: {backup_path}")
            
            # Get appropriate encoding for file type
            encoding = self._get_encoding_for_file_type(file_type)
            
            # Ensure directory exists
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with appropriate line endings based on file type
            content = self._normalize_line_endings(content, file_type)
            
            with open(path, 'w', encoding=encoding, newline='') as f:
                f.write(content)
            
            return f"Successfully wrote to {path}"
            
        except Exception as e:
            return f"Error writing file: {e}"
    
    def _backup_file(self, path: Optional[str]) -> str:
        """Create a backup of any file type."""
        if not path:
            return "No file path provided."
        
        try:
            source = Path(path)
            if not source.exists():
                return f"File {path} does not exist."
            
            file_type = get_file_type(path)
            backup_path = self._create_backup_path(path, file_type)
            
            import shutil
            shutil.copy2(source, backup_path)
            return f"Backup created: {backup_path}"
            
        except Exception as e:
            return f"Error creating backup: {e}"
    
    def _validate_file(self, path: Optional[str]) -> str:
        """Validate file based on its type."""
        if not path:
            return "No file path provided."
        
        path_obj = Path(path)
        if not path_obj.exists():
            return f"File {path} does not exist."
        
        file_type = get_file_type(path)
        validation_result = {
            "file_type": file_type,
            "exists": True,
            "readable": path_obj.is_file(),
            "size_bytes": path_obj.stat().st_size if path_obj.exists() else 0,
            "extension": path_obj.suffix
        }
        
        # Additional validation based on file type
        try:
            content = self._read_file(path)
            validation_result.update(self._validate_content_by_type(content, file_type))
        except Exception as e:
            validation_result["content_error"] = str(e)
        
        return str(validation_result)
    
    def _analyze_file_structure(self, path: Optional[str]) -> str:
        """Analyze file structure based on type."""
        if not path:
            return "No file path provided."
        
        try:
            content = self._read_file(path)
            file_type = get_file_type(path)
            
            analysis = {
                "file_type": file_type,
                "line_count": len(content.splitlines()),
                "char_count": len(content),
                "size_kb": round(len(content.encode('utf-8')) / 1024, 2)
            }
            
            # Type-specific analysis
            if file_type in ["python", "javascript", "java", "cpp", "csharp"]:
                analysis["estimated_functions"] = content.count("def ") + content.count("function ") + content.count("void ") + content.count("public ")
            elif file_type == "html":
                analysis["estimated_elements"] = content.count("<") - content.count("</")
            elif file_type == "css":
                analysis["estimated_rules"] = content.count("{")
            elif file_type == "json":
                analysis["estimated_objects"] = content.count("{")
            elif file_type == "sql":
                analysis["estimated_statements"] = len([line for line in content.upper().split('\n') if any(keyword in line for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE'])])
            
            return str(analysis)
            
        except Exception as e:
            return f"Error analyzing file: {e}"
    
    def _get_encoding_for_file_type(self, file_type: str) -> str:
        """Get appropriate encoding for different file types."""
        encoding_map = {
            'python': 'utf-8',
            'javascript': 'utf-8',
            'typescript': 'utf-8',
            'java': 'utf-8',
            'cpp': 'utf-8',
            'c': 'utf-8',
            'csharp': 'utf-8-sig',  # BOM for C#
            'php': 'utf-8',
            'ruby': 'utf-8',
            'go': 'utf-8',
            'rust': 'utf-8',
            'html': 'utf-8',
            'css': 'utf-8',
            'json': 'utf-8',
            'xml': 'utf-8',
            'yaml': 'utf-8',
            'sql': 'utf-8',
            'markdown': 'utf-8',
            'text': 'utf-8',
            'shell': 'utf-8',
            'batch': 'cp1252',  # Windows default
            'powershell': 'utf-8-sig'
        }
        return encoding_map.get(file_type, 'utf-8')
    
    def _create_backup_path(self, original_path: str, file_type: str) -> str:
        """Create appropriate backup path based on file type."""
        from datetime import datetime
        
        path_obj = Path(original_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return str(path_obj.parent / f"{path_obj.stem}.backup_{timestamp}{path_obj.suffix}")
    
    def _normalize_line_endings(self, content: str, file_type: str) -> str:
        """Normalize line endings based on file type and platform."""
        import os
        
        # Some file types have specific line ending preferences
        if file_type == "batch":
            return content.replace('\n', '\r\n')  # Windows batch files need CRLF
        elif file_type in ["shell", "python", "ruby"]:
            return content.replace('\r\n', '\n')  # Unix-style LF
        else:
            return content  # Keep as-is for other types
    
    def _validate_content_by_type(self, content: str, file_type: str) -> Dict[str, Any]:
        """Validate content based on file type."""
        validation = {}
        
        try:
            if file_type == "json":
                import json
                json.loads(content)
                validation["json_valid"] = True
            elif file_type == "yaml":
                try:
                    import yaml
                    yaml.safe_load(content)
                    validation["yaml_valid"] = True
                except ImportError:
                    validation["yaml_validation"] = "PyYAML not available"
            elif file_type == "xml":
                try:
                    import xml.etree.ElementTree as ET
                    ET.fromstring(content)
                    validation["xml_valid"] = True
                except ET.ParseError as e:
                    validation["xml_error"] = str(e)
            elif file_type == "html":
                validation["has_doctype"] = "<!DOCTYPE" in content
                validation["has_html_tags"] = "<html" in content
            elif file_type in ["python", "javascript", "java"]:
                validation["has_syntax_errors"] = self._basic_syntax_check(content, file_type)
                
        except Exception as e:
            validation["validation_error"] = str(e)
        
        return validation
    
    def _basic_syntax_check(self, content: str, file_type: str) -> bool:
        """Basic syntax checking for programming languages."""
        try:
            if file_type == "python":
                import ast
                ast.parse(content)
                return False  # No syntax errors
            elif file_type == "json":
                import json
                json.loads(content)
                return False  # No syntax errors
        except:
            return True  # Has syntax errors
        
        return False  # Assume no errors for other types



class SafetyCheckNode(BaseAgentNode):
    """Agent for safety checks and user approval across different file types."""
    
    def approve_changes(self, changes: str, verbose: bool = False, file_path: Optional[str] = None) -> bool:
        """Request user approval for changes with file-type awareness."""
        file_type = get_file_type(file_path) if file_path else "unknown"
        
        if verbose:
            print(f"\nChanges to be applied to {file_type} file:")
            if file_path:
                print(f"File: {file_path}")
            print("-" * 50)
            print(changes[:1000])  # Show first 1000 chars
            if len(changes) > 1000:
                print(f"\n... ({len(changes) - 1000} more characters)")
            print("-" * 50)
        
        # File-type specific warnings
        warnings = self._get_safety_warnings(file_type, changes, file_path)
        if warnings:
            print("\n⚠️  Safety Warnings:")
            for warning in warnings:
                print(f"  • {warning}")
        
        while True:
            options = "(y)es/(n)o/(v)iew full/(d)iff/(s)ave preview: " if file_path else "(y)es/(n)o/(v)iew full: "
            response = input(f"\nApply these changes? {options}").lower().strip()
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['v', 'view']:
                self._show_full_changes(changes, file_type)
            elif response in ['d', 'diff'] and file_path:
                self._show_diff(changes, file_path)
            elif response in ['s', 'save'] and file_path:
                self._save_preview(changes, file_path, file_type)
            else:
                print(f"Please enter one of: {options}")
    
    def _get_safety_warnings(self, file_type: str, changes: str, file_path: Optional[str]) -> List[str]:
        """Get file-type specific safety warnings."""
        warnings = []
        
        # General warnings
        if file_path and Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            if file_size > 100000:  # 100KB
                warnings.append("Large file detected - consider backing up first")
        
        # File type specific warnings
        type_warnings = {
            'python': self._python_safety_warnings,
            'javascript': self._javascript_safety_warnings,
            'typescript': self._typescript_safety_warnings,
            'java': self._java_safety_warnings,
            'cpp': self._cpp_safety_warnings,
            'csharp': self._csharp_safety_warnings,
            'html': self._html_safety_warnings,
            'css': self._css_safety_warnings,
            'sql': self._sql_safety_warnings,
            'json': self._json_safety_warnings,
            'xml': self._xml_safety_warnings,
            'yaml': self._yaml_safety_warnings
        }
        
        warning_func = type_warnings.get(file_type)
        if warning_func:
            warnings.extend(warning_func(changes))
        
        return warnings
    
    def _python_safety_warnings(self, changes: str) -> List[str]:
        """Python-specific safety warnings."""
        warnings = []
        if 'import os' in changes or 'import sys' in changes:
            warnings.append("System imports detected - review for security implications")
        if 'exec(' in changes or 'eval(' in changes:
            warnings.append("Dynamic code execution detected - potential security risk")
        if '__import__' in changes:
            warnings.append("Dynamic imports detected - review carefully")
        return warnings
    
    def _javascript_safety_warnings(self, changes: str) -> List[str]:
        """JavaScript-specific safety warnings."""
        warnings = []
        if 'eval(' in changes:
            warnings.append("eval() usage detected - potential security risk")
        if 'innerHTML' in changes:
            warnings.append("innerHTML usage - potential XSS vulnerability")
        if 'document.write' in changes:
            warnings.append("document.write detected - consider safer alternatives")
        return warnings
    
    def _sql_safety_warnings(self, changes: str) -> List[str]:
        """SQL-specific safety warnings."""
        warnings = []
        if any(keyword in changes.upper() for keyword in ['DROP', 'DELETE', 'TRUNCATE']):
            warnings.append("Destructive SQL operations detected - use with extreme caution")
        if 'ALTER' in changes.upper():
            warnings.append("Schema modification detected - ensure you have backups")
        return warnings
    
    def _html_safety_warnings(self, changes: str) -> List[str]:
        """HTML-specific safety warnings."""
        warnings = []
        if '<script' in changes.lower():
            warnings.append("Script tags detected - review for security")
        if 'javascript:' in changes.lower():
            warnings.append("JavaScript URLs detected - potential security risk")
        return warnings
    
    def _json_safety_warnings(self, changes: str) -> List[str]:
        """JSON-specific safety warnings."""
        warnings = []
        try:
            import json
            json.loads(changes)
        except:
            warnings.append("Invalid JSON syntax detected")
        return warnings
    
    # Add stubs for other language warning functions
    def _typescript_safety_warnings(self, changes: str) -> List[str]:
        return self._javascript_safety_warnings(changes)  # Similar to JS
    
    def _java_safety_warnings(self, changes: str) -> List[str]:
        warnings = []
        if 'Runtime.getRuntime()' in changes:
            warnings.append("Runtime execution detected - potential security risk")
        return warnings
    
    def _cpp_safety_warnings(self, changes: str) -> List[str]:
        warnings = []
        if any(func in changes for func in ['malloc', 'free', 'delete', 'new']):
            warnings.append("Manual memory management detected - check for leaks")
        if 'system(' in changes:
            warnings.append("System calls detected - security risk")
        return warnings
    
    def _csharp_safety_warnings(self, changes: str) -> List[str]:
        warnings = []
        if 'Process.Start' in changes:
            warnings.append("Process execution detected - security risk")
        return warnings
    
    def _css_safety_warnings(self, changes: str) -> List[str]:
        return []  # CSS is generally safe
    
    def _xml_safety_warnings(self, changes: str) -> List[str]:
        warnings = []
        if '<!ENTITY' in changes:
            warnings.append("XML entities detected - potential XXE vulnerability")
        return warnings
    
    def _yaml_safety_warnings(self, changes: str) -> List[str]:
        warnings = []
        if '!!python' in changes:
            warnings.append("Python object serialization detected - security risk")
        return warnings
    
    def _show_full_changes(self, changes: str, file_type: str) -> None:
        """Show full changes with syntax highlighting if available."""
        print(f"\nFull changes ({file_type}):")
        print("=" * 60)
        print(changes)
        print("=" * 60)
    
    def _show_diff(self, changes: str, file_path: str) -> None:
        """Show diff between original and proposed changes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()
            
            print("\nDiff preview:")
            print("-" * 40)
            
            # Simple line-by-line diff
            original_lines = original.splitlines()
            new_lines = changes.splitlines()
            
            for i, (old_line, new_line) in enumerate(zip(original_lines, new_lines)):
                if old_line != new_line:
                    print(f"Line {i+1}:")
                    print(f"  - {old_line}")
                    print(f"  + {new_line}")
            
            print("-" * 40)
            
        except Exception as e:
            print(f"Could not generate diff: {e}")
    
    def _save_preview(self, changes: str, file_path: str, file_type: str) -> None:
        """Save a preview of the changes."""
        try:
            preview_path = f"{file_path}.preview"
            with open(preview_path, 'w', encoding='utf-8') as f:
                f.write(changes)
            print(f"Preview saved to: {preview_path}")
        except Exception as e:
            print(f"Could not save preview: {e}")
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process safety check requests."""
        changes = kwargs.get("changes", content or "")
        approved = self.approve_changes(changes, kwargs.get("verbose", False), path)
        return "approved" if approved else "rejected"



class ContextAwarenessNode(BaseAgentNode):
    """Agent for understanding code context and relationships across languages."""
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process context analysis requests - required implementation of abstract method."""
        verbose = kwargs.get("verbose", False)
        
        if verbose:
            print("Analyzing code context...")
        
        # Analyze the context
        context = self.analyze_context(content, path)
        
        # Return formatted context information
        if context:
            result = "📋 Context Analysis:\n"
            result += f"File type: {context.get('file_type', 'unknown')}\n"
            result += f"Lines: {context.get('line_count', 0)}\n"
            result += f"Characters: {context.get('char_count', 0)}\n"
            
            if context.get('functions'):
                result += f"Functions: {', '.join(context['functions'])}\n"
            if context.get('classes'):
                result += f"Classes: {', '.join(context['classes'])}\n"
            if context.get('imports'):
                result += f"Imports: {len(context['imports'])} found\n"
            
            return result
        else:
            return "No context information available."
    
    def analyze_context(self, content: Optional[str], path: Optional[str]) -> Dict[str, Any]:
        """Analyze code context for better processing across different languages."""
        if not content:
            return {}
        
        file_type = get_file_type(path) if path else "text"
        context = {
            "file_type": file_type,
            "line_count": len(content.splitlines()),
            "char_count": len(content)
        }
        
        # Language-specific analysis
        if file_type == "python":
            context.update(self._analyze_python_context(content))
        elif file_type == "javascript":
            context.update(self._analyze_javascript_context(content))
        elif file_type == "java":
            context.update(self._analyze_java_context(content))
        elif file_type == "cpp":
            context.update(self._analyze_cpp_context(content))
        elif file_type == "html":
            context.update(self._analyze_html_context(content))
        elif file_type == "css":
            context.update(self._analyze_css_context(content))
        elif file_type == "sql":
            context.update(self._analyze_sql_context(content))
        else:
            context.update(self._analyze_generic_context(content))
        
        return context
    
    def _analyze_python_context(self, content: str) -> Dict[str, Any]:
        """Analyze Python-specific context."""
        import re
        
        imports = re.findall(r'^(?:from\s+\S+\s+)?import\s+.+$', content, re.MULTILINE)
        functions = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)
        classes = re.findall(r'^class\s+(\w+)\s*[\(:]', content, re.MULTILINE)
        
        return {
            "imports": imports,
            "functions": functions,
            "classes": classes,
            "complexity": len(functions) + len(classes) * 2
        }
    
    def _analyze_javascript_context(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript-specific context."""
        import re
        
        imports = re.findall(r'import\s+.*?from\s+["\'].+?["\']', content)
        functions = re.findall(r'(?:function\s+(\w+)|const\s+(\w+)\s*=.*?=>)', content)
        classes = re.findall(r'class\s+(\w+)', content)
        
        return {
            "imports": imports,
            "functions": [f[0] or f[1] for f in functions],
            "classes": classes,
            "has_async": "async" in content,
            "has_promises": "Promise" in content
        }
    
    def _analyze_java_context(self, content: str) -> Dict[str, Any]:
        """Analyze Java-specific context."""
        import re
        
        imports = re.findall(r'import\s+[\w.]+;', content)
        classes = re.findall(r'(?:public\s+)?class\s+(\w+)', content)
        methods = re.findall(r'(?:public|private|protected)?\s+\w+\s+(\w+)\s*\(', content)
        
        return {
            "imports": imports,
            "classes": classes,
            "methods": methods,
            "has_main": "public static void main" in content
        }
    
    def _analyze_cpp_context(self, content: str) -> Dict[str, Any]:
        """Analyze C++-specific context."""
        import re
        
        includes = re.findall(r'#include\s*[<"][^>"]+[>"]', content)
        functions = re.findall(r'\w+\s+(\w+)\s*\([^{]*\)\s*{', content)
        classes = re.findall(r'class\s+(\w+)', content)
        
        return {
            "includes": includes,
            "functions": functions,
            "classes": classes,
            "has_templates": "template" in content,
            "has_namespaces": "namespace" in content
        }
    
    def _analyze_html_context(self, content: str) -> Dict[str, Any]:
        """Analyze HTML-specific context."""
        import re
        
        tags = re.findall(r'<(\w+)', content)
        unique_tags = list(set(tags))
        
        return {
            "tags": unique_tags,
            "tag_count": len(tags),
            "has_doctype": "<!DOCTYPE" in content,
            "has_scripts": "script" in unique_tags,
            "has_styles": "style" in unique_tags
        }
    
    def _analyze_css_context(self, content: str) -> Dict[str, Any]:
        """Analyze CSS-specific context."""
        import re
        
        selectors = re.findall(r'([.#]?\w+(?:\s*[>+~]\s*\w+)*)\s*{', content)
        properties = re.findall(r'(\w+-?\w*)\s*:', content)
        
        return {
            "selectors": selectors,
            "properties": list(set(properties)),
            "has_media_queries": "@media" in content,
            "has_animations": "@keyframes" in content
        }
    
    def _analyze_sql_context(self, content: str) -> Dict[str, Any]:
        """Analyze SQL-specific context."""
        import re
        
        tables = re.findall(r'FROM\s+(\w+)', content, re.IGNORECASE)
        keywords = re.findall(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b', content, re.IGNORECASE)
        
        return {
            "tables": list(set(tables)),
            "keywords": list(set(keywords)),
            "complexity": len(keywords)
        }
    
    def _analyze_generic_context(self, content: str) -> Dict[str, Any]:
        """Analyze generic file context."""
        words = content.split()
        unique_words = len(set(words))
        
        return {
            "word_count": len(words),
            "unique_words": unique_words,
            "complexity": min(10, unique_words // 100)  # Simple complexity metric
        }




class ErrorHandlingNode(BaseAgentNode):
    """Agent for handling errors across different file types and operations."""
    
    def handle_error(self, error: Exception, command: Optional[str], path: Optional[str], verbose: bool = False) -> str:
        """Handle errors gracefully with file-type awareness."""
        error_type = type(error).__name__
        error_message = str(error)
        file_type = get_file_type(path) if path else "unknown"
        
        if verbose:
            import traceback
            print("\nDetailed error information:")
            traceback.print_exc()
        
        # File-type specific error handling
        context_info = self._get_error_context(error_type, error_message, file_type, command, path)
        
        # Generate helpful error message
        error_report = self._format_error_message(error_type, error_message, command, path, file_type, context_info)
        
        # Add suggestions based on error type and file type
        suggestions = self._get_error_suggestions(error_type, error_message, file_type, command)
        
        if suggestions:
            error_report += "\n\n💡 Suggestions:"
            for suggestion in suggestions:
                error_report += f"\n  • {suggestion}"
        
        return error_report
    
    def _get_error_context(self, error_type: str, error_message: str, file_type: str, command: Optional[str], path: Optional[str]) -> Dict[str, Any]:
        """Get contextual information about the error."""
        context = {
            "file_type": file_type,
            "command": command,
            "has_file": path is not None
        }
        
        # Add file-specific context if file exists
        if path and Path(path).exists():
            try:
                stat_info = Path(path).stat()
                context.update({
                    "file_size": stat_info.st_size,
                    "file_readable": os.access(path, os.R_OK),
                    "file_writable": os.access(path, os.W_OK)
                })
            except:
                pass
        
        return context
    
    def _format_error_message(self, error_type: str, error_message: str, command: Optional[str], path: Optional[str], file_type: str, context: Dict[str, Any]) -> str:
        """Format a comprehensive error message."""
        
        # Base error message
        message = f"❌ Error in {command or 'operation'}"
        
        if path:
            message += f" for {file_type} file: {Path(path).name}"
        
        message += f"\n\n🔍 Error Details:"
        message += f"\n  Type: {error_type}"
        message += f"\n  Message: {error_message}"
        
        # Add file context if available
        if context.get("has_file") and path:
            message += f"\n  File: {path}"
            if context.get("file_size"):
                message += f"\n  File size: {context['file_size']} bytes"
        
        # Add specific error explanations
        explanation = self._get_error_explanation(error_type, error_message, file_type)
        if explanation:
            message += f"\n\n📝 What this means:\n  {explanation}"
        
        return message
    
    def _get_error_explanation(self, error_type: str, error_message: str, file_type: str) -> Optional[str]:
        """Get human-readable explanation for common errors."""
        
        explanations = {
            "FileNotFoundError": f"The {file_type} file could not be found at the specified location.",
            "PermissionError": f"Insufficient permissions to access the {file_type} file.",
            "UnicodeDecodeError": f"The {file_type} file contains characters that cannot be decoded with the current encoding.",
            "JSONDecodeError": "The JSON file contains invalid syntax and cannot be parsed.",
            "SyntaxError": f"The {file_type} code contains syntax errors that prevent processing.",
            "ImportError": "Required Python packages are not installed or cannot be imported.",
            "ConnectionError": "Cannot connect to the Gemini API - check your internet connection.",
            "KeyError": "Missing required configuration or API key.",
            "ValueError": f"Invalid value or parameter provided for {file_type} processing.",
            "TimeoutError": "The operation timed out - the file might be too large or complex.",
            "MemoryError": "Not enough memory to process the file - try with a smaller file."
        }
        
        return explanations.get(error_type)
    
    def _get_error_suggestions(self, error_type: str, error_message: str, file_type: str, command: Optional[str]) -> List[str]:
        """Get suggestions for fixing the error."""
        suggestions = []
        
        # General suggestions based on error type
        if error_type == "FileNotFoundError":
            suggestions.extend([
                "Check if the file path is correct",
                "Ensure the file exists in the specified location",
                f"Verify the file has a .{file_type} extension if expected"
            ])
        
        elif error_type == "PermissionError":
            suggestions.extend([
                "Run the command as administrator/sudo",
                "Check file permissions and ownership",
                "Ensure the file is not open in another program"
            ])
        
        elif error_type == "UnicodeDecodeError":
            suggestions.extend([
                f"The {file_type} file might use a different encoding",
                "Try opening the file in a text editor to check encoding",
                "Consider converting the file to UTF-8 encoding"
            ])
        
        elif "API" in error_message or "gemini" in error_message.lower():
            suggestions.extend([
                "Check your GEMINI_API_KEY environment variable",
                "Verify your internet connection",
                "Ensure your API key is valid and active",
                "Check if you've exceeded API rate limits"
            ])
        
        elif error_type == "ImportError":
            suggestions.extend([
                "Install required packages: pip install google-generativeai",
                "Check your Python environment and virtual environment",
                "Ensure all dependencies are properly installed"
            ])
        
        # File-type specific suggestions
        file_suggestions = self._get_file_type_suggestions(error_type, error_message, file_type, command)
        suggestions.extend(file_suggestions)
        
        return suggestions
    
    def _get_file_type_suggestions(self, error_type: str, error_message: str, file_type: str, command: Optional[str]) -> List[str]:
        """Get file-type specific suggestions."""
        suggestions = []
        
        if file_type == "python" and error_type == "SyntaxError":
            suggestions.extend([
                "Check for proper indentation",
                "Verify parentheses and brackets are balanced",
                "Ensure proper Python syntax"
            ])
        
        elif file_type == "javascript" and error_type == "SyntaxError":
            suggestions.extend([
                "Check for missing semicolons",
                "Verify curly braces are balanced",
                "Ensure proper JavaScript syntax"
            ])
        
        elif file_type == "json" and "JSON" in error_type:
            suggestions.extend([
                "Validate JSON syntax online",
                "Check for trailing commas",
                "Ensure strings are properly quoted"
            ])
        
        elif file_type == "yaml" and error_type == "ScannerError":
            suggestions.extend([
                "Check YAML indentation (use spaces, not tabs)",
                "Verify proper YAML syntax",
                "Ensure colons have spaces after them"
            ])
        
        elif file_type == "xml" and "XML" in error_message:
            suggestions.extend([
                "Check for unclosed tags",
                "Verify proper XML structure",
                "Ensure special characters are properly escaped"
            ])
        
        # Command-specific suggestions
        if command == "test" and file_type in ["python", "javascript", "java"]:
            suggestions.append(f"Ensure your {file_type} code has testable functions/methods")
        
        elif command == "doc" and file_type == "python":
            suggestions.append("Ensure functions and classes are properly defined")
        
        return suggestions
    
    def process(self, content: Optional[str], path: Optional[str], **kwargs) -> str:
        """Process error handling requests."""
        error = kwargs.get("error")
        if error:
            return self.handle_error(
                error, 
                kwargs.get("command"), 
                path, 
                kwargs.get("verbose", False)
            )
        return "No error to handle."
    
    def log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """Log error for debugging purposes."""
        import logging
        import json
        
        logger = logging.getLogger("breeze.errors")
        
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": str(datetime.now())
        }
        
        logger.error(f"Breeze error: {json.dumps(error_info, indent=2)}")
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for debugging."""
        # This could be implemented to track error patterns
        # for improving the tool over time
        return {
            "total_errors": 0,
            "error_types": {},
            "file_types_with_errors": {},
            "commands_with_errors": {}
        }
