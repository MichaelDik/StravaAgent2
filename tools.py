# tools.py
from typing import Dict, Any

# 1) The actual Python function the tool will call
def add_numbers(args: Dict[str, Any]) -> str:
    """Add two numbers from the tool arguments."""
    a = args.get("a", 0)
    b = args.get("b", 0)
    return str(a + b)

# 2) The JSON schema definition you give to the OpenAI API
ADD_NUMBERS_TOOL = {
    "type": "function",
    "function": {
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number",
                },
                "b": {
                    "type": "number",
                    "description": "Second number",
                },
            },
            "required": ["a", "b"],
        },
    },
}
