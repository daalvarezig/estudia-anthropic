# Model Context Protocol: Advanced Topics

Fuente: https://anthropic.skilljar.com/model-context-protocol-advanced-topics

## Para que sirve

Discover advanced Model Context Protocol implementation patterns including sampling, notifications, file system access, and transport mechanisms for production MCP server development.

## Cobertura del scrape

- Lecciones visibles en pagina de curso: 15
- Contenido extenso embebido: si
- PDFs detectados: 0
- Videos detectados en pagina principal: 8
- Lecciones bloqueadas al abrir pagina individual: 15

## Secciones

### Core MCP features

Learn the advanced features that make MCP servers more powerful. Covers sampling to offload AI costs to clients, implementing progress notifications for better UX, and using roots to safely handle file access.

### Transports and communication

Understand how MCP messages flow between clients and servers. Explores the JSON message protocol, STDIO transport for local development, and the complexities of StreamableHTTP including when to sacrifice features for scalability.

## Resumen de estudio

### Sampling

- Sampling = technique allowing MCP servers to request language model text generation from clients instead of directly accessing LLMs themselves.
- Purpose = shifts LLM access responsibility from server to client, avoiding need for servers to handle API keys, authentication, or token costs.
- Architecture = Server creates message request → Client receives via sampling callback → Client calls LLM → Client returns generated text to server.
- Benefits = eliminates server complexity for LLM integration, removes API key requirements from servers, prevents unauthorized token usage on public servers.
- Implementation = Server uses create_message() function with message list, Client implements sampling callback to handle LLM requests and return create_message_result.
- Primary use case = publicly accessible MCP servers that need LLM capabilities without direct LLM access or associated costs/security concerns.

### Log and Progress Notitications

- Log and Progress Notifications = MCP server feature that provides real-time feedback during tool execution to improve user experience.
- Implementation on server side:
- Tool functions automatically receive context argument as last parameter
- Context object provides methods: info() for logging, report_progress() for progress updates
- Calling these methods automatically sends messages back to client
- Implementation on client side:
- Create callback function for logging statements
- Create separate callback for progress updates

### Roots

- MCP Roots = codified way for users to grant server access to specific files/folders
- Problem without roots: User says "convert bikin.mp4" but Claude can't locate file in complex filesystem without full path. Requiring full paths inconvenient for users.
- Solution with roots: Add 3 tools to MCP server:
- ConvertVideo (original tool)
- ReadDirectory (lists files/folders in directory)
- ListRoots (returns available roots)
- Root = file/folder user grants permission to access beforehand (via command line args when starting server)
- Implementation requirement: Tools must check that accessed files/folders are contained within granted roots using function like is_path_allowed()

### JSON Message Types

- JSON Message Types in MCP:
- MCP communication = JSON messages between clients and servers. Each message type has distinct purpose.
- Message categories:
- Request/Result pairs = Always come together (call_tool_request + call_tool_result, initialize_request + initialize_result)
- Notifications = Events that don't need responses (progress_notification, logging_message_notification, tool_change_notification)
- Message direction classification:
- Client messages = Sent by MCP client to server
- Server messages = Sent by MCP server to client

### The Stdio Transport

- MCP Transport = mechanism for moving JSON messages between client and server
- Stdio Transport = transport where client launches server as separate process, communicates via standard input/output streams
- Communication mechanism: Client writes to server's stdin, reads from server's stdout. Server writes to stdout, reads from stdin.
- Advantages: Bidirectional communication - either client or server can initiate requests at any time
- Limitations: Only works when client and server run on same physical machine
- Message exchange patterns:
- Client-to-server request: Write to stdin, read response from stdout
- Server-to-client request: Server writes to stdout, client responds via stdin

### The StreamableHTTP Transport

- StreamableHTTP Transport = MCP transport enabling client-server communication over HTTP connections, allows remote server hosting unlike standard I/O transport which requires same-machine operation.
- Key advantage = Remote hosting capability - servers can be publicly accessible at URLs like mcpserver.com, expanding MCP server possibilities.
- Critical limitation = Restricted server-to-client messaging functionality due to HTTP's unidirectional nature - clients easily request from servers, but servers cannot easily initiate requests to clients.
- Two key settings impact functionality:
- stateless HTTP (default: false)
- JSON response (default: false)
- Setting these to true = Reduced functionality, breaks progress bars, logging notifications, progress notifications, and sampling requests.
- HTTP communication constraint = Server doesn't know client address and client may not be publicly accessible, making server-initiated requests challenging.

### StreamableHTTP in Depth

- StreamableHTTP Transport = HTTP-based MCP transport using server-sent events (SSE) to enable server-to-client communication
- Core Problem: MCP requires server-to-client requests (sampling, notifications, logging) but HTTP naturally supports only client-to-server requests
- Workaround Solution: Uses SSE connections to allow server streaming messages to client
- Session ID = Random identifier assigned during initialization, included in all subsequent requests as HTTP header
- Initialization Flow:
- 1. Client sends initialize request
- 2. Server responds with result + MCP session ID header
- 3. Client sends initialized notification with session ID

### Stateless HTTP

- **Stateless HTTP Flag**
- Stateless HTTP = flag set to true when MCP server needs horizontal scaling across multiple instances with load balancer
- **Why needed**: Single server instance can't handle high traffic. Horizontal scaling uses multiple server copies + load balancer routing requests randomly.
- **Problem without stateless**: Client needs 2 connections (GET SSE for server-to-client requests, POST for client-to-server). Load balancer may route these to different server instances. If tool on Server A needs sampling request, it must go through GET SSE connection on Server B - requires complex coordination.
- **Effect of stateless=true**:
- No session IDs assigned to clients
- Server cannot track individual clients
- GET SSE response pathway disabled (server cannot send requests to client)

## Preguntas de repaso

- Cual es el objetivo practico de este curso?
- Que conceptos o herramientas aparecen repetidamente?
- Que decisiones humanas no deberian delegarse por completo a la IA?
- Que evidencias o verificaciones exige el flujo de trabajo presentado?
- Que skill de LinkedIn representa mejor esta certificacion?
