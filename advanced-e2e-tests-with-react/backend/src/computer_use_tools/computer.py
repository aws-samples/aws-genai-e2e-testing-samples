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

import asyncio
import base64
import os
from pathlib import Path
from typing import Literal, TypedDict
from uuid import uuid4

from anthropic.types.beta import BetaToolComputerUse20241022Param

from .base import BaseAnthropicTool, ToolError, ToolResult
from src.driver.manager import WebDriverSingleton
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

OUTPUT_DIR = "./tests/screenshots"

TYPING_DELAY_MS = 12
TYPING_GROUP_SIZE = 50

KEY_MAP = {
    "return": Keys.ENTER,
    "tab": Keys.TAB,
    "space": Keys.SPACE,
    "backspace": Keys.BACKSPACE,
    "escape": Keys.ESCAPE,
    "page_down": Keys.PAGE_DOWN,
    "page_up": Keys.PAGE_UP,
}

Action = Literal[
    "key",
    "type",
    "mouse_move",
    "left_click",
    "right_click",
    "middle_click",
    "double_click",
    "screenshot",
    "cursor_position",
]

class ComputerToolOptions(TypedDict):
    display_height_px: int
    display_width_px: int
    display_number: int | None


def chunks(s: str, chunk_size: int) -> list[str]:
    return [s[i : i + chunk_size] for i in range(0, len(s), chunk_size)]

class ComputerTool(BaseAnthropicTool):
    """
    A tool that allows the agent to interact with the screen, keyboard, and mouse of the current computer.
    The tool parameters are defined by Anthropic and are not editable.
    """

    name: Literal["computer"] = "computer"
    api_type: Literal["computer_20241022"] = "computer_20241022"
    width: int
    height: int
    display_num: int | None
    mouse_coordinates: tuple[int, int] | None = (0,0)

    _screenshot_delay = 2.0
    _scaling_enabled = False
    _web_driver = WebDriverSingleton.get_driver()
    _actions = ActionChains(_web_driver)

    @property
    def options(self) -> ComputerToolOptions:
        return {
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {"name": self.name, "type": self.api_type, **self.options}

    def __init__(self):
        super().__init__()
        viewport = self._web_driver.execute_script("""
            return {width: window.innerWidth, height: window.innerHeight};
        """)

        self.width = viewport["width"]
        self.height = viewport["height"]
        if (display_num := os.getenv("DISPLAY_NUM")) is not None:
            self.display_num = int(display_num)
        else:
            self.display_num = 1
        
        self._cleanup_screenshot_dir()

    async def __call__(
        self,
        *,
        action: Action,
        text: str | None = None,
        coordinate: tuple[int, int] | None = None,
        **kwargs,
    ):
        # Track Mouse position
        self._web_driver.execute_script("""
            document.addEventListener('mousemove', function(event) {
                window.mouseX = event.clientX;
                window.mouseY = event.clientY;
            });
        """)
        if action in ("mouse_move"):
            return await self.mouse_move_actions(action=action, text=text, coordinate=coordinate)
            
        if action in ("key", "type"):
            return await self.type_actions(action=action, text=text)
            
        if action in (
            "left_click",
            "right_click",
            "double_click",
            "middle_click",
            "screenshot",
            "cursor_position",
        ):
            return await self.click_actions(action=action)
        
        raise ToolError(f"Invalid action: {action}")
    
    async def mouse_move_actions(self, action, text, coordinate):
        if coordinate is None:
            raise ToolError(f"coordinate is required for {action}")
        if text is not None:
            raise ToolError(f"text is not accepted for {action}")
        if not isinstance(coordinate, list) or len(coordinate) != 2:
            raise ToolError(f"{coordinate} must be a tuple of length 2")
        if not all(isinstance(i, int) and i >= 0 for i in coordinate):
            raise ToolError(f"{coordinate} must be a tuple of non-negative ints")

        x, y = coordinate
        try:
            # get current mouse position
            x1, y1 = await self.get_mouse_coordinates()
            if x1 is None or y1 is None:
                #print("Mouse position is not available.")
                cmd = ActionChains(self._web_driver).move_by_offset(x, y).perform()
            else:
                # print(f'Moving mouse from {x1}, {y1} to {x}, {y}')
                # Move the mouse from its current position to (0,0), then to the specified (x, y) location
                cmd = ActionChains(self._web_driver).move_by_offset(-int(x1),-int(y1)).move_by_offset(x, y).perform()
            self.mouse_coordinates = (x, y)
            return await self.execute(cmd)
        except Exception as e:
            raise ToolError(f"Failed to move mouse: {e}")

    async def type_actions(self, action, text):
        if text is None:
            raise ToolError(f"text is required for {action}")
        if not isinstance(text, str):
            raise ToolError(f"{text} must be a string")
        
        if action == "key":
            cmd = self._get_active_element().send_keys(
                KEY_MAP.get(text.lower(), text)
            )
            return await self.execute(cmd)
        elif action == "type":
            input_element = self._get_active_element()
            if input_element.tag_name == "input" or input_element.tag_name == "textarea":
                input_element.clear()
                return await self.execute(input_element.send_keys(text))
            else:
                raise ToolError(f"Cannot type into element {input_element.tag_name}")
            
    async def click_actions(self, action):
        if action == "screenshot":
            return await self._take_delayed_screenshot()
        elif action == "cursor_position":
            x, y = (
                int(self._web_driver.execute_script("return window.mouseX;")),
                int(self._web_driver.execute_script("return window.mouseY;")),
            )
            return ToolResult(output=f"X={x},Y={y}")
        else:
            click_arg = {
                "left_click": await self.left_click(self.mouse_coordinates),
                "right_click": self._actions.context_click(),
                "middle_click": self._actions.click(),
                "double_click": self._actions.double_click(),
            }[action]
            return await self.execute(click_arg)
        
    async def execute(self, command, take_screenshot=True) -> ToolResult:
        """Run the command and return the output, error, and optionally a screenshot."""
        base64_image = None
        try:
            command
            if take_screenshot:
                base64_image = (await self._take_delayed_screenshot()).base64_image
            return ToolResult(output="", error="", base64_image=base64_image)
        except ToolError as e:
            return ToolResult(output="", error=str(e), base64_image=base64_image)
        except Exception as e:
            return ToolResult(output="", error=str(e), base64_image=base64_image)
    
    async def left_click(self, coordinate: tuple[int, int]) -> ToolResult:
        """Perform a left-click at the specified coordinates."""
        try:
            x, y = coordinate
            element = self._web_driver.execute_script(f"return document.elementFromPoint({x}, {y});")
            # print(f"element from point {element.tag_name} {element.text}")
            if element:
                return await self.execute(self._actions.move_to_element(element).click().perform())
            return ToolResult(output='Left click performed')
        except Exception as e:
            return ToolResult(error=str(e))
    
    async def _take_delayed_screenshot(self):
        """Helper method to take a screenshot after a delay."""
        try:
            await asyncio.sleep(self._screenshot_delay)
            return await self.screenshot()
        except Exception as e:
            return ToolError(f"Failed to take screenshot: {e}")
        
    async def screenshot(self):
        """Take a screenshot of the current screen and return the base64 encoded image."""
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"screenshot_{uuid4().hex}.png"
        
        self._web_driver.save_screenshot(path)
        #result = ToolResult(output=f"Screenshot saved at {path}", error="", base64_image=None)
        result = ToolResult(output="", error="", base64_image=None)

        if path.exists():
            return result.replace(
                base64_image=base64.b64encode(path.read_bytes()).decode()
            )
        raise ToolError(f"Failed to take screenshot: {result.error}")
    
    async def get_mouse_coordinates(self):
        """Get the current mouse coordinates."""
        x, y = (
                self._web_driver.execute_script("return window.mouseX;"),
                self._web_driver.execute_script("return window.mouseY;"),
            )
        return x, y
    
    def _get_active_element(self):
        return self._web_driver.switch_to.active_element

    def _cleanup_screenshot_dir(self):
        """Delete all files in the screenshot directory."""
        output_dir = Path(OUTPUT_DIR)
        if output_dir.exists():
            for file in output_dir.iterdir():
                file.unlink()
        print("Screenshot directory cleaned up")
