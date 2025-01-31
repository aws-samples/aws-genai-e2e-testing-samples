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
from functools import partial

from dotenv import load_dotenv
from rich.console import Console
import yaml

from ..constants import HR, SUCCESS_INDICATOR
from ..loop import sampling_loop
from .utils import (
    DEFAULT_PROMPT_MODE,
    INPUT_FILE_PATH,
    Sender,
    _render_message,
    _tool_output_callback,
    format_chat_input,
    load_interactive_instructions,
    session
)
from anthropic.types.beta import (
    BetaMessageParam
)

# Initialize Console instance
console = Console()

load_dotenv()

http_logs = []  

def get_prompt_mode():
    prompt_mode = os.getenv('PROMPT_MODE')
    if not prompt_mode:
        print(f"PROMPT_MODE environment variable is not set.\nUsing default value: {DEFAULT_PROMPT_MODE}")
        return DEFAULT_PROMPT_MODE
    return prompt_mode
    
async def interactive_prompt():
    load_interactive_instructions()
    while True:
        user_input = input("Enter test commands (or 'exit' to quit): ").strip()
        
        if user_input.lower() == "exit":
            print("Exiting the client.")
            break
        elif user_input:
            session["chat_input"] = format_chat_input(user_input)
            session["messages"].append(session["chat_input"])
            # call_api(user_input)
            await sampling_loop(
                system_prompt_suffix="",
                messages=[session["chat_input"]],
                output_callback=partial(_render_message, Sender.BOT),
                tool_output_callback=partial(
                    _tool_output_callback, tool_state=session["tools"]
                ),
                only_n_most_recent_images=session["only_n_most_recent_images"]
            )
        else:
            print("Please enter some text or type 'exit' to quit.")

async def process_file():
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"File not found: {INPUT_FILE_PATH}")
        return
    print(f"Loading test file from {INPUT_FILE_PATH}")
    tests = load_tests(INPUT_FILE_PATH)
    print("File loaded successfully.")
    print(f"{HR}\nTESTS\n{HR}")

    for test in tests:
        console.print(f"Running test: '{test['name']}'", style="bold blue")
        user_input = test["prompt"]
        session["chat_input"] = format_chat_input(user_input)
        session["messages"].append(session["chat_input"])
        # call_api(user_input)
        response_list = await sampling_loop(
            system_prompt_suffix="",
            messages=[session["chat_input"]],
            output_callback=partial(_render_message, Sender.BOT),
            tool_output_callback=partial(
                _tool_output_callback, tool_state=session["tools"]
            ),
            only_n_most_recent_images=session["only_n_most_recent_images"]
        )
        assert_test_response(response_list, test['expected_response'])
        console.print(HR)


def load_tests(file_path):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data["tests"]
    except Exception as e:
        raise (f"Error loading tests: {e}")

def assert_test_response(responses: list[BetaMessageParam], expected_response):
    try:
        final_response = responses[-1]["content"]
        status = final_response[-1]['text'].split('\n')[-1]
        console.print(HR)
        if SUCCESS_INDICATOR in status.lower():
            console.print("TEST PASSED", style="bold green")
        else:
            console.print("TEST FAIL", style="bold red")
        console.print(f"Expected response: {expected_response}", style="bold blue")
    except Exception as e:
        console.print(f"Error asserting response: {e}", style="bold red")
        