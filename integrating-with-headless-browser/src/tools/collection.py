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

from typing import Any, Dict, List
from anthropic.types.beta import BetaToolUnionParam
from .base import BaseAnthropicTool, ToolError, ToolFailure, ToolResult


class ToolCollection:
    """A collection of anthropic-defined tools for efficient management and execution."""

    def __init__(self, *tools: BaseAnthropicTool):
        """
        Initializes the collection with a list of tools.
        
        Args:
            tools: A variable number of BaseAnthropicTool instances.
        """
        self.tools = tools
        # Create a mapping of tool names to tool instances
        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}
        
        # Optionally, validate the uniqueness of tool names
        if len(self.tool_map) != len(tools):
            raise ValueError("Duplicate tool names found in the provided tools.")

    def to_params(self) -> List[BetaToolUnionParam]:
        """
        Converts the tools into their parameter representation.
        
        Returns:
            A list of BetaToolUnionParam for each tool.
        """
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: Dict[str, Any]) -> ToolResult:
        """
        Executes a tool by its name with the provided input.
        
        Args:
            name: The name of the tool to execute.
            tool_input: The input dictionary for the tool.

        Returns:
            ToolResult: The result of the tool execution.
        """
        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool '{name}' is invalid")

        try:
            # Execute the tool asynchronously
            return await tool(**tool_input)
        except ToolError as e:
            # Handle known tool errors
            return ToolFailure(error=e.message)
        except Exception as e:
            # Handle unexpected exceptions
            return ToolFailure(error=f"Unexpected error: {e}")
