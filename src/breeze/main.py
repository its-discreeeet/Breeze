"""Main entry point and CLI interface for Breeze."""

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from .flow import FlowOrchestrator
from .utils import (
    setup_logging, 
    validate_file_path, 
    get_api_key,
    get_file_type,
    get_file_extension
)



def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="breeze",
        description="""AI-powered code understanding and transformation tool for multiple programming languages.

Supported file types:
  • Programming Languages: Python (.py), JavaScript (.js), TypeScript (.ts), Java (.java), 
    C++ (.cpp), C (.c), C# (.cs), PHP (.php), Ruby (.rb), Go (.go), Rust (.rs)
  • Web Technologies: HTML (.html), CSS (.css), SQL (.sql)
  • Data Formats: JSON (.json), XML (.xml), YAML (.yaml/.yml)
  • Scripts & Config: Shell (.sh), Batch (.bat), PowerShell (.ps1), Markdown (.md)
  • And more text-based files!

Examples:
  breeze doc app.py              # Generate Python docstrings
  breeze summarize main.js       # Summarize JavaScript code
  breeze test utils.java         # Generate Java unit tests
  breeze inspect script.php      # Analyze PHP for bugs
  breeze refactor legacy.cpp     # Refactor C++ code
  breeze annotate api.ts         # Add TypeScript type annotations
  breeze migrate old.py --target "Python 3.12"
  breeze chat                    # Interactive multi-language assistant
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""For more information and examples, visit: https://ai.google.dev/
Set your API key: export GEMINI_API_KEY=your_api_key (Linux/macOS) or setx GEMINI_API_KEY "your_api_key" (Windows)"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", metavar="COMMAND")
    
    # Common arguments for all subcommands
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--output", 
        choices=["console", "in-place", "new-file"],
        default="console",
        help="Output mode: 'console' (display results), 'in-place' (modify original file), 'new-file' (create new file)"
    )
    common_parser.add_argument(
        "--secure", 
        action="store_true",
        help="Require user approval before applying file modifications (recommended for --output in-place)"
    )
    common_parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable detailed logging and processing information"
    )
    
    # Documentation generation command
    doc_parser = subparsers.add_parser(
        "doc", 
        parents=[common_parser],
        help="Generate documentation for functions, classes, and modules",
        description="""Generate language-appropriate documentation:
  • Python: Google-style docstrings
  • JavaScript/TypeScript: JSDoc/TSDoc comments
  • Java: Javadoc comments
  • C++/C: Doxygen comments
  • C#: XML documentation comments
  • PHP: PHPDoc comments
  • Ruby: YARD documentation
  • Go: Go doc comments
  • Rust: Rust doc comments"""
    )
    doc_parser.add_argument(
        "path", 
        help="Path to source code file (supports: .py, .js, .ts, .java, .cpp, .c, .cs, .php, .rb, .go, .rs, etc.)"
    )
    
    # Code summarization command
    summarize_parser = subparsers.add_parser(
        "summarize", 
        parents=[common_parser],
        help="Create concise summaries of code files",
        description="""Generate intelligent summaries including:
  • Main purpose and functionality
  • Key components (classes, functions, modules)
  • Dependencies and imports
  • Notable patterns and design decisions
  • Architecture and structure overview"""
    )
    summarize_parser.add_argument(
        "path", 
        help="Path to any source code or configuration file"
    )
    
    # Test generation command
    test_parser = subparsers.add_parser(
        "test", 
        parents=[common_parser],
        help="Generate comprehensive unit tests",
        description="""Generate tests using appropriate frameworks:
  • Python: pytest
  • JavaScript: Jest
  • TypeScript: Jest with TypeScript
  • Java: JUnit
  • C++: Google Test
  • C#: NUnit/MSTest
  • PHP: PHPUnit
  • Ruby: RSpec
  • Go: Go testing package
  • Rust: Built-in test framework"""
    )
    test_parser.add_argument(
        "path", 
        help="Path to source code file to generate tests for"
    )
    
    # Bug detection and code inspection command
    inspect_parser = subparsers.add_parser(
        "inspect", 
        parents=[common_parser],
        help="Detect bugs, security issues, and code quality problems",
        description="""Comprehensive code analysis including:
  • Logic errors and potential bugs
  • Security vulnerabilities
  • Performance bottlenecks
  • Code smells and maintainability issues
  • Language-specific best practice violations
  • Memory management issues (for C/C++)
  • Type safety concerns"""
    )
    inspect_parser.add_argument(
        "path", 
        help="Path to source code file to analyze"
    )
    
    # Code refactoring command
    refactor_parser = subparsers.add_parser(
        "refactor", 
        parents=[common_parser],
        help="Improve code structure, readability, and maintainability",
        description="""Language-specific refactoring including:
  • Code organization and structure
  • Performance optimizations
  • Modern language feature adoption
  • Design pattern implementation
  • Complexity reduction
  • Following language conventions and best practices"""
    )
    refactor_parser.add_argument(
        "path", 
        help="Path to source code file to refactor"
    )
    
    # Type annotation command
    annotate_parser = subparsers.add_parser(
        "annotate", 
        parents=[common_parser],
        help="Add or improve type annotations/declarations",
        description="""Add appropriate type annotations:
  • Python: Type hints with typing module
  • TypeScript: Interface and type annotations
  • Java: Generic type declarations
  • C++: Template and auto keyword usage
  • C#: Nullable reference types
  • Go: Interface and type declarations
  • Rust: Type annotations and trait bounds
  • PHP: Scalar and return type declarations
  • JavaScript: JSDoc type comments"""
    )
    annotate_parser.add_argument(
        "path", 
        help="Path to source code file (works with statically typed or type-aware languages)"
    )
    
    # Code migration command
    migrate_parser = subparsers.add_parser(
        "migrate", 
        parents=[common_parser],
        help="Migrate code to newer versions, different languages, or frameworks (may not give the best possible results)",
        description="""Migration capabilities:
  • Language version upgrades (Python 2→3, ES5→ES6+, etc.)
  • Cross-language conversion (Python↔JavaScript, etc.)
  • Framework migrations (jQuery→React, etc.)
  • API modernization
  • Dependency updates
  • Platform-specific adaptations"""
    )
    migrate_parser.add_argument(
        "path", 
        help="Path to source code file to migrate"
    )
    migrate_parser.add_argument(
        "--target", 
        required=True,
        help='Migration target (examples: "Python 3.12", "TypeScript", "React", "Java 17", "C++20")',
        metavar="TARGET"
    )
    
    # Interactive chat mode
    chat_parser = subparsers.add_parser(
        "chat", 
        help="Start interactive multi-language code assistant",
        description="""Interactive mode features:
  • Natural language code queries
  • Multi-file analysis
  • Step-by-step guidance
  • Code explanations and tutorials
  • Best practice recommendations
  • Real-time code assistance

Commands in chat mode:
  • doc <file>          - Generate documentation
  • summarize <file>    - Summarize code
  • test <file>         - Generate tests  
  • inspect <file>      - Analyze for bugs
  • refactor <file>     - Improve code
  • annotate <file>     - Add type annotations
  • migrate <file>      - Migrate code
  • help               - Show available commands
  • exit/quit          - Exit chat mode"""
    )
    chat_parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable detailed processing information in chat mode"
    )
    
    # Add examples for better UX
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    return parser


def print_usage_examples():
    """Print comprehensive usage examples."""
    examples = """
🌟 Breeze Usage Examples:

📝 Documentation Generation:
  breeze doc calculator.py                    # Python docstrings
  breeze doc utils.js --output new-file       # JavaScript JSDoc
  breeze doc MathUtils.java -v               # Java Javadoc with verbose output

📊 Code Analysis:
  breeze summarize large_project.py           # Get code overview
  breeze inspect security_check.php           # Find security issues
  breeze inspect memory_manager.cpp --verbose # C++ memory analysis

🧪 Test Generation:
  breeze test api_client.py --output new-file # Generate pytest tests
  breeze test validator.js                    # Generate Jest tests
  breeze test calculator.java                 # Generate JUnit tests

⚡ Code Improvement:
  breeze refactor legacy_code.py --secure     # Refactor with confirmation
  breeze annotate api.ts --output in-place    # Add TypeScript types
  breeze refactor old_script.js -v            # Modern JavaScript patterns

🔄 Code Migration:
  breeze migrate old_app.py --target "Python 3.12"
  breeze migrate jquery_code.js --target "React"
  breeze migrate legacy.java --target "Java 17"
  breeze migrate script.py --target "TypeScript" --output new-file

💬 Interactive Mode:
  breeze chat                                 # Start interactive session
  # In chat mode:
  # > analyze my_project.py for performance issues
  # > convert this Python code to JavaScript
  # > help me refactor this function

🎯 Output Modes:
  --output console     # Display results (default)
  --output in-place    # Modify original file  
  --output new-file    # Create new file

🛡️ Safety Options:
  --secure            # Ask for confirmation before changes
  --verbose           # Show detailed processing info

📁 Supported File Types:
  Programming: .py .js .ts .java .cpp .c .cs .php .rb .go .rs .swift .kt
  Web:         .html .css .scss .sass .sql
  Data:        .json .xml .yaml .yml
  Config:      .sh .bat .ps1 .md .txt
  And more!
"""
    print(examples)


def print_chat_help() -> None:
    """Print comprehensive help for chat mode."""
    help_text = """
💬 Breeze Interactive Chat Mode Help:

🎯 Direct Commands:
  doc <file>                   - Generate documentation
  summarize <file>             - Create code summary  
  test <file>                  - Generate unit tests
  inspect <file>               - Analyze for bugs and issues
  refactor <file>              - Improve code structure
  annotate <file>              - Add type annotations
  migrate <file> --target X    - Migrate to target version/language

🗣️ Natural Language Queries:
  "Analyze security issues in auth.py"
  "Generate tests for my calculator class"
  "Convert this Python code to JavaScript"
  "Refactor this function to be more readable"
  "What are the potential bugs in this C++ code?"
  "Add TypeScript types to my API client"
  "Help me migrate from jQuery to React"

🎛️ Chat Options:
  help                         - Show this help message
  examples                     - Show usage examples
  supported                    - List supported file types
  exit, quit, q               - Exit chat mode

💡 Tips:
  • You can reference files by path: "doc src/utils.py"  
  • Ask questions about code: "What does this function do?"
  • Request explanations: "Explain this algorithm"
  • Get recommendations: "Best practices for this code?"
  • Multiple files: "Compare these two implementations"

🌟 Example Chat Session:
  breeze> doc calculator.py
  breeze> What security issues might this PHP code have?
  breeze> Convert my Python script to TypeScript
  breeze> help me optimize this SQL query
  breeze> exit

🔧 For non-interactive usage, use: breeze <command> <file> [options]
"""
    print(help_text)


def print_supported_languages():
    """Print all supported programming languages and file types."""
    languages = """
🌐 Breeze Supported Languages & File Types:

💻 Programming Languages:
  • Python         (.py)      - Docstrings, pytest, type hints
  • JavaScript     (.js)      - JSDoc, Jest, modern ES features  
  • TypeScript     (.ts)      - TSDoc, type annotations, interfaces
  • Java           (.java)    - Javadoc, JUnit, generics
  • C++            (.cpp/.cc) - Doxygen, Google Test, modern C++
  • C              (.c)       - Doxygen, Unity Test, ANSI/C99/C11
  • C#             (.cs)      - XML docs, NUnit, nullable references  
  • PHP            (.php)     - PHPDoc, PHPUnit, type declarations
  • Ruby           (.rb)      - YARD, RSpec, idiomatic patterns
  • Go             (.go)      - Go docs, testing package, interfaces
  • Rust           (.rs)      - Rust docs, built-in tests, ownership
  • Swift          (.swift)   - Swift docs, XCTest
  • Kotlin         (.kt)      - KDoc, JUnit integration
  • Scala          (.scala)   - ScalaDoc, ScalaTest

🌐 Web Technologies:
  • HTML           (.html)    - Semantic markup, accessibility
  • CSS            (.css)     - Modern CSS, responsive design
  • SCSS/Sass      (.scss)    - Sass features, optimization  
  • SQL            (.sql)     - Query optimization, security

📄 Data & Configuration:
  • JSON           (.json)    - Structure validation, schema
  • XML            (.xml)     - Well-formed validation, XSD
  • YAML           (.yaml)    - Configuration analysis
  • TOML           (.toml)    - Configuration files
  • Markdown       (.md)      - Documentation, formatting

🔧 Scripts & Tools:
  • Shell Scripts  (.sh)      - Bash/Zsh, best practices
  • Batch Files    (.bat)     - Windows batch scripting
  • PowerShell     (.ps1)     - PowerShell scripting
  • Makefile       (Makefile) - Build system optimization

📝 Text Files:
  • Plain Text     (.txt)     - General text analysis
  • Config Files   (.conf)    - Configuration analysis
  • Log Files      (.log)     - Log pattern analysis

🔄 Language-Specific Features:

Python:           PEP compliance, type hints, context managers
JavaScript:       ES6+, async/await, modern patterns  
TypeScript:       Strict typing, interfaces, generics
Java:             OOP patterns, streams, lambda expressions
C++:              RAII, smart pointers, templates
Rust:             Ownership, lifetimes, trait bounds
Go:               Idiomatic patterns, goroutines, interfaces

🚀 Coming Soon:
  • Dart, Flutter  • R, Julia     • Haskell, F#
  • Assembly       • Dockerfile   • Terraform
  • More frameworks and DSLs!
"""
    print(languages)


def handle_chat_mode(verbose: bool = False) -> None:
    """Enhanced chat mode handler with better UX."""
    print("🌬️  Welcome to Breeze Interactive Mode!")
    print("AI-powered multi-language code assistant\n")
    
    if verbose:
        print("🔧 Verbose mode enabled - detailed processing info will be shown")
    
    print("💡 Quick start:")
    print("  • Type 'help' for available commands")
    print("  • Type 'examples' for usage examples") 
    print("  • Type 'supported' for supported languages")
    print("  • Type 'exit' or 'quit' to end session")
    print("  • Ask questions like: 'analyze bugs in my_file.py'")
    print("")
    
    orchestrator = FlowOrchestrator()
    session_count = 0
    
    while True:
        try:
            # Dynamic prompt showing session info
            prompt = f"breeze[{session_count}]> " if session_count > 0 else "breeze> "
            user_input = input(prompt).strip()
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Thanks for using Breeze! Goodbye!")
                break
            elif user_input.lower() == "help":
                print_chat_help()
                continue
            elif user_input.lower() == "examples":
                print_usage_examples()
                continue
            elif user_input.lower() == "supported":
                print_supported_languages()
                continue
            elif not user_input:
                continue
            
            session_count += 1
            
            # Process the chat input
            print("🤖 Processing..." if not verbose else "🤖 Analyzing your request...")
            result = orchestrator.process_chat_input(user_input, verbose=verbose)
            print(f"\n📋 Result:\n{result}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Breeze! Goodbye!")
            break
        except Exception as e:
            session_count += 1
            print(f"\n❌ Error: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            print("💡 Try 'help' for assistance or 'exit' to quit\n")


def handle_chat_mode(verbose: bool = False) -> None:
    """Handle interactive chat mode."""
    if verbose:
        print("Starting Breeze interactive chat session...")
        print("Type 'exit' or 'quit' to end the session.")
        print("Type 'help' for available commands.\n")
    
    orchestrator = FlowOrchestrator()
    
    while True:
        try:
            user_input = input("breeze> ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            elif user_input.lower() == "help":
                print_chat_help()
                continue
            elif not user_input:
                continue
            
            # Process the chat input through the orchestrator
            result = orchestrator.process_chat_input(user_input, verbose=verbose)
            print(result)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_chat_help() -> None:
    """Print help for chat mode."""
    help_text = """
Available commands in chat mode:
- doc <file>: Generate docstrings
- summarize <file>: Summarize code
- test <file>: Generate tests
- inspect <file>: Detect bugs
- refactor <file>: Suggest refactorings
- annotate <file>: Add type annotations
- migrate <file> --target <spec>: Migrate code
- help: Show this help
- exit/quit: Exit chat mode

You can also ask natural language questions about code analysis tasks.
"""
    print(help_text)


def main() -> None:
    """Enhanced main entry point for the Breeze CLI."""
    parser = create_parser()
    
    # Handle no arguments - show help with examples
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n" + "="*60)
        print_usage_examples()
        return
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=getattr(args, "verbose", False))
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        print("\n🔑 Please set your Google AI API key:")
        print("  Windows (CMD):      set GEMINI_API_KEY \"your_key_here\"")
        print("  Windows (PowerShell): $env:GEMINI_API_KEY=\"your_key_here\"")
        print("  Linux/macOS:        export GEMINI_API_KEY=your_key_here")
        print("\n🌐 Get your API key at: https://ai.google.dev/")
        print("📖 For detailed setup instructions, run: breeze --help")
        sys.exit(1)
    
    # Validate API key format (basic check)
    if not api_key.startswith("AIza"):
        print("⚠️  Warning: API key format may be incorrect (should start with 'AIza')")
    
    # Handle chat mode
    if args.command == "chat":
        try:
            handle_chat_mode(verbose=getattr(args, "verbose", False))
        except KeyboardInterrupt:
            print("\n👋 Chat session interrupted. Goodbye!")
        except Exception as e:
            print(f"❌ Chat mode error: {e}")
            if getattr(args, "verbose", False):
                import traceback
                traceback.print_exc()
        return
    
    # Validate file path for non-chat commands
    if hasattr(args, "path"):
        path = args.path
        
        # Check if file exists
        if not Path(path).exists():
            print(f"❌ Error: File '{path}' does not exist.")
            
            # Provide helpful suggestions
            path_obj = Path(path)
            parent_dir = path_obj.parent
            
            if parent_dir.exists():
                # Look for similar files in the directory
                similar_files = []
                try:
                    for file in parent_dir.iterdir():
                        if file.is_file() and path_obj.stem.lower() in file.stem.lower():
                            similar_files.append(str(file))
                except:
                    pass
                
                if similar_files:
                    print("💡 Did you mean one of these files?")
                    for similar_file in similar_files[:5]:  # Show max 5 suggestions
                        print(f"   {similar_file}")
            else:
                print(f"💡 Directory '{parent_dir}' does not exist either.")
            
            print(f"\n📁 Supported file types: .py .js .ts .java .cpp .c .cs .php .rb .go .rs .html .css .sql .json .xml .yaml .md .txt and more")
            sys.exit(1)
        
        # Check if it's a file (not a directory)
        if not Path(path).is_file():
            print(f"❌ Error: '{path}' is not a file.")
            if Path(path).is_dir():
                print("💡 This appears to be a directory. Please specify a file path.")
                # Show some files in the directory
                try:
                    files = [f for f in Path(path).iterdir() if f.is_file()]
                    if files:
                        print("📁 Files in this directory:")
                        for file in files[:10]:  # Show max 10 files
                            print(f"   {file.name}")
                        if len(files) > 10:
                            print(f"   ... and {len(files) - 10} more files")
                except:
                    pass
            sys.exit(1)
        
        # Get file type and show it if verbose
        file_type = get_file_type(path)
        if getattr(args, "verbose", False):
            print(f"📄 Detected file type: {file_type}")
            print(f"📏 File size: {Path(path).stat().st_size} bytes")
    
    # Validate command-specific requirements
    if hasattr(args, "target") and args.command == "migrate":
        if not args.target:
            print("❌ Error: Migration target is required for migrate command.")
            print("💡 Examples:")
            print("   --target \"Python 3.12\"")
            print("   --target \"TypeScript\"") 
            print("   --target \"React\"")
            print("   --target \"Java 17\"")
            sys.exit(1)
    
    # Show operation info if verbose
    if getattr(args, "verbose", False):
        print(f"🚀 Starting {args.command} operation...")
        print(f"📂 File: {getattr(args, 'path', 'N/A')}")
        print(f"📤 Output mode: {getattr(args, 'output', 'console')}")
        if hasattr(args, "target"):
            print(f"🎯 Target: {getattr(args, 'target', 'N/A')}")
        if getattr(args, "secure", False):
            print("🛡️  Secure mode: User approval required for changes")
        print("-" * 50)
    
    # Create flow orchestrator and process command
    orchestrator = FlowOrchestrator()
    
    try:
        # Process the command
        result = orchestrator.process_command(
            command=args.command,
            path=getattr(args, "path", None),
            output_mode=getattr(args, "output", "console"),
            secure=getattr(args, "secure", False),
            verbose=getattr(args, "verbose", False),
            target=getattr(args, "target", None)
        )
        
        # Handle output
        if result:
            # Add separator for better readability in verbose mode
            if getattr(args, "verbose", False):
                print("-" * 50)
                print("📋 Result:")
            
            print(result)
            
            # Show success message for file operations
            if getattr(args, "output", "console") != "console":
                print(f"\n✅ {args.command.title()} operation completed successfully")
        else:
            print("✅ Operation completed successfully (no output generated)")
    
    except KeyboardInterrupt:
        print(f"\n⏹️  {args.command.title()} operation interrupted by user")
        sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        print("💡 Please check the file path and try again")
        sys.exit(1)
    
    except PermissionError as e:
        print(f"❌ Permission Error: {e}")
        print("💡 Try running as administrator or check file permissions")
        sys.exit(1)
    
    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("💡 Please check your internet connection and API key")
        print("🌐 Verify your API key at: https://ai.google.dev/")
        sys.exit(1)
    
    except Exception as e:
        error_type = type(e).__name__
        print(f"❌ {error_type} during {args.command} operation:")
        
        # Show different levels of error detail based on verbose mode
        if getattr(args, "verbose", False):
            print(f"   Full error: {str(e)}")
            print("\n📋 Full traceback:")
            import traceback
            traceback.print_exc()
        else:
            print(f"   {str(e)}")
            print(f"\n💡 Use --verbose for detailed error information")
            print("🔧 Common solutions:")
            
            # Provide error-specific suggestions
            if "API" in str(e) or "gemini" in str(e).lower():
                print("   • Check your GEMINI_API_KEY environment variable")
                print("   • Verify your internet connection")
                print("   • Ensure your API key is valid and active")
            elif "encoding" in str(e).lower() or "decode" in str(e).lower():
                print("   • File might use different encoding")
                print("   • Try converting file to UTF-8")
            elif "timeout" in str(e).lower():
                print("   • File might be too large or complex")
                print("   • Try with a smaller file")
            elif "memory" in str(e).lower():
                print("   • File is too large for available memory")
                print("   • Try processing a smaller file")
            else:
                print("   • Check file path and permissions")
                print("   • Verify file format is supported")
                print("   • Try with --verbose for more details")
        
        sys.exit(1)
    
    # Final verbose output
    if getattr(args, "verbose", False):
        print(f"\n🏁 {args.command.title()} operation finished")


# Additional helper function for the main module
def show_quick_help():
    """Show quick help without full argument parsing."""
    print("🌬️  Breeze - AI-powered multi-language code assistant")
    print("\n🚀 Quick Commands:")
    print("  breeze doc <file>           # Generate documentation")
    print("  breeze summarize <file>     # Summarize code") 
    print("  breeze test <file>          # Generate tests")
    print("  breeze inspect <file>       # Find bugs")
    print("  breeze refactor <file>      # Improve code")
    print("  breeze annotate <file>      # Add types")
    print("  breeze migrate <file> --target X  # Migrate code")
    print("  breeze chat                 # Interactive mode")
    print("\n📖 For detailed help: breeze --help")
    print("💬 For interactive help: breeze chat")


# Enhanced entry point check
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Breeze interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("🔧 Please report this issue if it persists")
        sys.exit(1)



if __name__ == "__main__":
    main()
