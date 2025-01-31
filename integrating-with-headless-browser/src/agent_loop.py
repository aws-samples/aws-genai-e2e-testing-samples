# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from enum import StrEnum
from typing import Any, cast

from anthropic import AnthropicBedrock
from anthropic.types.beta import (
    BetaImageBlockParam,
    BetaMessage,
    BetaMessageParam,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaToolResultBlockParam,
    BetaToolUseBlockParam,
)
from configs.agent import SYSTEM_PROMPT
from tools import ToolCollection, ComputerTool, ToolResult

# Beta flags
COMPUTER_USE_BETA_FLAG = "computer-use-2024-10-22"
PROMPT_CACHING_BETA_FLAG = "prompt-caching-2024-07-31"

class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"

# Mapping of API providers to default models
PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
    APIProvider.BEDROCK: "anthropic.claude-3-5-sonnet-20241022-v2:0",
}

# System and model setup
PROVIDER = APIProvider.BEDROCK
MODEL = PROVIDER_TO_DEFAULT_MODEL_NAME[PROVIDER]

async def sampling_loop(
    website_url: str,
    test_case: str,
    max_tokens: int = 4096,
) -> list[BetaMessageParam]:
    """
    Agentic sampling loop for the assistant/tool interaction of computer use.
    """
    messages: list[BetaMessageParam] = [{"role": "user", "content": test_case}]
    tool_collection = ToolCollection(ComputerTool(website_url))
    system_prompt = BetaTextBlockParam(type="text", text=SYSTEM_PROMPT)
    client = AnthropicBedrock()
    betas = [COMPUTER_USE_BETA_FLAG]

    while True:
        try:
            # Call the API and get a response
            raw_response = client.beta.messages.with_raw_response.create(
                max_tokens=max_tokens,
                messages=messages,
                model=MODEL,
                system=[system_prompt],
                tools=tool_collection.to_params(),
                betas=betas,
            )
        except Exception as e:
            print(f"API call failed: {e}")
            return messages

        response = raw_response.parse()
        print("******* New instructions received *******\n")
        response_params = _response_to_params(response)
        messages.append({"role": "assistant", "content": response_params})

        tool_result_content, final_agent_message = await _process_tool_use(tool_collection, response_params)
        if not tool_result_content:
            return final_agent_message

        messages.append({"content": tool_result_content, "role": "user"})

async def _process_tool_use(
    tool_collection: ToolCollection,
    response_params: list[BetaTextBlockParam | BetaToolUseBlockParam],
) -> list[BetaToolResultBlockParam]:
    """
    Process tool use instructions and return tool results.
    """
    tool_result_content = []
    final_agent_message = ''
    for block in response_params:
        print(f'{block}\n')
        if block["type"] == "tool_use":
            result = await tool_collection.run(
                name=block["name"],
                tool_input=cast(dict[str, Any], block["input"]),
            )
            tool_result_content.append(_make_api_tool_result(result, block["id"]))

    if not tool_result_content:
        final_agent_message = response_params[0]['text']
    return tool_result_content, final_agent_message

def _response_to_params(
    response: BetaMessage
) -> list[BetaTextBlockParam | BetaToolUseBlockParam]:
    """
    Convert the response to a list of parameters.
    """
    return [
        {"type": "text", "text": block.text} if isinstance(block, BetaTextBlock)
        else cast(BetaToolUseBlockParam, block.model_dump())
        for block in response.content
    ]

def _make_api_tool_result(
    result: ToolResult, tool_use_id: str
) -> BetaToolResultBlockParam:
    """
    Convert a ToolResult to a BetaToolResultBlockParam for the API.
    """
    tool_result_content: list[BetaTextBlockParam | BetaImageBlockParam] | str = []
    is_error = False

    if result.error:
        is_error = True
        tool_result_content = _maybe_prepend_system_tool_result(result, result.error)
    else:
        if result.output:
            tool_result_content.append({
                "type": "text",
                "text": _maybe_prepend_system_tool_result(result, result.output),
            })
        if result.base64_image:
            tool_result_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": result.base64_image,
                }
            })
    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }

def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str) -> str:
    """
    Prepend system information to the result if available.
    """
    if result.system:
        return f"<system>{result.system}</system>\n{result_text}"
    return result_text