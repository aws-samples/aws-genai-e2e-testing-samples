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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from src.client import get_app_base_url
from selenium.webdriver.firefox.service import Service as FirefoxService

class WebDriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            firefox_options = Options()
            firefox_options.add_argument("--headless")  # Headless mode
            firefox_options.add_argument("--disable-gpu")  # Disable GPU acceleration
            firefox_options.add_argument("--no-sandbox") 
            firefox_options.add_argument("--window-size=1280,800")
            if os.getenv("ENVIRONMENT") == "container":
                if os.getenv("FIREFOX_BINARY_PATH") is None:
                    raise ValueError("FIREFOX_BINARY_PATH environment variable is not set.")
                firefox_options.binary_location = os.getenv("FIREFOX_BINARY_PATH")
                service = FirefoxService(executable_path=GeckoDriverManager().install())
                cls._driver = webdriver.Firefox(service=service, options=firefox_options)
            else:
                cls._driver = webdriver.Firefox(options=firefox_options)
            cls._driver.get(get_app_base_url()) 
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
