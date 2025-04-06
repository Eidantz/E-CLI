import argparse
from pathlib import Path
from .session_memory import SessionMemory
from .llm import setup_llm, user_query_to_zsh_commands
from .system import get_user_os, execute_zsh_command

# Version information
__version__ = "2.0.0"

def main():
    # Clean up old session files at startup
    SessionMemory.cleanup_old_sessions()
    
    parser = argparse.ArgumentParser(description="LLM Command Assistant for Zsh")
    # Optional LLM flag; defaults to groq if not provided
    parser.add_argument("--llm", type=str, default="groq/llama-3.3-70b-specdec",
                        help="LLM model identifier to use (default: groq/llama-3.3-70b-specdec)")
    # Mutually exclusive modes: suggestion or execute
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--suggestion", action="store_true",
                       help="Return the suggested commands without executing them")
    group.add_argument("-e", "--execute", action="store_true",
                       help="Execute the suggested commands")
    parser.add_argument("--clear-memory", action="store_true",
                       help="Clear all session memory files")
    parser.add_argument("-v", "--version", action="version",
                       version=f"%(prog)s {__version__}",
                       help="Show program's version number and exit")
    parser.add_argument("query", type=str, nargs="?",
                       help="User query to be converted to Zsh commands")
    args = parser.parse_args()

    # Handle --clear-memory flag
    if args.clear_memory:
        memory_dir = Path("ecli_memory")
        if memory_dir.exists():
            for session_file in memory_dir.glob("session_*.json"):
                try:
                    session_file.unlink()
                except Exception as e:
                    print(f"Error deleting {session_file}: {e}")
            print("All session memory files have been cleared.")
            return

    # Default to suggestion mode if no mode flag is provided
    if not args.suggestion and not args.execute:
        args.suggestion = True

    # Check if query is provided when not clearing memory
    if not args.query and not args.clear_memory:
        parser.error("the following arguments are required: query")

    # Initialize session memory
    session_memory = SessionMemory()

    # Set up the chosen LLM
    setup_llm(args.llm)

    try:
        user_os = get_user_os()
        commands = user_query_to_zsh_commands(args.query, session_memory, user_os)
        
        if args.suggestion:
            print("Suggested commands:")
            for cmd in commands:
                print(cmd)
        elif args.execute:
            print("Executing commands:")
            for cmd in commands:
                print(f"Executing: {cmd}")
                try:
                    output = execute_zsh_command(cmd)
                    print("Command Output:")
                    print(output)
                    # Save the output to session memory
                    session_memory.add_interaction(args.query, [cmd], output)
                except Exception as err:
                    print(f"Error executing command: {err}")

    except Exception as err:
        print(f"Error generating commands: {err}")
        return

if __name__ == "__main__":
    main()