"""Main entry point and CLI interface for Breeze."""

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from .flow import FlowOrchestrator
from .utils import setup_logging, validate_file_path, get_api_key


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="breeze",
        description="AI-powered Python code understanding and transformation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Common arguments for all subcommands
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--output", 
        choices=["console", "in-place", "new-file"],
        default="console",
        help="Set output mode"
    )
    common_parser.add_argument(
        "--secure", 
        action="store_true",
        help="Require user approval before applying changes"
    )
    common_parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    # Doc command
    doc_parser = subparsers.add_parser(
        "doc", 
        parents=[common_parser],
        help="Generate docstrings for functions/classes"
    )
    doc_parser.add_argument("path", help="Path to Python file")
    
    # Summarize command
    summarize_parser = subparsers.add_parser(
        "summarize", 
        parents=[common_parser],
        help="Summarize a code file"
    )
    summarize_parser.add_argument("path", help="Path to Python file")
    
    # Test command
    test_parser = subparsers.add_parser(
        "test", 
        parents=[common_parser],
        help="Generate unit tests"
    )
    test_parser.add_argument("path", help="Path to Python file")
    
    # Inspect command
    inspect_parser = subparsers.add_parser(
        "inspect", 
        parents=[common_parser],
        help="Detect bugs and potential issues"
    )
    inspect_parser.add_argument("path", help="Path to Python file")
    
    # Refactor command
    refactor_parser = subparsers.add_parser(
        "refactor", 
        parents=[common_parser],
        help="Suggest and apply code refactorings"
    )
    refactor_parser.add_argument("path", help="Path to Python file")
    
    # Annotate command
    annotate_parser = subparsers.add_parser(
        "annotate", 
        parents=[common_parser],
        help="Add or update type annotations"
    )
    annotate_parser.add_argument("path", help="Path to Python file")
    
    # Migrate command
    migrate_parser = subparsers.add_parser(
        "migrate", 
        parents=[common_parser],
        help="Migrate code to a new version or library"
    )
    migrate_parser.add_argument("path", help="Path to Python file")
    migrate_parser.add_argument(
        "--target", 
        required=True,
        help="Migration target version or library"
    )
    
    # Chat command
    chat_parser = subparsers.add_parser(
        "chat", 
        help="Start an interactive chat session"
    )
    chat_parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser


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
    """Main entry point for the Breeze CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=getattr(args, "verbose", False))
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set your Google AI API key: export GEMINI_API_KEY=your_key_here")
        sys.exit(1)
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle chat mode
    if args.command == "chat":
        handle_chat_mode(verbose=getattr(args, "verbose", False))
        return
    
    # Validate file path for non-chat commands
    if hasattr(args, "path"):
        if not validate_file_path(args.path):
            print(f"Error: File '{args.path}' does not exist or is not a Python file.")
            sys.exit(1)
    
    # Create flow orchestrator and process command
    orchestrator = FlowOrchestrator()
    
    try:
        result = orchestrator.process_command(
            command=args.command,
            path=getattr(args, "path", None),
            output_mode=getattr(args, "output", "console"),
            secure=getattr(args, "secure", False),
            verbose=getattr(args, "verbose", False),
            target=getattr(args, "target", None)
        )
        
        if result:
            print(result)
            
    except Exception as e:
        if getattr(args, "verbose", False):
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
