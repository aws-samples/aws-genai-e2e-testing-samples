# Automating E2E Tests with Bedrock and Anthropic's "Computer Use" - Integrating E2E in headless browser

In this part of the repository, we're exploring the idea of automating E2E testing by running an instance of a headless browser to make it easily integrate with CI/CD pipelines.

This repository includes key modules such as:
- **Agent Loop**: Responsible for managing the interaction between the Claude LLM and the computer tools. It begins by submitting the user's test case to the LLM, relaying the corresponding actions back to the computer interface. The module handles executing these actions (by delegating them back to the ComputerTool), provides feedback to the LLM on the results, and finally exits the loop when an end condition is met or indicated by the LLM.
- **ComputerTool**: Provides a programmatic way to interact with a headless web browser, enabling capabilities like:
    - Moving the mouse cursor
    - Clicking with the mouse
    - Entering text
    - Pressing hotkeys (e.g., return, space, escape)

Selenium is used as the WebDriver for browser interaction.

## Getting Started

### 1. Install Dependencies

- Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

- Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Model Setup

- Navigate to **Bedrock** on your AWS account.
- Ensure you are in the **'us-west-2'** region.
- Request access to Anthropic's 'Claude 3.5 Sonnet v2' LLM.

### 3. Get AWS (Bedrock) Credentials

To interact with the Bedrock service, set your AWS credentials in the terminal:
```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_SESSION_TOKEN="your-session-token"
export AWS_REGION="us-west-2"
```

### 4. Write Your Test Case
Write your test case in the `tests/testcase.txt` file in the following format:
- The first line should contain the **website URL**.
- The second line should be **empty**.
- The following lines should contain the test case **description**.

Example:
```
https://www.amazon.com/

You are on amazon.com website.
Search for 'xbox' on the search bar at the top.
You should see a list of search results.
Click on the first item in the list.
You should see item details.
Finally verify that the item is a sony playstation product.
```
> DISCLAIMER: You need to provide both the website url, and indicate in your test scenario that you are on that website for better context to the LLM. For example: "You are on amazon.com website".

As of now, we only support running a single test case. This can easily be expanded further to to include and run multiple files or test cases. Please refer to `src/main.py` and `src/utils/testcase_reader.py`.

### 5. Run Your Test

To execute the test:

1. Navigate to the `src` directory:
    ```bash
    cd src
    ```

2. Run the main testing script:
    ```bash
    python3 main.py
    ```

During the test execution:
- You will see detailed logs in the console, showing what **Claude** is doing at each step.
- Screenshots will be saved in the `./screenshots` directory to help you better follow the test execution and verify UI interactions.



## Important Notes

### 1. Rate Limiting:
To avoid running into rate limiting issues by the API gateway, make sure this piece of instruction is included in your system prompt:
```
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
```

## Improvements needed
### 1. How to provide indication for the test assertion status?
Ideally, it would be great to be able to receive an augmented response from Claude which includes an additional field like `testStatus`. But this is not possible at the moment. Claude response will include a list 'blocks', each can be of type `tool_use` or `text`. For example:
```json
{
  "id": "toolu_bdrk_01Uzt5fZXhCVbX8GEgGiTsoQ",
  "input": { "action": "mouse_move", "coordinate": [580, 29] },
  "name": "computer",
  "type": "tool_use"
}
```
```json
{
  "type": "text",
  "text": "5. Let me take a screenshot of the product details page to verify the assertion"
}

```

As of now, we use this system prompt to ask the LLM to return `success` or `fail` at the end of the final reponse:
```
* You will be provided with a complete test case scenario, which includes an assertion condition at the end. After executing all the actions needed to for the test, your final message should ONLY be 1 word either 'Success' or 'Fail' to indicate whether the assertion was met.
```

The final LLM response looks something like this
```json
{
  "type": "text",
  "text": "Based on the final screenshot, I can verify that this product is NOT an RC car. It is an Xbox Series X – 1TB Digital Edition gaming console.\n\nFail"
}
```

Finally, we parse the last line in this message to get the assertion status.

### 2. Payload reduction
Claude requests screenshots (base64) to be able to get a context of what's happening in the computer in order to be able to provide a feedback and follow-up actions. This will happen multiple times during the execution of a test scenario, and since Claude requires a 'context' i.e. providing a list of all messages in the conversation including images, we can run into payload issues.

### 3. How to avoid infnite loops?
If Claude can't execute an action or not seeing a reponse it can deal with it can go on forever trying multiple actions.

### 4. Additional actions needed
Scrolling hasn't been testing yet.