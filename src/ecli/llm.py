import logging
import os
from typing import List

import dspy

from ecli.session_memory import SessionMemory

logger = logging.getLogger(__name__)

OLLAMA_DEFAULT_API_BASE = "http://localhost:11434"
OLLAMA_PROVIDER_PREFIXES = ("ollama_chat/", "ollama/")


def setup_llm(llm_model: str) -> None:
    """
    Configures the language model for DSPy.

    Detects whether the model uses an Ollama provider prefix and
    applies the appropriate api_base and api_key settings. For
    non-Ollama providers, the model is configured directly.

    Args:
        llm_model (str): Identifier of the LLM to use, in the
            format "provider/model_name" (e.g.
            "ollama_chat/glm-4.7:cloud", "groq/llama-3.3-70b-versatile").
    """
    if llm_model.startswith(OLLAMA_PROVIDER_PREFIXES):
        api_base = os.getenv(
            "OLLAMA_API_BASE", OLLAMA_DEFAULT_API_BASE
        )
        logger.info(
            "Configuring Ollama LLM: %s at %s", llm_model, api_base
        )
        lm = dspy.LM(llm_model, api_base=api_base, api_key="")
    else:
        logger.info("Configuring LLM: %s", llm_model)
        lm = dspy.LM(llm_model)
    dspy.configure(lm=lm)

class QueryToZshCommand(dspy.Signature):
    """
    Signature for a Zsh command generator.
    Converts a user query to a Zsh command using the language model.
    """
    query: str = dspy.InputField(desc="User query to be converted to a Zsh command")
    userOS: str = dspy.InputField(desc="Operating system of the user")
    session_history: List[dict] = dspy.InputField(desc="Current session's command history")
    commands: List[str] = dspy.OutputField(desc="Generated Zsh commands to execute the query")

def user_query_to_zsh_commands(query: str, session_memory: SessionMemory, user_os: str) -> List[str]:
    """
    Generates a list of Zsh commands from the provided query using the LLM.
    
    Args:
        query (str): User query to be converted to Zsh commands.
        session_memory (SessionMemory): Current session's memory manager.
        user_os (str): User's operating system information.
    
    Returns:
        List[str]: A list of generated Zsh commands.
    """
    agent = dspy.Predict(QueryToZshCommand)
    session_history = session_memory.get_session_history()
    
    response = agent(
        query=query,
        userOS=user_os,
        session_history=session_history
    )
    
    return response.commands 