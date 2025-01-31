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

import asyncio

from agent_loop import sampling_loop
from utils.testcase_reader import read_test_case

TEST_FILE_PATH = '../tests/testcase.txt'
SUCCESS_INDICATOR = 'success'

# Define the main function to call the async function
def main():

    # read test case
    test_case = read_test_case(TEST_FILE_PATH)

    # Run the event loop to execute the async function
    final_agent_message = asyncio.run(sampling_loop(test_case['website'], test_case['description']))
    status = final_agent_message.split('\n')[-1] # check the readme for more info about assertion status
    if SUCCESS_INDICATOR in status.lower():
        print("\033[32mTest Passed\033[0m")
    else:
        print("\033[31mTest Failed\033[0m")

# Run main function
if __name__ == "__main__":
    main()
