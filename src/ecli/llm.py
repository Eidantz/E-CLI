import dspy
from typing import List
from ecli.session_memory import SessionMemory

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