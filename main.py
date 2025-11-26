"""Entry point for the simple tool-calling CLI."""

from openai import OpenAIwea
from Tools import run_tools, tools


def run_agent() -> None:
    """Prompt the user, run the selected tool, and show the model response."""
    client = OpenAI()

    function_call = None
    context = []
    response = None

    # Processing Loop
    # Exit Condition is an input of q in initial prompt or subsequent ones.
    while function_call is None:
        prompt = input("Please input your prompt: ")
        if prompt == "q":
            break
        context = [
            {
                "role": "user",
                "content": f"Please call {prompt} and tell me the result",
            }
        ]

        response = client.responses.create(
            model="o4-mini",
            input=context,
            tools=tools,
        )

        for item in response.output:
            if item.type == "function_call":
                function_call = item
                break

        if function_call is None:
            print(
                "I'm sorry, I can only call three tools right now: Weather, "
                "Activities, or Date."
            )

    tool_result = run_tools(function_call.name)

    if response is None:
        raise RuntimeError("Response missing after tool selection loop.")

    context += response.output
    context.append(
        {
            "type": "function_call_output",
            "call_id": function_call.call_id,
            "output": str(tool_result),
        }
    )

    second_response = client.responses.create(
        model="o4-mini",
        input=context,
        tools=tools,
    )

    print("\n Final Answer from the model: ")
    print(second_response.output_text)

    conversation_ended = None
    while conversation_ended != "q":
        conversation_ended = input(
            "\n Is there anything else you would like me to do? " "(hit q to exit) "
        )


if __name__ == "__main__":
    run_agent()
