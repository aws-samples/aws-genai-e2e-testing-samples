# Automating E2E Tests with Bedrock and Anthropic's "Computer Use"

This repository contains an experimental sample code which allows developers to automate UI testing by simply writing test cases using natural language. It leverages Anthropic's `Claude 3.5 Sonnet v2` large language model (LLM), which interprets test scenarios and identifies UI components in an application. The `Claude 3.5 Sonnet v2` model includes the "computer use" (beta) feature, allowing it to interact with computers and execute actions within a web browser.

This repo explores the feasibility of building proprietary tools around Claude's "computer use" capability, integrating with Claude, executing browser actions in headless mode, and running end-to-end test scenarios.

This repository provides two experimental implementations of this testing framework, tailored to different testing needs:

1. **integrating-with-headless-browser** using the "Computer Tool" in a headless environment.  
2. **advanced-e2e-tests-with-react** utilizing the "Bash and Text Editor Tools" in a React application.

## Appendix
### Resources and reading material
* Claude computer use: https://docs.anthropic.com/en/docs/build-with-claude/computer-use
* Understanding different parameters: https://docs.anthropic.com/en/api/messages
* Understand tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use#single-tool-example
* Understanding a full request / response scenario: https://docs.anthropic.com/en/docs/build-with-claude/tool-use#tool-use-examples
* Prompt engineering for Claude's system parameter to fit selenium scenario: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
