# Claude Code in Action

Fuente: https://anthropic.skilljar.com/claude-code-in-action

## Para que sirve

Integrate Claude Code into your development workflow

## Cobertura del scrape

- Lecciones visibles en pagina de curso: 21
- Contenido extenso embebido: si
- PDFs detectados: 0
- Videos detectados en pagina principal: 8
- Lecciones bloqueadas al abrir pagina individual: 21

## Secciones

### Claude Code in action

Complete guide to using Claude Code effectively. Starts with understanding how coding assistants work, then moves through setup, context management, making changes, and advanced features like MCP servers, GitHub integration, and hook implementations.

## Resumen de estudio

### What is a Coding Assistant?

- Coding Assistant = tool that uses language models to write code and complete development tasks
- Core Process:
- 1. Receives task (e.g., fix bug from error message)
- 2. Language model gathers context (reads files, understands codebase)
- 3. Formulates plan to solve issue
- 4. Takes action (updates files, runs tests)
- Key Limitation: Language models only process text input/output - cannot directly read files, run commands, or interact with external systems.
- Tool Use System = method enabling language models to perform actions:

### Claude Code in Action

- Claude Code = AI assistant with tool-based capabilities for code tasks
- Default tools = file reading/writing, command execution, basic development operations
- Performance optimization demo: Claude analyzed Chalk JavaScript library (5th most downloaded JS package, 429M weekly downloads). Used benchmarks, profiling tools, created todo lists, identified bottlenecks, implemented fixes. Result = 3.9x throughput improvement.
- Data analysis demo: Claude performed churn analysis on video streaming platform CSV data using Jupyter notebooks. Executed code cells iteratively, viewed results, customized successive analyses based on findings.
- Tool extensibility: Claude Code accepts new tool sets. Example used Playwright MCP server for browser automation. Claude opened browser, took screenshots, updated UI styling, iterated on design improvements.
- GitHub integration: Claude Code runs in GitHub Actions, triggered by pull requests/issues. Gets GitHub-specific tools (comments, commits, PR creation).
- Infrastructure review example: Terraform-defined AWS infrastructure with DynamoDB table and S3 bucket shared with external partner. Developer added user email to Lambda function output. Claude Code automatically detected PII exposure risk in pull request review by analyzing infrastructure flow and identifying external data sharing.
- Key principle: Claude Code = flexible assistant that grows with team needs through tool expansion rather than fixed functionality.

### Adding Context

- Context management = critical for Claude Code effectiveness. Too much irrelevant info decreases performance.
- /init command = analyzes entire codebase on first run, creates Claude.md file with project summary/architecture/key files. File contents included in every request.
- Three Claude.md file types:
- Project level = shared with team, committed to source control
- Local level = personal instructions, not committed
- Machine level = global instructions for all projects
- Memory mode (# symbol) = edit Claude.md files intelligently with natural language requests
- @ symbol = mention specific files to include in requests, provides targeted context instead of letting Claude search

### Making Changes

- Claude Code Change Management:
- Screenshot integration = Control-V (not Command-V on macOS) pastes screenshots to help Claude understand specific UI elements to modify
- Performance boosting modes:
- Plan Mode = Shift + Tab twice, makes Claude research more files and create detailed implementation plans before executing
- Thinking Mode = triggered by phrases like "Ultra think", gives Claude extended reasoning budget for complex logic
- Planning vs Thinking usage:
- Planning = handles breadth, useful for multi-step tasks requiring wide codebase understanding
- Thinking = handles depth, useful for tricky logic or debugging specific issues

### Controlling Context

- Context Control Techniques:
- Escape = Stops Claude mid-response to redirect conversation flow. Press once to interrupt current output.
- Escape + Memory = Powerful error prevention. Stop Claude, add memory about repeated mistakes using # shortcut to prevent future occurrences.
- Double Escape = Conversation rewind. Shows all previous messages, allows jumping back to earlier point while maintaining relevant context and skipping irrelevant debugging/back-and-forth.
- Compact Command = Summarizes entire conversation history while preserving Claude's learned knowledge about current task. Use when Claude has gained expertise but conversation has accumulated clutter.
- Clear Command = Deletes entire conversation history for fresh start. Use when switching to completely unrelated tasks.
- Key Benefits: Maintains focus, reduces distracting context, preserves relevant knowledge, prevents repeated errors. Most effective for long conversations and task transitions.

### Custom Commands

- Custom Commands = user-defined automation commands in Claude Code accessed via forward slash
- Location = .Claude/commands/ folder in project directory
- File naming = filename becomes command name (audit.md creates /audit command)
- Activation = restart Claude Code after creating command files
- Command structure = markdown file containing instructions for Claude to execute
- Arguments = use $arguments placeholder in command text to accept runtime parameters
- Argument types = any string (file paths, descriptive text, etc.)
- Use cases = automating repetitive tasks like dependency auditing, test generation, vulnerability fixes

### Extending Claude Code with MCP Servers

- MCP servers = external tools that extend Claude Code capabilities, run locally or remotely.
- Playwright MCP server = popular server enabling Claude to control browsers for web automation.
- Installation: Terminal command \`claude mcp add [name] [start-command]\` adds MCP server to Claude Code.
- Permission management: Initial tool usage requires approval. Auto-approve by adding "MCP__[servername]" to settings.local.json allow array.
- Practical example: Claude used Playwright to navigate localhost:3000, generate UI component, analyze styling quality, then automatically update generation prompts based on visual feedback.
- Results: Automated prompt refinement produced significantly better component styling, demonstrating MCP servers unlock sophisticated development workflows.
- Key benefit: MCP servers enable Claude to perform complex multi-step tasks involving external systems, expanding beyond code editing to full development automation.

### Github Integration

- Claude Code GitHub Integration = official integration allowing Claude to run inside GitHub actions
- Setup Process:
- Run "/install GitHub app" command
- Install Claude Code app on GitHub
- Add API key
- Auto-generated pull request adds two GitHub actions
- Default Actions:
- 1. Mention support = @Claude in issues/PRs to assign tasks

### Introducing Hooks

- Hooks = commands that run before/after Claude executes tools
- Pre-tool use hooks = run before tool execution, can inspect and block tool operations, send error messages to Claude
- Post-tool use hooks = run after tool execution, perform follow-up operations, provide feedback to Claude
- Configuration = added to Claude settings file (global/project/personal) via manual editing or /hooks command
- Hook structure = two sections (pre-tool use, post-tool use), each with matcher (specifies which tools to target) and commands to execute
- Example uses = auto-format files after creation, run tests after edits, block file access, code quality checks, type checking
- Hook commands = receive tool call details, can modify Claude's workflow through blocking or feedback mechanisms

### Defining Hooks

- **Hooks Overview**
- Hooks = mechanisms to intercept and control tool calls before/after execution
- **Hook Types**
- Pre-tool use hook = executes before tool call, can block execution
- Post-tool use hook = executes after tool call, cannot block execution
- **Hook Implementation Process**
- 1. Choose hook type (pre vs post)
- 2. Identify target tool names to monitor

### Defining Hooks

- Hooks = mechanisms to control Claude's tool usage by running custom commands before/after tool calls
- Pre-tool use hook = executes before tool call, can block with exit code 2
- Post-tool use hook = executes after tool call, cannot block
- Hook process:
- 1. Claude sends tool call data as JSON via stdin to your command
- 2. Command parses JSON containing tool_name and input arguments
- 3. Command exits with code 0 (allow) or 2 (block for pre-hooks only)
- 4. Exit code 2 sends stderr output as feedback to Claude

### Implementing a Hook

- **Custom Hook Implementation**
- Hook purpose = prevent Claude from reading .env file contents
- **Configuration Setup**
- Location = .clod/settings.local.json
- Hook type = pre-tool use hook (blocks before execution)
- Matcher = "read|grep" (pipe symbol separates tool names)
- Command = "node ./hooks/read_hook.js"
- **Implementation Details**

### Implementing a Hook

- **Hook Implementation Process:**
- Hook = custom script that intercepts and controls tool usage in Clod
- **Configuration (settings.local.json):**
- Pre-tool use hooks = run before tool execution
- Post-tool use hooks = run after tool execution
- Matcher = specifies which tools to intercept (e.g., "read|grep")
- Command = script to execute when matched tools are called
- **Implementation Steps:**

### Useful Hooks!

- **Useful Hooks for Claude Code Projects**
- **Problem**: Claude Code often misses type errors and creates duplicate code, especially in larger projects.
- **Hook 1: TypeScript Type Checker Hook**
- **Purpose**: Catch type errors immediately after file edits
- **Implementation**: Run \`tsc --no-emit\` after TypeScript file changes via post-tool-use hook
- **Process**: Detects type errors → feeds errors back to Claude → Claude fixes call sites automatically
- **Benefits**: Prevents broken function calls when signatures change
- **Adaptable**: Works for any typed language with type checker, or use tests for untyped languages

### Useful Hooks!

- TypeScript Type Checker Hook:
- Problem: Claude edits function signatures but doesn't update call sites, causing type errors
- Solution: Post-tool-use hook that runs \`tsc --no-emit\` after TypeScript file edits
- Process: Detects type errors → feeds errors back to Claude → Claude fixes call sites automatically
- Works for any typed language with type checker, or untyped languages using tests instead
- Query Deduplication Hook:
- Problem: Claude creates duplicate SQL queries/functions instead of reusing existing ones, especially in complex tasks
- Cause: Focused tasks work well, but wrapped/complex tasks make Claude lose focus

### The Claude Code SDK

- Claude Code SDK = programmatic interface for Claude Code with CLI, TypeScript, and Python libraries. Contains same tools as terminal version.
- Primary use case = integration into larger pipelines/workflows to add intelligence to existing processes.
- Default permissions = read-only (files, directories, grep operations). Write permissions require manual configuration via options.allowTools array or .Claude directory settings.
- SDK execution shows raw conversation between local Claude Code and language model, with final response as last message.
- Key implementation pattern = add write permissions by specifying tools like "edit" in options.allowTools when making query calls.
- Best suited for = helper commands, scripts, and hooks within existing projects rather than standalone usage.

### The Claude Code SDK

- Claude Code SDK = programmatic interface to use Claude Code via CLI, TypeScript, or Python libraries. Same tools as terminal version.
- Primary use case = integration into larger pipelines/workflows to add intelligence to processes.
- Key characteristics:
- Default permissions = read-only (files, directories, grep operations)
- Write permissions = must be manually enabled via query options or settings file
- Raw conversation output = shows message-by-message exchange between local Claude Code and language model
- Best applications = helper commands, scripts, hooks within existing projects rather than standalone use.
- Output format = conversational messages with final response from Claude as last message.

## Preguntas de repaso

- Cual es el objetivo practico de este curso?
- Que conceptos o herramientas aparecen repetidamente?
- Que decisiones humanas no deberian delegarse por completo a la IA?
- Que evidencias o verificaciones exige el flujo de trabajo presentado?
- Que skill de LinkedIn representa mejor esta certificacion?
