import dspy

import argparse
import subprocess
from typing import List
import platform
import os
import distro



def setup_llm(llm_model: str):
    """
    Configures the language model.
    
    Args:
        llm_model (str): Identifier of the LLM to use.
    """
    lm = dspy.LM(llm_model)
    dspy.configure(lm=lm)

class QueryToZshCommand(dspy.Signature):
    """
    Signature for a Zsh command generator.
    Converts a user query to a Zsh command using the language model.
    """
    query: str = dspy.InputField(desc="User query to be converted to a Zsh command")
    userOS: str = dspy.OutputField(desc="Operating system of the user")
    commands: List[str] = dspy.OutputField(desc="Generated Zsh commands to execute the query")

def get_user_os() -> str:
    """
    Determines the operating system of the user.
    
    Returns:
        str: The name of the operating system (Linux, Windows, or MacOS).
    """
    # OS name (e.g. 'Windows', 'Linux', 'Darwin' for macOS)
    os_name = platform.system()

    # Detailed OS version
    os_version = platform.version()

    # Distribution info (more useful for Linux)
    if os_name == "Linux":
        try:
            
            distro_name = distro.name()
            distro_version = distro.version()
            return (f"{distro_name} {distro_version}")
        except:
            return "Linux"
    else:
        return(f"{os_name} {platform.release()} (Version: {os_version})")


    
def user_query_to_zsh_commands(query: str) -> List[str]:
    """
    Generates a list of Zsh commands from the provided query using the LLM.
    
    Args:
        query (str): User query to be converted to Zsh commands.
    
    Returns:
        List[str]: A list of generated Zsh commands.
    """
    agent = dspy.Predict(QueryToZshCommand)
    # Set the OS field to the user's OS
    user_os = get_user_os()
    response = agent(query=query, userOS=user_os)
    commands = response.commands
    return commands

def execute_zsh_command(command: str) -> str:
    """
    Executes a Zsh command using the subprocess module.
    
    Args:
        command (str): Zsh command to be executed.
    
    Returns:
        str: Output of the executed command.
    
    Raises:
        Exception: If the command execution fails.
    """
    # Explicitly use Zsh to run the command
    result = subprocess.run(["zsh", "-c", command], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr}")
    return result.stdout

def main():
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
    parser.add_argument("query", type=str,
                        help="User query to be converted to Zsh commands")
    args = parser.parse_args()

    # Default to suggestion mode if no mode flag is provided
    if not args.suggestion and not args.execute:
        args.suggestion = True

    # Set up the chosen LLM
    setup_llm(args.llm)

    # Generate commands from the query
    try:
        commands = user_query_to_zsh_commands(args.query)
    except Exception as err:
        print(f"Error generating commands: {err}")
        return

    # Process the list of commands depending on the mode selected
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
            except Exception as err:
                print(f"Error executing command: {err}")


if __name__ == "__main__":
    main()