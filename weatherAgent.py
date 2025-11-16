"""Agent that can call the helpers implemented in weather.py."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List

from openai import OpenAI
from openai.types.responses import Response, ResponseFunctionToolCall

from weather import get_alerts, get_forecast

client = OpenAI()

ToolArgs = Dict[str, Any]
ToolHandler = Callable[[ToolArgs], str]


@dataclass(frozen=True)
class Tool:
    definition: Dict[str, Any]
    handler: ToolHandler


def _build_tools() -> List[Tool]:
    """Describe the tools for the model and map them to local handlers."""
    return [
        Tool(
            definition={
                "type": "function",
                "name": "get_alerts",
                "description": "Get active National Weather Service alerts for a US state.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "state": {
                            "type": "string",
                            "description": "Two-letter US state code (e.g. CA, NY).",
                        },
                    },
                    "required": ["state"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            handler=lambda args: asyncio.run(get_alerts(args["state"])),
        ),
        Tool(
            definition={
                "type": "function",
                "name": "get_forecast",
                "description": "Get a short-term NWS forecast for a latitude and longitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Latitude for the forecast lookup.",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Longitude for the forecast lookup.",
                        },
                    },
                    "required": ["latitude", "longitude"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            handler=lambda args: asyncio.run(
                get_forecast(args["latitude"], args["longitude"])
            ),
        ),
    ]


TOOLS: List[Tool] = _build_tools()
TOOL_DEFINITIONS = [tool.definition for tool in TOOLS]
HANDLERS: Dict[str, ToolHandler] = {tool.definition["name"]: tool.handler for tool in TOOLS}


def _call_tool(name: str, arguments_json: str) -> str:
    """Execute a model-requested tool call and serialize the output."""
    if name not in HANDLERS:
        return f"Tool '{name}' is not available."

    try:
        arguments = json.loads(arguments_json) if arguments_json else {}
    except json.JSONDecodeError as exc:
        return f"Invalid arguments for {name}: {exc}"

    handler = HANDLERS[name]
    try:
        return handler(arguments)
    except Exception as exc:  # pragma: no cover - defensive logging for runtime use
        return f"Failed to run {name}: {exc}"


def _pending_tool_calls(response: Response) -> Iterable[ResponseFunctionToolCall]:
    return (
        item
        for item in response.output
        if isinstance(item, ResponseFunctionToolCall)
    )


def run_agent(question: str) -> str:
    """Ask the model a question, fulfilling any tool calls it makes."""
    response = client.responses.create(
        model="gpt-5",
        input=[{"role": "user", "content": question}],
        tools=TOOL_DEFINITIONS,
    )

    tool_calls = list(_pending_tool_calls(response))
    while tool_calls:
        tool_outputs = []
        for call in tool_calls:
            result = _call_tool(call.name, call.arguments)
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": result,
                }
            )

        response = client.responses.create(
            model="gpt-5",
            previous_response_id=response.id,
            input=tool_outputs,
        )
        tool_calls = list(_pending_tool_calls(response))

    return response.output_text or "No response text returned."



if __name__ == "__main__":
    print("Please enter Where you would like to see the weather from:")
    inp = input()
    print(run_agent(inp))
