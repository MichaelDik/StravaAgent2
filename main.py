# main.py
from openai import OpenAI
from tools import add_numbers, ADD_NUMBERS_TOOL  # <- import from tools.py

client = OpenAI()

def handle_tool_call(name: str, arguments: dict) -> str:
    """Route tool calls from the model to your local Python functions."""
    if name == "add_numbers":
        return add_numbers(arguments)

    # If you add more tools later, extend this if/elif block:
    # elif name == "other_tool":
    #     return other_tool(arguments)

    raise ValueError(f"Unknown tool: {name}")

def run_agent(user_input: str) -> str:
    # 1) Ask the model; let it decide whether to call a tool
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": user_input}],
        tools=[ADD_NUMBERS_TOOL],  # <- imported tool definition
    )

    msg = response.output[0].content[0]

    # 2) If the model called a tool, execute it locally
    if msg.type == "tool_call":
        tool_call = msg  # depending on your exact SDK shape, adapt this
        tool_name = tool_call.name
        tool_args = tool_call.arguments  # already parsed dict in new SDKs

        tool_result = handle_tool_call(tool_name, tool_args)

        # 3) Send tool result back to the model if you want a final answer
        followup = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "user", "content": user_input},
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result,
                },
            ],
        )
        return followup.output_text

    # If no tool call, just return the model’s reply
    return response.output_text

if __name__ == "__main__":
    print(run_agent("Add 3 and 5 for me."))
