import json
import time
import os
import psutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

class SessionMemory:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get installation directory from .env
        install_dir = os.getenv('INSTALLATION_DIR')
        if not install_dir:
            raise ValueError("INSTALLATION_DIR not found in .env file. Please run the installation script again.")
            
        # Create ecli_memory directory in installation folder
        self.memory_dir = Path(install_dir) / "ecli_memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Get the parent terminal's PID (shell PID)
        self.terminal_pid = os.getppid()
        
        # Use terminal PID as session identifier
        self.session_file = self.memory_dir / f"session_{self.terminal_pid}.json"
        
        # Load existing session or create new one
        self.history = self._load_or_create_session()

    def _load_or_create_session(self) -> List[Dict[str, Any]]:
        # Check if session file exists and the terminal is still running
        if self.session_file.exists():
            try:
                # Check if the terminal process still exists
                psutil.Process(self.terminal_pid)
                # If we reach here, the terminal is still running
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            except (psutil.NoSuchProcess, json.JSONDecodeError):
                # Terminal no longer exists or corrupted file
                # Start fresh session
                pass
        
        # New session or invalid old session
        return []

    def add_interaction(self, query: str, commands: List[str], output: Optional[str] = None) -> None:
        interaction = {
            "timestamp": time.time(),
            "query": query,
            "commands": commands,
            "output": output
        }
        self.history.append(interaction)
        
        # Limit history to 10 commands
        if len(self.history) > 10:
            self.history.pop(0)  # Remove the oldest entry
            
        self._save_history()

    def get_session_history(self) -> List[Dict[str, Any]]:
        return self.history

    def _save_history(self) -> None:
        with open(self.session_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    @classmethod
    def cleanup_old_sessions(cls) -> None:
        """Clean up session files for terminals that no longer exist"""
        # Load environment variables
        load_dotenv()
        
        # Get installation directory from .env
        install_dir = os.getenv('INSTALLATION_DIR')
        if not install_dir:
            raise ValueError("INSTALLATION_DIR not found in .env file. Please run the installation script again.")
            
        memory_dir = Path(install_dir) / "ecli_memory"
        if not memory_dir.exists():
            return

        for session_file in memory_dir.glob("session_*.json"):
            try:
                # Extract PID from filename
                pid = int(session_file.stem.split('_')[1])
                # Check if process exists
                psutil.Process(pid)
            except (ValueError, psutil.NoSuchProcess):
                # Invalid PID or process no longer exists
                session_file.unlink()  # Delete the file 