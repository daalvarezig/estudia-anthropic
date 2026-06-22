# Claude with Google Cloud's Vertex AI

Fuente: https://anthropic.skilljar.com/claude-with-google-vertex

## Para que sirve

This comprehensive course covers the full spectrum of working with Anthropic models through Google Cloud's Vertex AI.

## Cobertura del scrape

- Lecciones visibles en pagina de curso: 93
- Contenido extenso embebido: si
- PDFs detectados: 0
- Videos detectados en pagina principal: 8
- Lecciones bloqueadas al abrir pagina individual: 93

## Secciones

### Getting started with Claude

Start here for the fundamentals. Covers API authentication, basic requests, conversation management, system prompts, and structured output generation.

### Prompt engineering & evaluation

Learn to write prompts that actually work. Focuses on prompting strategies, evaluation frameworks, and systematic testing approaches.

### Tool use with Claude

Extend Claude with custom tools and functions. Build apps with function calling, multi-turn tool interactions, batch tool calling, and leverage built-in utilities.

### Retrieval augmented generation

Implementation guide for production RAG systems. Covers text chunking, embeddings, hybrid search with BM25, multi-index architectures, reranking, and contextual retrieval.

### Model Context Protocol (MCP)

The protocol for building modular AI applications. Define custom tools and resources, implement MCP servers and clients, handle the full integration lifecycle.

### Claude Code & Computer Use

Two powerful Anthropic tools in action. Claude Code accelerates development workflows, Computer Use automates UI interactions. Includes MCP integration patterns.

### Agents and workflows

Architecture patterns for autonomous AI systems. Understand parallel execution, operation chaining, conditional routing, and effective debugging strategies.

## Resumen de estudio

### Overview of Claude Models

- Claude models = 3 families optimized for different priorities
- **Opus** = highest intelligence model. For complex multi-step tasks requiring deep reasoning and planning. Can work independently for hours. Supports reasoning capability. Trade-off = higher cost + moderate latency.
- **Sonnet** = balanced model. Good intelligence + speed + cost efficiency. Strong coding abilities, precise code edits without breaking functionality. Fast text generation. Sweet spot for most use cases.
- **Haiku** = fastest model. Optimized for speed + cost efficiency. No reasoning capabilities. Best for real-time user interactions + high-volume processing.
- **Selection framework**: Intelligence priority → Opus. Speed priority → Haiku. Balanced needs → Sonnet.
- **Key insight**: Teams often use multiple models in same application. Haiku for user interactions, Sonnet for business logic, Opus for complex reasoning tasks.
- All models share core capabilities = text generation, coding, image analysis.

### Accessing the API

- API Access Flow = 5-step process from user input to response display
- Step 1: Client sends user text to developer's server (never access Vertex directly from client - credentials must stay secret)
- Step 2: Server makes request to Vertex AI using SDK (Python/TypeScript/Go/Ruby). Required parameters: model name, messages list, max_tokens limit
- Step 3: Claude text generation process = 4 stages:
- Tokenization = input broken into tokens (words/parts/symbols)
- Embedding = tokens converted to number lists representing all possible meanings
- Contextualization = embeddings adjusted based on neighboring tokens to determine precise meaning
- Generation = output layer produces word probabilities, model selects using probability + randomness, adds selected word, repeats process

### Making a Request

- **Making a Request to Vertex AI Claude**
- **Setup Steps:**
- 1. Install anthropic SDK: \`%pip install "anthropic[vertex]"\`
- 2. Import and create client: \`from anthropic import vertex\` then instantiate with region="global" and project_id
- 3. Define model version variable for reuse
- **Required Arguments for client.messages.create():**
- model = specific Claude model version string
- max_tokens = safety limit on response length (not a target, just maximum)

### Multi-Turn Conversations

- Multi-Turn Conversations = maintaining context across multiple exchanges with Claude
- Key constraint: Anthropic API stores no messages. Each request is stateless - no memory of previous exchanges.
- Problem: Sending follow-up requests without context produces irrelevant responses since Claude has no memory of prior conversation.
- Solution requirements:
- 1. Manually maintain message list in your code
- 2. Send entire conversation history with every request
- Implementation pattern:
- Create empty messages list

### System Prompts

- System Prompts = instructions that customize Claude's tone, style, and behavior for specific use cases.
- Purpose = control how Claude responds rather than just what it responds with. Example: making Claude act as patient math tutor who gives hints instead of direct answers.
- Implementation = pass system prompt as plain string to create function using system keyword argument.
- Structure = first line typically assigns Claude a role ("You are a patient math tutor"), followed by specific behavioral instructions.
- Key principle = system prompts steer Claude's approach - tutor gives guidance and asks leading questions vs directly solving problems.
- Technical consideration = system parameter cannot be None, must conditionally include in API call only when prompt exists.
- Best practice = make system prompts configurable rather than hard-coded for reusability across different use cases.
- Result = transforms direct question-answer interactions into guided, interactive experiences tailored to specific roles and contexts.

### Temperature

- Temperature = parameter controlling randomness in Claude's text generation, decimal value 0-1
- Text generation process = tokenization → probability assignment → token selection based on probabilities
- Temperature effects:
- Temperature 0 = deterministic output, always selects highest probability token
- Higher temperature = increases chance of selecting lower probability tokens, more creative/unexpected outputs
- Usage guidelines:
- Low temperature (near 0) = data extraction, factual tasks, consistent outputs
- High temperature (near 1) = creative writing, brainstorming, jokes, marketing

### Response Streaming

- Response Streaming = technique to provide immediate feedback to users during long AI response generation times instead of showing loading spinners for 10-30 seconds.
- How it works: Server sends user message to Claude → Claude immediately sends initial response (no text content, just acknowledgment) → Claude sends stream of events containing text chunks → Server receives events and sends text chunks to frontend → User sees text appear progressively chunk by chunk.
- Event types: message_start, content_block_start, content_block_delta (contains actual text), content_block_stop, message_delta, message_stop.
- Implementation:
- Basic streaming: client.messages.create(model, max_tokens, messages, stream=True) returns iterator of events
- Text-focused streaming: client.messages.stream() with context manager provides cleaner access to text content via stream.text_stream
- Final message assembly: stream.get_final_message() collects all chunks into complete message for database storage
- Key benefit: Users see immediate progressive response instead of waiting for complete generation, improving user experience in chat interfaces.

### Controlling Model Output

- Model output control = two main techniques beyond prompt modification: pre-filling assistant messages and stop sequences.
- Pre-filling assistant messages = manually adding assistant message at end of message list to steer response direction. Claude treats pre-filled content as already authored and continues from that point. Example: adding "coffee is better because" forces Claude to justify coffee preference. Response continues from end of pre-filled text, not complete replacement.
- Implementation: Add assistant message with partial content after user message in messages list. Claude sees this as its own previous response and builds upon it.
- Stop sequences = forcing Claude to halt generation when specific string appears. Provides list of strings that trigger immediate response termination when generated. Generated stop sequence text excluded from final output.
- Implementation: Add stop_sequences parameter to API call with list of trigger strings. Generation stops immediately upon encountering any listed sequence.
- Use cases: Pre-filling controls response direction/stance. Stop sequences control response length/format by terminating at specific points.

### Structured Data

- Structured Data Generation = combining stop sequences + assistant message prefilling to get raw output without commentary.
- Problem: Claude naturally adds headers/footers/explanations when generating structured data (JSON, Python, lists). Users often want just the raw content for copy/paste functionality.
- Solution Pattern:
- 1. Pre-fill assistant message with opening delimiter (e.g., "\`\`\`json")
- 2. Set stop sequence to match closing delimiter (e.g., "\`\`\`")
- 3. Claude assumes it already wrote the opening, generates only the content, stops at closing delimiter
- Result: Raw structured data with no additional commentary.
- Example Flow:

### Prompt Evaluation

- Prompt Engineering = techniques for writing/editing prompts to help Claude understand requests and desired response format.
- Prompt Evaluation = automated testing of prompts using objective metrics to measure effectiveness.
- Three paths after writing a prompt:
- 1. Test once/twice, deploy to production (trap)
- 2. Test with custom inputs, minor tweaks for corner cases (trap)
- 3. Run through evaluation pipeline for objective scoring (recommended)
- Options 1 and 2 are common traps - engineers don't test prompts sufficiently before production use.
- Best practice = Use evaluation pipeline to get objective performance scores, then iterate on prompt based on results before deployment.

### A Typical Eval Workflow

- Typical Eval Workflow = 5-step iterative process for prompt optimization
- Step 1: Initial Prompt Draft = Write basic prompt with input variables (example: "Please answer the user's question [user_input]")
- Step 2: Evaluation Dataset = Create collection of test inputs (3 examples minimum, real-world uses hundreds/thousands). Can be hand-crafted or AI-generated.
- Step 3: Prompt Execution = Feed each dataset input through prompt template to create complete prompts, then send to Claude for responses.
- Step 4: Grading = Use grader system to score each question-answer pair (typically 1-10 scale). Average all scores for overall prompt performance metric.
- Step 5: Iteration = Modify prompt based on results, repeat entire process, compare scores to determine better version.
- Key Principles:
- No standardized methodology across industry

### Generating Test Datasets

- Custom Prompt Evaluation Workflow = Building system to evaluate AWS code generation prompts
- Goal = Help users write AWS-specific code by outputting one of three formats: Python, JSON configuration, or raw regular expressions
- Prompt Structure = "Please provide a solution to the following task: [user task]" with no additional explanation/headers/footers
- Test Dataset = Array of JSON objects with "task" property describing desired AWS tasks
- Dataset Generation Methods = Manual assembly or automatic generation using Claude Haiku (faster model recommended)
- Implementation Process:
- 1. Create generate_dataset() function with large prompt asking Claude to generate test cases
- 2. Use pre-filling technique with assistant message starting "\`\`\`json"

### Running the Eval

- Test case = individual record from generated dataset that gets merged with prompt and fed to Claude
- run_prompt function = takes test case, merges with prompt (simple "please solve the following task" + test case), sends to Claude, returns output. Currently lacks formatting instructions so returns verbose output.
- run_test_case function = takes individual case, calls run_prompt, grades result (currently hardcoded score of 10), returns dictionary with output/test case/score.
- run_eval function = loads dataset, loops through each test case calling run_test_case, assembles all results into list.
- Eval pipeline workflow = dataset → merge with prompt → send to Claude → grade results → collect outputs
- Current limitations = no grading logic implemented (hardcoded scores), no output formatting instructions in prompt, relatively slow execution time (31 seconds with Haiku model).
- Results format = array of objects containing Claude output, original test case, and score for each test case.
- Next step = implement actual graders to replace hardcoded scoring system.

### Model Based Grading

- Model Based Grading = using AI models to evaluate outputs from other AI models by providing objective scoring signals
- Three grader types:
- Code graders = programmatic checks (length, syntax, readability, word presence)
- Model graders = additional API calls to evaluate quality, instruction following, completeness
- Human graders = manual evaluation (flexible but time-consuming)
- Key requirements:
- All graders must return objective signals (typically 1-10 scores)
- Define evaluation criteria upfront

### Code Based Grading

- Code Based Grading = system to validate model outputs contain only valid code (Python/JSON/RegEx) without explanations
- Core Components:
- validate_json() = tries JSON parsing, returns 10 if valid, 0 if error
- validate_python() = tries AST parsing, returns 10 if valid, 0 if error
- validate_regex() = tries regex compilation, returns 10 if valid, 0 if error
- grade_syntax() = dispatcher function that calls appropriate validator based on test case format
- Implementation Steps:
- 1. Add validator functions that attempt parsing/compilation

### Prompt Engineering

- Prompt Engineering = improving prompts to get more reliable, higher quality outputs from language models.
- Goal: Generate one-day meal plans for athletes based on height, weight, physical goal, and dietary restrictions.
- Process:
- 1. Write initial prompt (poor first attempt)
- 2. Evaluate prompt performance
- 3. Apply prompt engineering techniques iteratively
- 4. Re-evaluate after each improvement
- 5. Monitor performance improvements

### Being Clear and Direct

- Being Clear and Direct = technique for improving prompt effectiveness by focusing on the first line of prompts.
- First line importance = most critical part of prompt that sets the foundation for AI response.
- Structure = use action verb + simple direct language + clear task description.
- Action verbs = write, generate, create, identify, analyze - tells AI exactly what to do.
- Task specification = include details about expected output format and content requirements.
- Examples:
- "Write three paragraphs about how solar panels work" = action verb + output format + topic
- "Identify three countries that use geothermal energy and for each include generation stats" = action verb + quantity + specific requirements

### Being Specific

- Being Specific = adding guidelines or steps to direct model output in particular direction
- Two types of guidelines:
- Type A: Control output attributes (length, structure, qualities)
- Type B: Provide steps for model to follow (forces consideration of specific elements, improves reasoning quality)
- Both types often combined in professional prompts.
- When to use:
- Type A: Almost always - list desired output qualities
- Type B: Complex problems requiring broader consideration of viewpoints/data beyond model's natural scope

### Structure with XML Tags

- XML Tags for Prompt Structure = technique to organize and clarify different content sections within prompts using custom XML-style tags.
- Purpose = helps language models distinguish between different types of interpolated content when large amounts of text are inserted into prompts.
- Implementation = wrap content sections with descriptive tags like    or    rather than dumping raw text.
- Tag naming = use specific, descriptive names (sales_records > records > data) to provide context about content nature.
- Use cases = separating code from documentation, marking athlete information, organizing sales data, any scenario with multiple content types in single prompt.
- Benefits = reduces ambiguity about what text serves what purpose, improves model comprehension of prompt structure, can lead to quality improvements especially with simpler models.
- Best practice = even for shorter content sections, XML tags can clarify that content represents external input or specific information categories.

### Providing Examples

- One-shot/multi-shot prompting = providing examples within prompts to guide model behavior. One-shot = single example, multi-shot = multiple examples.
- Implementation = wrap examples in XML tags with sample input and ideal output sections. Structure clearly separates example content from main prompt.
- Corner cases = use multi-shot prompting to handle edge cases like sarcasm detection. Add context explaining why specific scenarios need special attention.
- Complex outputs = examples especially effective for demonstrating intricate JSON structures or formatting requirements.
- Prompt evaluation integration = extract high-scoring test cases from evaluation results to use as examples. Include reasoning explanation of why output is ideal to reinforce desired behavior patterns.
- Effectiveness = consistently improves model performance by providing concrete behavioral templates and output format guidance.

### Introducing Tool Use

- Tool use = mechanism allowing Claude to access external information beyond its training data
- Core limitation: Claude only knows information from training data, lacks real-time/current information
- Tool use flow:
- 1. Send initial request to Claude + instructions for external data access
- 2. Claude determines if external data needed, requests specific information
- 3. Server runs code to fetch requested data from external sources
- 4. Send follow-up request to Claude with retrieved data
- 5. Claude generates final response using original prompt + external data

### Project Overview

- Project goal = teach Claude to set time-based reminders via tools in Jupyter notebook
- Target interaction = user says "Set reminder for doctor's appointment, week from Thursday" → Claude responds "I will remind you at that point in time"
- Three core problems identified:
- 1. Claude lacks precise current time knowledge (knows date, not exact time)
- 2. Claude sometimes fails at time-based calculations (e.g., "379 days from January 13th, 1973")
- 3. Claude has no mechanism to actually set reminders (understands concept but cannot execute)
- Solution approach = three dedicated tools:
- 1. Get current datetime tool (date + time)

### Tool Functions

- Tool Functions = Python functions executed automatically when Claude needs extra information to help users
- Key Components:
- Tool function = plain Python function that retrieves specific data (e.g., current datetime, weather)
- Executed when Claude determines it needs additional information to answer user queries
- Best Practices:
- 1. Use descriptive function/argument names
- 2. Validate inputs and raise errors for invalid data
- 3. Include meaningful error messages that help Claude correct mistakes

### Tool Schemas

- Tool Schemas = JSON configuration objects that describe tool functions for language models
- JSON Schema = data validation specification (not LM-specific) used to validate JSON data. LM community adopted it for tool calling because it's widely understood and convenient.
- Tool Schema Structure:
- name: tool function name
- description: 3-4 sentences explaining what tool does, when to use, what data it returns
- input_schema: actual JSON schema describing function arguments (type, description for each parameter)
- Best Practice: Use 3-4 sentence descriptions for both tool and individual arguments to help Claude understand purpose and usage.
- Schema Generation Trick: Ask Claude to write JSON schema for your function + attach Anthropic tool use documentation for best practices. Results in high-quality schemas.

### Handling Message Blocks

- **Step 3: Calling Claude with Tool Schema**
- API Request Structure = Include tools parameter with JSON schema list to inform Claude of available tools
- **Multi-Block Message Response**
- Message Content Types = Text blocks (user display) + Tool use blocks (function calls)
- Tool Use Block Contents = Function name + input arguments for execution
- **Critical Message History Management**
- Conversation Persistence = Manual tracking required - Claude stores no history
- Multi-Block Handling = Must preserve entire content list including all blocks (text + tool use) when appending to message history

### Sending Tool Results

- Step 4: Execute tool function that Claude requested. Extract arguments from tool use block using response.content[1].input, then call function with **kwargs syntax to convert dictionary to keyword arguments.
- Step 5: Send follow-up request to Claude with full conversation history plus new user message containing tool result block.
- Tool result block structure:
- tool_use_id = matches ID from original tool use block (enables Claude to match requests to results when multiple tools called)
- content = tool function output converted to string
- is_error = false (default, set true if tool execution failed)
- Tool use ID system: When Claude makes multiple tool calls, each gets unique ID. Tool results must reference matching IDs so Claude can correlate which result belongs to which request.
- Complete flow: Original user message → Assistant message with tool use block → Execute tool function → User message with tool result block → Final assistant response using tool output.

### Multi-Turn Conversations with Tools

- Multi-Turn Tool Conversations = system allowing AI to make multiple sequential tool calls within single conversation
- Problem: Users submit queries requiring multiple tools. Example: "What day is 103 days from today?" needs get_current_datetime tool, then add_duration_to_datetime tool.
- Process Flow:
- 1. Claude requests first tool (get_current_datetime)
- 2. System executes tool, returns result
- 3. Claude requests second tool (add_duration_to_datetime)
- 4. System executes tool, returns result
- 5. Claude provides final answer

### Implementing Multiple Turns

- Multiple Turns = Loop that keeps calling Claude until it stops requesting tools, indicated by stop_reason field
- Stop Reason = Field in Claude's response indicating why text generation stopped. "tool_use" value means Claude wants to call a tool.
- Run Conversation Function = Main loop that:
- 1. Calls Claude with messages + available tools
- 2. Adds assistant response to message history
- 3. Checks stop_reason - if not "tool_use", breaks loop
- 4. If tool_use, calls run_tools function
- 5. Adds tool results as user message

### Using Multiple Tools

- Adding multiple tools to Claude involves updating two key functions after implementing tool schemas and functions.
- **Process:**
- 1. Add tool schemas to tools list in RunConversation function
- 2. Add corresponding function calls to RunTool function using if/elif statements
- 3. Tool functions execute and return results when Claude requests them
- **Example Implementation:**
- RunTool checks tool_name, calls appropriate function with **tool_input
- Pattern: if tool_name == "ToolName": return ToolFunction(**tool_input)

### The Batch Tool

- Batch Tool = workaround to make Claude call multiple tools in parallel within single Assistant message
- Problem: Claude can technically send multiple tool use blocks in one response but rarely does so in practice. Instead sends separate sequential Assistant messages with single tool uses, creating unnecessary request rounds.
- Solution: Implement batch tool that acts as abstraction layer. Claude calls batch tool instead of individual tools directly.
- Batch Tool Schema: Takes "invocations" parameter = list of objects, each representing another tool to call (tool name + arguments)
- Implementation:
- Add batch tool to available tools list
- When Claude calls batch tool, extract invocations list
- Iterate through each invocation, parse JSON arguments, call run_tool() for each

### Tools for Structured Data

- Tools for Structured Data:
- Alternative method to extract structured JSON from Claude using tools instead of message pre-fill/stop sequences. More reliable but more complex setup.
- Core concept: Create JSON schema spec for tool where inputs match desired output structure. Claude calls tool with structured arguments containing extracted data.
- Workflow:
- 1. Write prompt asking Claude to analyze data and call provided tool
- 2. Provide JSON schema defining tool inputs (matches desired output structure)
- 3. Claude responds with tool_use block containing structured arguments
- 4. Extract JSON from tool arguments - no tool_result response needed

### The Text Edit Tool

- Text Editor Tool = Claude's built-in tool for file/text manipulation with wide text editor capabilities (open/read files, edit ranges, add/replace text, create files, undo).
- Only JSON schema built into Claude, not implementation. Developers must write tool function implementation to handle Claude's text editor requests.
- Schema stub required based on model version:
- Claude 3.7: specific date format
- Claude 3.5: different date format
- Small schema automatically expands to full schema in Claude.
- Capabilities = replicate code editor functionality (file operations, refactoring, testing file creation). Use cases = scenarios without access to full-featured code editors but need programmatic file manipulation.
- Implementation class needed with methods: view (file/directory contents), string_replace, create_file, etc.

### The Web Search Tool

- Web Search Tool = built-in Claude tool for searching web to find up-to-date/specialized information
- Key Implementation:
- Requires minimal schema: type="web_search_20250305", name="web_search", max_uses=5
- No custom implementation needed - Claude handles search execution
- max_uses = limit on total searches (single search can return multiple results)
- Response Structure:
- Text blocks = Claude's framing/answers
- Server tool use blocks = search query inputs

### Introducing Retrieval Augmented Generation

- RAG = Retrieval Augmented Generation, technique for querying large documents with LLMs.
- Problem: How to extract specific information from large documents (100-1000 pages) for LLM processing.
- Option 1 (Direct approach): Feed entire document text into prompt.
- Limitations: Token limits, decreased effectiveness with long prompts, higher cost, slower processing.
- Option 2 (RAG approach):
- Step 1: Break document into small chunks
- Step 2: Find most relevant chunks for user question, include only those in prompt
- RAG advantages: LLM focuses on relevant content, scales to large/multiple documents, smaller prompts = faster/cheaper processing.

### Text Chunking Strategies

- Text Chunking = process of dividing source documents into smaller text segments for RAG pipelines
- Core Problem: How text is chunked significantly impacts RAG quality. Poor chunking leads to wrong context retrieval (e.g., medical text about "bugs" retrieved for software engineering questions due to word overlap)
- Three Main Strategies:
- Size-based Chunking = dividing documents into equal-length strings
- Pros: easiest to implement, most common in production
- Cons: cuts off words mid-sentence, lacks context
- Solution: overlap strategy = include characters from neighboring chunks to preserve context
- Trade-off: creates text duplication but improves chunk meaning

### Text Embeddings

- Text Embeddings = numerical representation of meaning in text, generated by embedding models
- Embedding Model = takes text input, outputs long list of numbers (values range -1 to +1)
- Each Number = score representing some quality/feature of input text (actual qualities unknown but helpful to think as semantic features like happiness, topic relevance, etc.)
- Semantic Search = uses text embeddings to find related content by comparing numerical representations rather than exact word matches
- RAG Pipeline Process = extract text chunks → user submits query → find related chunks using embeddings → add as context to prompt
- Google's text-embedding-005 = specific embedding model available on Vertex AI for generating text embeddings
- Key Limitation = we don't know what each number in embedding actually represents, but can conceptualize them as semantic quality scores
- Implementation = use Google GenAI SDK, create client, pass text through model to get embedding vectors

### The Full RAG Flow

- RAG Pipeline = Complete flow from document processing to query response through embeddings and vector search.
- Step 1: Text Chunking = Split source documents into separate text pieces for processing.
- Step 2: Embedding Generation = Convert text chunks into numerical vectors using embedding models. Embeddings = numerical representations where each dimension captures semantic meaning.
- Step 3: Normalization = Scale embedding vectors to unit length (magnitude = 1.0), typically handled automatically by embedding APIs.
- Step 4: Vector Database Storage = Store normalized embeddings in specialized database optimized for numerical vector operations.
- Step 5: Query Processing = User submits question, gets embedded using same model as source documents.
- Step 6: Similarity Search = Vector database finds most similar stored embeddings to query embedding.
- Cosine Similarity = Measure of similarity between vectors, calculated as cosine of angle between them. Returns values -1 to 1, where 1 = very similar, -1 = very different.

### Implementing the Rag Flow

- RAG Flow Implementation = Complete workflow using vector database for document retrieval
- 5 Core Steps:
- 1. Text Chunking = Split document into sections using chunk_by_section function
- 2. Generate Embeddings = Create embeddings for each text chunk using generate_embedding
- 3. Vector Store Population = Create vector index instance, loop through chunk-embedding pairs, insert via store.add_vector with embedding + metadata dictionary containing original text
- 4. Query Processing = Generate embedding for user question using same generate_embedding function
- 5. Similarity Search = Use store.search(user_embedding, num_results) to find most relevant chunks, returns documents with cosine distances
- Key Technical Points:

### BM25 Lexical Search

- BM25 = Best Match 25, a lexical search algorithm used in RAG pipelines for text-based search complementing semantic search.
- Problem with semantic search alone: Can return irrelevant results despite good performance. Example: searching "incident 2023 Q4 011" returned correct section 10 but also irrelevant section 3 (financial analysis) that never mentions the incident.
- Solution approach: Hybrid search combining semantic search (embeddings + vector database) with lexical search (BM25) running in parallel, then merging results for better balance.
- BM25 algorithm steps:
- 1. Tokenize user query = break into individual terms by removing punctuation and splitting on spaces
- 2. Count term frequency = calculate how often each term appears across all text chunks
- 3. Assign importance weights = rare terms get higher importance, common terms (like "a") get lower importance
- 4. Rank chunks = prioritize chunks containing higher-weighted terms more frequently

### A Multi-Index Rag Pipeline

- Multi-Index RAG Pipeline = system combining semantic search (vector index) and lexical search (BM25 index) for improved retrieval accuracy.
- Core Architecture:
- Vector Index + BM25 Index = both have identical APIs (add_document, search methods)
- Retriever Class = wrapper that forwards queries to both indexes and merges results
- Unified Interface = enables easy addition of new search methodologies
- Reciprocal Rank Fusion = technique for merging results from different search methods:
- Formula: Score = sum of (1/(1+rank)) for each search method
- Process: collect all results → record ranks from each method → apply formula → sort by highest score

### Reranking Results

- Reranking = post-processing technique to improve retrieval accuracy by using an LLM to reorder search results based on relevance.
- Process: After hybrid retrieval (vector + BM25), pass top results to Claude with prompt asking to rank documents by relevance to user query. Claude returns reordered list with most relevant documents first.
- Implementation details: Use document IDs instead of full text for efficiency - assign random IDs to chunks, ask Claude to return ordered IDs rather than full content. Uses XML formatting for documents in prompt, JSON response with pre-fill and stop sequences.
- Trade-offs: Increases search accuracy but adds latency due to LLM call. Particularly effective when semantic understanding needed (example: "engineering team" query correctly prioritized software engineering section over cybersecurity).
- Prompt structure: User question + candidate documents + instruction to return N most relevant documents in decreasing relevance order.

### Contextual Retrieval

- Contextual Retrieval = RAG improvement technique that adds document context to text chunks before vector storage.
- Problem: Document chunking removes context from original source, reducing retrieval accuracy.
- Solution: Pre-processing step using LLM to generate contextual information for each chunk.
- Process:
- 1. Take individual chunk + original source document
- 2. Send to LLM (Claude) with prompt asking to situate chunk within larger document context
- 3. LLM generates brief contextual description
- 4. Combine generated context + original chunk = contextualized chunk

### Extended Thinking

- Extended Thinking = Claude feature that allows reasoning time before generating final response
- Key mechanics:
- Displays separate thinking process in chat UIs
- User charged for tokens generated during thinking phase
- Increases accuracy for complex tasks but adds cost and latency
- When to enable:
- Use prompt evals first
- Enable only when accuracy insufficient after prompt optimization efforts

### Image Support

- Claude Vision Capabilities = ability to send up to 100 images per request to Claude for analysis, comparison, counting, and other visual tasks.
- Technical Requirements = image size/dimension limits exist, images consume tokens based on pixel dimensions (height x width), costs calculated via specific equation.
- Image Integration = use image blocks in user messages containing either raw base64 image data or URLs to online images. Multiple image blocks allowed per message.
- Critical Success Factor = sophisticated prompting techniques essential for accurate results. Simple prompts typically fail.
- Prompting Techniques for Images = provide analysis steps, guidelines, one-shot/multi-shot examples. Structure prompts with specific sequential instructions rather than basic requests.
- Example Enhancement Methods =
- Step-by-step analysis (identify objects, count methodically, verify count with different strategy, compare results)
- One-shot prompting (show example image with correct answer, then present target image)

### PDF Support

- Claude PDF Support = ability to read and process PDF file content directly
- Implementation = nearly identical to image processing code with key changes:
- File type: "document" instead of "image"
- Media type: "application/pdf" instead of "image/png"
- Variable naming: file_bytes instead of image_bytes
- PDF capabilities = extract text, images, charts, tables, and other document elements
- Usage pattern = attach PDF file, modify existing image processing code with type/media changes, send to Claude with text prompt
- Key benefit = single tool for comprehensive PDF content extraction and analysis

### Citations

- Citations = Claude feature allowing AI to reference specific source documents when generating responses
- Citation purpose = Inform users that AI response comes from actual source rather than just AI memory/training
- Citation types:
- Citation page location = For PDF documents, includes cited text + document index + document title + start/end pages
- Citation char location = For plain text, includes character position within text block
- Implementation = Add citations field with enabled:true to API request along with source document
- Response structure = Content becomes list of text blocks, some containing citations arrays with location data
- User interface benefit = Build popups/overlays showing users exactly which source text supports each AI statement

### Prompt Caching

- Prompt caching = feature that speeds up Claude's response and reduces text generation costs by reusing computational work from previous requests.
- Normal request process: User sends message → Claude performs extensive internal calculations on input → generates output → discards all computational work → ready for next request.
- Problem: When follow-up requests contain previously seen messages, Claude must redo identical calculations it already performed and discarded.
- Solution: Prompt caching stores computational work in temporary data store instead of discarding it. When identical input appears in subsequent requests, Claude reuses cached calculations rather than recomputing them.
- Benefits: Faster response times, lower costs due to avoiding redundant processing of repeated content.
- Key requirement: Input text must be exactly identical to previously cached content for reuse to occur.

### Rules of Prompt Caching

- Prompt Caching = system where Claude saves processing work from initial request to reuse in follow-up requests with identical content
- Cache Duration = 5 minutes temporary storage
- Activation = manual cache breakpoint required in message blocks, not enabled by default
- Text Block Format = must use longhand format {type: "text", text: "content", cache_control: {...}} instead of shorthand string assignment to add cache control
- Cache Scope = all content cached up to and including breakpoint, not content after breakpoint
- Content Identity Rule = follow-up requests must have identical content up to breakpoint or cache invalidated
- Breakpoint Locations = text blocks, image blocks, tool use, tool results, tool schemas, system prompts
- Processing Order = tools → system prompt → messages (joined together behind scenes)

### Prompt Caching in Action

- Prompt Caching Implementation:
- Cache Breakpoints = multiple cache points in single request (tools + system prompt + messages)
- Tool Schema Caching:
- Add cache_control field to LAST tool schema only
- Best practice = copy tools list first, clone last tool, add cache_control type="ephemeral"
- Prevents accidental modification of original tool schemas
- System Prompt Caching:
- Convert system string to list with text block containing cache_control type="ephemeral"

### Introducing MCP

- MCP = Model Context Protocol, communication layer providing Claude with context and tools without requiring developers to write tedious code.
- MCP Architecture = client-server model where server contains tools, resources, and prompts.
- Primary Problem Solved = shifts burden of defining and running tools from developer's server to MCP server. Instead of authoring tool schemas and functions yourself, MCP server handles this.
- MCP Server = interface to outside service (like GitHub) that wraps functionality into pre-built tools. Eliminates need for developers to author/maintain tool implementations.
- Who Creates MCP Servers = anyone, but often service providers make official implementations (e.g., AWS releasing their own MCP server).
- MCP vs Direct API Calls = MCP saves development time by providing pre-built tool schemas and function implementations rather than requiring custom authoring.
- MCP vs Tool Use = complementary concepts, not identical. MCP focuses on who does the work (pre-built vs custom), while both involve tool usage. Common misconception stems from not understanding MCP's delegation aspect.
- Key Benefit = reduces developer burden of creating/maintaining integrations for complex services with extensive functionality.

### MCP Clients

- MCP Client = communication interface between your server and MCP server, provides access to server's tools
- Transport agnostic = client/server can communicate via multiple protocols (stdin/stdout, HTTP, WebSockets, etc.)
- Communication method = message exchange following MCP spec
- Key message types:
- list tools request = client asks server for available tools
- list tools result = server responds with tool list
- call tool request = client asks server to run specific tool with arguments
- call tool result = server returns tool execution results

### Project Setup

- Project Setup = CLI-based chatbot implementation to understand MCP client-server interaction
- Components = MCP client + custom MCP server in single project
- Documents = fake documents stored in memory only
- Server tools = read document contents, update document contents
- Important note = typically projects implement either client OR server, not both. This project does both for learning purposes.
- Setup steps:
- Download CLI project.zip starter code
- Extract and open in code editor

### Defining Tools with MCP

- MCP Server Implementation = Creating server with Python SDK using single line of code (mcp package)
- Tool Definition Syntax = Use @mcp.tool decorator with name, description, and typed arguments instead of manual JSON schemas
- Python MCP SDK Benefits = Auto-generates JSON schemas from decorators and field types, eliminates manual schema writing
- Example Tools Created = read_doc_contents (takes doc_id string, returns document content from in-memory docs dictionary) and edit_document (takes doc_id, old_string, new_string for find/replace operations)
- Tool Structure = Decorator specifies metadata, function implements logic, Field() from pydantic adds argument descriptions
- Error Handling = Check if doc_id exists in docs dictionary, raise ValueError if not found
- Document Storage = In-memory dictionary with doc IDs as keys, content as values
- Implementation Pattern = @mcp.tool decorator → function definition → typed parameters with Field descriptions → validation logic → core functionality

### The Server Inspector

- MCP Inspector = in-browser debugger for testing MCP servers without connecting to applications
- Access: Run \`mcp dev [server-file.py]\` in terminal with Python environment activated → generates local server URL → open in browser
- Key features:
- Connect button = starts MCP server
- Top menu bar = shows resources, prompts, tools sections
- Tools section = lists available tools from server
- Right panel = manual tool invocation interface
- Testing workflow:

### Implementing a Client

- MCP Client Implementation:
- MCP Client = wrapper class around client session for resource management and cleanup
- Client Session = actual connection to MCP server from Python SDK, requires resource cleanup
- Client Purpose = exposes server functionality to codebase, bridges server tools to application code
- Key Functions:
- list_tools() = await self.session.list_tools(), returns result.tools
- call_tool() = await self.session.call_tool(tool_name, tool_input), executes specific tool with Claude-provided parameters
- Implementation Pattern:

### Defining Resources

- MCP Resources = mechanism for MCP servers to expose data to clients for read operations
- Resource Types:
- Direct/Static Resources = fixed URI, always same address (e.g., docs://documents)
- Templated Resources = parameterized URI with wildcards (e.g., documents/{doc_id})
- Resource Flow:
- 1. Client sends read resource request with URI to MCP server
- 2. Server matches URI to defined resource function
- 3. Server executes function and returns data via read resource result

### Accessing Resources

- MCP Resource Access Implementation:
- Resource fetching = MCP client function reads resources from MCP server by URI, parses content based on MIME type, returns data
- Key imports = json module, AnyURL from pydantic for type handling
- Function flow = await self.session.read_resource(AnyURL(uri)) → extract first content from results.contents[0] → check MIME type → parse accordingly
- Content parsing logic = if resource is TextResourceContents and mime_type == "application/json" → return json.loads(resource.text), else return resource.text as plain text
- Response structure = result.contents list containing resource objects with type and mime_type properties
- Integration = read_resource function called by other application components to fetch document contents for prompts
- Testing workflow = CLI shows resource list → user selects with arrow keys/space → resource content sent directly to Claude in prompt without requiring tool calls

### Defining Prompts

- MCP Prompts = pre-defined, tested prompts exposed by MCP servers for specialized tasks
- Purpose = Allow server authors to create high-quality, domain-specific prompts rather than users writing generic prompts manually
- Implementation:
- Use @prompt decorator with name and description
- Function receives parameters (like document ID)
- Returns list of messages (user/assistant format)
- Import: from mcp.server.fastmcp.prompts import BaseMessage
- Example structure:

### Prompts in the Client

- **Prompts in MCP Client Implementation**
- Client-side prompt functions:
- \`list_prompts()\` = await self.session.list_prompts(), return result.props
- \`get_prompt()\` = await self.session.get_prompt(prompt_name, arguments), return result.messages
- **Prompt workflow:**
- 1. Define prompt in MCP server with variables (e.g., document_id)
- 2. Client calls get_prompt with prompt name + arguments dictionary
- 3. Arguments interpolated into prompt function as keyword arguments

### MCP Review

- MCP Server Primitives = three core components with distinct control patterns and purposes.
- Tools = model-controlled actions. Claude decides when to execute based on conversation needs. Purpose: add capabilities to AI model (e.g., JavaScript execution for calculations). Implementation: define tools in MCP server for model consumption.
- Resources = app-controlled data access. Application code decides when to fetch and use data. Purpose: provide data for UI elements or prompt augmentation (e.g., autocomplete options, document listings, Google Drive integration). Implementation: fetch resources to populate app interfaces.
- Prompts = user-controlled workflows. Users trigger through UI buttons, menu options, or slash commands. Purpose: implement predefined workflows and optimized conversation starters. Implementation: create prompt templates for common user actions.
- Control Pattern Summary:
- Tools serve the model
- Resources serve the app
- Prompts serve the users

### Agents and Workflows

- Workflows and agents = strategies for handling user tasks that can't be completed by Claude in a single request.
- Decision rule: Use workflows when you know exact task steps ahead of time. Use agents when task details are uncertain.
- Workflow = series of calls to Claude for specific problems where all steps are predetermined and plannable.
- Agent = letting Claude figure out how to complete tasks using provided tools (like the tools examples in previous course modules).
- Example workflow: Image-to-3D model converter
- Step 1: Claude describes uploaded metal part image in detail
- Step 2: Claude uses CADQuery Python library to create 3D model from description
- Step 3: Generate rendering of model as image

### Parallelization Workflows

- Parallelization Workflows = breaking one complex task into multiple parallel subtasks, then aggregating results
- Core Pattern:
- Split complex analysis into specialized parallel requests
- Each subtask focuses on one specific aspect
- Aggregator step combines all results into final output
- Example Implementation:
- Original approach: single large prompt asking Claude to analyze image and recommend best material (metal/polymer/ceramic/etc.)
- Parallelized approach: separate simultaneous requests, each evaluating image suitability for ONE material type

### Chaining Workflows

- Chaining Workflows = breaking large tasks into sequential distinct steps rather than single complex prompts.
- Key structure: One main task → Multiple sequential subtasks → Each step feeds into next step.
- Example workflow: User topic input → Twitter trending search → Claude selects best topic → Claude researches topic → Claude writes script → AI creates video → Post to social media.
- Primary benefit = allows AI to focus on one task at a time rather than juggling multiple requirements simultaneously.
- Critical use case: Large prompts with many constraints where AI consistently violates some requirements despite repeated instructions.
- Solution pattern:
- 1. Send initial complex prompt with all constraints
- 2. Accept imperfect output that violates some constraints

### Routing Workflows

- Routing Workflows = workflow pattern that categorizes user input to determine appropriate processing pipeline
- Process:
- 1. User provides input/topic
- 2. Routing step = AI call to categorize input into predefined genres/categories
- 3. Based on category, input gets forwarded to specialized processing pipeline
- 4. Each pipeline has customized prompts/tools for that category type
- Example: Social media video script generation
- Programming topic → Educational category → Educational script prompt (clear explanations, definitions, examples)

### Agents and Tools

- Agents = AI systems that use tools to complete tasks when exact steps are unknown, unlike workflows which need precise predetermined steps.
- Key difference: Workflows = known step sequences, Agents = flexible tool combination for unknown step sequences.
- Agent advantages: Flexibility to solve wide variety of tasks using same toolset. Claude creates plans dynamically using available tools.
- Tool abstraction principle: Agents need abstract/general tools rather than hyper-specialized ones. Example: Claude code uses bash, web fetch, file write (abstract) rather than specific refactor or install tools.
- Tool combination examples: With get_current_datetime, add_duration, set_reminder tools, Claude can handle "what time is it" (single tool) or "remind me gym next Wednesday" (multiple tools + planning).
- Dynamic interaction capability: Agents can request additional user information when needed, like asking warranty purchase date to calculate expiration.
- Best practice: Provide small set of abstract tools that can be combined creatively rather than many specialized single-purpose tools.
- Real example: Social media video agent with bash/FFmpeg, generate_image, text_to_speech, post_media tools enables both simple "create video" and complex "generate sample cover first for approval" workflows.

### Environment Inspection

- Environment Inspection = agents examining their environment state after (or before) taking actions to understand results and progress.
- Core concept: Agents need feedback beyond tool return values to understand action outcomes and current state.
- Computer use example: Claude takes screenshot after every action (typing, clicking) because it cannot predict how actions change the environment. Button clicks might navigate pages or open menus - screenshot reveals new state.
- Code editing example: Before modifying files, agents must read current file contents to understand existing state.
- Social media video agent applications:
- Use Whisper CPP via bash tool to generate timestamped captions, verify audio placement
- Use FFmpeg to extract video screenshots at intervals, verify visual output
- Inspect generated videos to ensure task completion quality

### Workflows vs Agents

- Workflows = pre-defined series of calls to Claude for tasks with known step sequences. Agents = flexible systems using basic tools that Claude combines creatively for unknown tasks.
- Key differences:
- Task approach: Workflows divide big tasks into smaller, specific subtasks for focused execution. Agents handle varied challenges through creative tool combination.
- Accuracy: Workflows achieve higher accuracy due to focused, specific steps. Agents have lower successful completion rates due to delegated complexity.
- Testing: Workflows easier to test/evaluate with known step sequences. Agents harder to test due to unpredictable execution paths.
- Flexibility: Workflows require specific inputs, fixed sequences. Agents adapt to varied user queries, can request additional input, flexible UX.
- Reliability: Workflows more reliable for consistent task completion. Agents more experimental but less dependable.
- Recommendation: Prioritize workflows when possible for reliable problem-solving. Use agents only when flexibility truly required. Users want 100% working products over fancy but unreliable agents.

## Preguntas de repaso

- Cual es el objetivo practico de este curso?
- Que conceptos o herramientas aparecen repetidamente?
- Que decisiones humanas no deberian delegarse por completo a la IA?
- Que evidencias o verificaciones exige el flujo de trabajo presentado?
- Que skill de LinkedIn representa mejor esta certificacion?
