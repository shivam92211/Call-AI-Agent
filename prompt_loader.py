from pathlib import Path

def get_system_prompt():
    """
    Reads and returns the system prompt from the system_prompt.md file.
    If the file doesn't exist, returns a default prompt.
    """
    prompt_file = Path("./system_prompt.md")
    
    if prompt_file.exists():
        with open(prompt_file, "r") as file:
            return file.read().strip()
    else:
        # Default prompt if file doesn't exist
        return "You are a helpful AI assistant. Please provide concise and accurate responses."