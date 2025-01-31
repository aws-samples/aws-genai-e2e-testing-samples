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

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import base64
from pathlib import Path
from typing import Literal, TypedDict
from anthropic.types.beta import BetaToolComputerUse20241022Param

from .base import ToolResult

# Constants
OUTPUT_DIR = "../screenshots"
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
    "key", "type", "mouse_move", "left_click", "left_click_drag", 
    "right_click", "middle_click", "double_click", "screenshot", "cursor_position"
]

class Resolution(TypedDict):
    width: int
    height: int

class ComputerTool:
    """
    A tool that allows interaction with the screen, keyboard, and mouse.
    """

    name: Literal["computer"] = "computer"
    api_type: Literal["computer_20241022"] = "computer_20241022"
    _screenshot_delay = 2.0
    screenshot_counter = 1

    def __init__(self, website_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--high-dpi-support=1")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,800")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.width, self.height = self._get_viewport_size()
        self.driver.get(website_url)
        self.coordinate = (0, 0)
        self._remove_all_files(OUTPUT_DIR)

    def _get_viewport_size(self) -> tuple[int, int]:
        """Get the actual viewport size."""
        viewport = self.driver.execute_script("""
            return {width: window.innerWidth, height: window.innerHeight};
        """)
        return viewport['width'], viewport['height']

    async def __call__(
        self, *, action: Action, text: str | None = None, coordinate: tuple[int, int] | None = None
    ) -> ToolResult:
        """Handle different actions based on the input."""
        try:
            if action == "screenshot":
                return await self.screenshot()
            if action == "mouse_move" and coordinate:
                return await self.move_mouse(coordinate)
            if action == "left_click":
                return await self.left_click(self.coordinate)
            if action == "type" and text:
                return await self.type_text(text)
            if action == "key" and text:
                return await self.send_key(text)
            
            raise ValueError(f"Unsupported action: {action}")
        finally:
            # Take a monitoring screenshot after each action
            if not action == "screenshot":
                await self.screenshot(action)

    async def screenshot(self, action: str = 'screenshot') -> ToolResult:
        """Take a screenshot and return it as a base64 string."""
        path = Path(OUTPUT_DIR) / f"{self.screenshot_counter}-{action}.png"; self.screenshot_counter += 1
        path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(path))
        with path.open("rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode()
        return ToolResult(base64_image=base64_image)

    async def move_mouse(self, coordinate: tuple[int, int]) -> ToolResult:
        """Move the mouse to the specified coordinates."""
        try:
            x, y = coordinate
            ActionChains(self.driver).move_by_offset(x, y).perform()
            self.coordinate = coordinate
            return ToolResult(output='Mouse moved')
        except Exception as e:
            return ToolResult(error=str(e))

    async def left_click(self, coordinate: tuple[int, int]) -> ToolResult:
        """Perform a left-click at the specified coordinates."""
        try:
            x, y = coordinate
            element = self.driver.execute_script(f"return document.elementFromPoint({x}, {y});")
            if element:
                ActionChains(self.driver).move_to_element(element).click().perform()
            return ToolResult(output='Left click performed')
        except Exception as e:
            return ToolResult(error=str(e))

    async def type_text(self, text: str) -> ToolResult:
        """Type text into the active element."""
        try:
            active_element = self.driver.switch_to.active_element
            active_element.clear()
            active_element.send_keys(text)
            return ToolResult(output='Text inputted')
        except Exception as e:
            return ToolResult(error=str(e))

    async def send_key(self, key: str) -> ToolResult:
        """Send a single keypress."""
        try:
            mapped_key = KEY_MAP.get(key.lower(), key)
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(mapped_key)
            return ToolResult(output='Key pressed')
        except Exception as e:
            return ToolResult(error=str(e))

    def to_params(self) -> BetaToolComputerUse20241022Param:
        """Convert object to API parameters."""
        return {
            "name": self.name,
            "type": self.api_type,
            "display_height_px": self.height,
            "display_width_px": self.width,
            "display_number": 1,
        }

    def __del__(self):
        """Ensure the Selenium driver is properly closed."""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _remove_all_files(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
