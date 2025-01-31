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

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, fields, replace
from typing import Any, Optional

from anthropic.types.beta import BetaToolUnionParam


class BaseAnthropicTool(metaclass=ABCMeta):
    """Abstract base class for Anthropic-defined tools."""

    @abstractmethod
    def __call__(self, **kwargs) -> Any:
        """Executes the tool with the given arguments."""
        ...

    @abstractmethod
    def to_params(self) -> BetaToolUnionParam:
        """Returns the tool's parameters in the BetaToolUnionParam format."""
        raise NotImplementedError


@dataclass(kw_only=True, frozen=True)
class ToolResult:
    """Represents the result of a tool execution."""
    output: Optional[str] = None
    error: Optional[str] = None
    base64_image: Optional[str] = None
    system: Optional[str] = None

    def __bool__(self) -> bool:
        """Check if any field in the result is populated."""
        return any(getattr(self, field.name) for field in fields(self))

    def __add__(self, other: "ToolResult") -> "ToolResult":
        """Combine two ToolResults by merging their fields."""
        def combine_fields(
            field1: Optional[str], field2: Optional[str], concatenate: bool = True
        ) -> Optional[str]:
            if field1 and field2:
                return field1 + field2 if concatenate else field1
            return field1 or field2

        return ToolResult(
            output=combine_fields(self.output, other.output),
            error=combine_fields(self.error, other.error),
            base64_image=combine_fields(self.base64_image, other.base64_image, False),
            system=combine_fields(self.system, other.system)
        )

    def replace(self, **kwargs: Any) -> "ToolResult":
        """Returns a new ToolResult with the specified fields replaced."""
        return replace(self, **kwargs)


class CLIResult(ToolResult):
    """A ToolResult that can be rendered as a CLI output."""
    pass


class ToolFailure(ToolResult):
    """A ToolResult that represents a failure."""
    pass


class ToolError(Exception):
    """Raised when a tool encounters an error."""

    def __init__(self, message: str):
        """
        Initializes the ToolError with an error message.

        Args:
            message (str): The error message describing the issue.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Returns the string representation of the error."""
        return f"ToolError: {self.message}"
