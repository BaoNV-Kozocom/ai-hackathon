# core/gpt.py

import json
from config import config
from tools import functions
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)


def ask(prompt: str) -> str:
    messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    def handle_tool_call(tool_call):
        name = tool_call.function.name
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON arguments"}

        match name:
            case "search_info":
                 return functions.search_info(function_args["query"])

            case "read_error_file":
                return functions.read_error_file(
                    function_args["file_path"],
                    function_args["line_start"],
                    function_args["line_end"]
                )
            case "execute_command":
                return functions.execute_command(function_args["command"])
            case _:
                return {"status": "error", "message": f"Tool {name} không được hỗ trợ"}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=config.TOOLS,
        tool_choice="auto",
        stream=False,
    )

    response_message = response.choices[0].message

    while response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            tool_response = handle_tool_call(tool_call)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": str(tool_response),
                }
            )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=config.TOOLS,
            tool_choice="auto",
            stream=False,
        )
        response_message = response.choices[0].message

    return response_message.content
