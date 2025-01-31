#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify,
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import httpx
import traceback

from src.computer_use_tools import ToolResult
from datetime import datetime, timedelta
from anthropic import RateLimitError
from enum import StrEnum
from typing import cast
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from ..constants import BASE_DIR, HR

console = Console()

from anthropic.types.beta import (
    BetaContentBlockParam,
)

CONFIG_DIR = "./client/config"
DEFAULT_PROMPT_MODE = 'file'
if os.getenv("ENVIRONMENT") == "container":
    INPUT_FILE_PATH = os.path.join(BASE_DIR, "..", "tests", "e2e.yml")
else:
    INPUT_FILE_PATH = os.path.join(BASE_DIR, "..", "..", "frontend", "tests", "e2e.yml")

class Sender(StrEnum):
    USER = "user"
    BOT = "assistant"
    TOOL = "tool"
        
session = {
    "messages": [],
    "chat_input": "",
    "only_n_most_recent_images": 10,
    "responses": {}, "tools": {}, "write": [], "error": [],
    "hide_images": False
}

def format_chat_input(user_input):
    formated_input = {
        "role": "user",
        "content": user_input
    }
    return formated_input

""" def _render_message(sender, message):
    print(f"response is reported") """

def _render_message(
    sender: Sender,
    message: str | BetaContentBlockParam | ToolResult,
):
    """Convert input from the user or output from the agent to a streamlit message."""
    # streamlit's hotreloading breaks isinstance checks, so we need to check for class names
    is_tool_result = not isinstance(message, str | dict)
    if not message or (
        is_tool_result
        and session["hide_images"]
        and not hasattr(message, "error")
        and not hasattr(message, "output")
    ):
        return
    #print(HR)
    if is_tool_result:
        message = cast(ToolResult, message)
        if message.output:
            if message.__class__.__name__ == "CLIResult":
                syntax = Syntax(message.output, "python", theme="monokai", line_numbers=True)
                console.print(syntax)
            elif message.base64_image and not session["hide_images"]:
                console.print(message.output, style="bold blue")
            else:
                console.print(Markdown(message.output))
        if message.error:
            console.print(message.error, style="bold red")
    elif isinstance(message, dict):
        if message["type"] == "text":
            console.print(message["text"])
        elif message["type"] == "tool_use":
            syntax = Syntax(f'Tool Use: {message["name"]}\nInput: {message["input"]}', "python", theme="monokai", line_numbers=True)
            console.print(syntax)
        else:
            # only expected return types are text and tool_use
            raise Exception(f'Unexpected response type {message["type"]}')
    else:
        console.print(Markdown(message))


def _tool_output_callback(
    tool_output: ToolResult, tool_id: str, tool_state: dict[str, ToolResult]
):
    """Handle a tool output by storing it to state and rendering it."""
    tool_state[tool_id] = tool_output
    _render_message(Sender.TOOL, tool_output)


def _render_error(error: Exception):
    if isinstance(error, RateLimitError):
        body = "You have been rate limited."
        if retry_after := error.response.headers.get("retry-after"):
            body += f" **Retry after {str(timedelta(seconds=int(retry_after)))} (HH:MM:SS).** See our API [documentation](https://docs.anthropic.com/en/api/rate-limits) for more details."
        body += f"\n\n{error.message}"
    else:
        body = str(error)
        body += "\n\n**Traceback:**"
        lines = "\n".join(traceback.format_exception(error))
        body += f"\n\n```{lines}```"
    save_to_storage(f"error_{datetime.now().timestamp()}.md", body)
    session["error"].append(f"**{error.__class__.__name__}**\n\n{body}", icon=":material/error:")

def save_to_storage(filename: str, data: str) -> None:
    """Save data to a file in the storage directory."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        file_path = CONFIG_DIR / filename
        file_path.write_text(data)
        # Ensure only user can read/write the file
        file_path.chmod(0o600)
    except Exception as e:
        session['write'].append(f"Debug: Error saving {filename}: {e}")

def _render_api_response(
    request: httpx.Request,
    response: httpx.Response | object | None,
    response_id: str,
):
    """Render an API response to a streamlit tab"""
    print(f"Request/Response ({response_id})")
    newline = "\n\n"
    print(
        f"`{request.method} {request.url}`{newline}{newline.join(f'`{k}: {v}`' for k, v in request.headers.items())}"
    )

    print(f"`{response.status_code}`{newline}{newline.join(f'`{k}: {v}`' for k, v in response.headers.items())}"
        )

def load_interactive_instructions():
    print("Type in test commands for frontend E2E with Natural Language! \ne.g. Go to aws.com, there is a Sign In button. Verify that the button exists or not")
    print("Type 'exit' to quit the interactive mode.")
    
def _intro():
    print(f"{HR}\nWelcome to the test client for FANTAS!")
    print(f"Supported by Claude LLM 'Computer Use'!\n{HR}Use CMD + C to quit.\n")