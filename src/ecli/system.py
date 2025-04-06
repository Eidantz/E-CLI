import platform
import distro
import subprocess
from typing import List

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