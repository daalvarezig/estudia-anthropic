## Resumen

El **Model Context Protocol (MCP)** es un protocolo abierto que estandariza cómo las aplicaciones de IA (como Claude) se conectan con fuentes de datos externas, herramientas y sistemas. La idea central es resolver el problema "M×N": antes de MCP, cada aplicación de IA (M) necesitaba una integración a medida con cada herramienta o fuente de datos (N), multiplicando el trabajo de integración. MCP convierte ese problema en "M+N": cada herramienta expone un único servidor MCP y cada aplicación implementa un único cliente MCP, y todo se entiende entre sí mediante un protocolo común.

A menudo se describe MCP con la analogía del **"USB-C de las aplicaciones de IA"**: un conector universal entre modelos y el mundo exterior (archivos, bases de datos, APIs, herramientas internas). Fue presentado por Anthropic a finales de 2024 como estándar abierto, y se basa en **JSON-RPC 2.0** para la mensajería.

Esta guía está pensada para quien prepara la certificación oficial **"Introduction to Model Context Protocol (MCP)"** de Anthropic Academy: desarrolladores, ingenieros de IA y técnicos que quieran entender qué es MCP, su arquitectura, sus primitivas y cómo construir o consumir servidores y clientes MCP.

## Conceptos clave

- **Problema M×N vs M+N**: MCP estandariza las integraciones para que no haya que escribir una conexión específica por cada par (modelo, herramienta). Un servidor MCP sirve a cualquier cliente compatible.
- **Arquitectura cliente-servidor (host / client / server)**:
  - **Host**: la aplicación de IA que el usuario maneja (Claude Desktop, Claude Code, un IDE, una app propia). Contiene el LLM y orquesta.
  - **Client (cliente MCP)**: vive dentro del host; mantiene una conexión **1:1** con un servidor MCP y traduce entre el host y el servidor.
  - **Server (servidor MCP)**: programa ligero que expone capacidades (datos, herramientas, prompts) a través del protocolo. Un host puede tener varios clientes, cada uno conectado a un servidor distinto.
- **JSON-RPC 2.0**: formato de mensajes del protocolo. Se intercambian *requests*, *responses* y *notifications*. MCP define un ciclo de vida con **inicialización** (handshake con negociación de capacidades y versión del protocolo), operación y cierre.
- **Las tres primitivas del servidor**:
  - **Tools (herramientas)**: funciones ejecutables que el modelo puede invocar para *actuar* (consultar una API, escribir en una BD, enviar un email). Son **model-controlled**: el modelo decide cuándo llamarlas (con aprobación del usuario). Cada tool tiene nombre, descripción y un `inputSchema` en JSON Schema.
  - **Resources (recursos)**: datos de solo lectura que dan **contexto** al modelo (archivos, registros, contenido de una URI). Son **application-controlled**: la app decide cómo y cuándo exponerlos. Se identifican por URI.
  - **Prompts**: plantillas predefinidas y reutilizables de instrucciones/flujos. Son **user-controlled**: típicamente el usuario las invoca (p. ej. como slash commands).
- **Primitivas del cliente** (capacidades que el servidor puede pedir al cliente):
  - **Sampling**: el servidor solicita al host una *completion* del LLM, permitiendo comportamientos agénticos sin que el servidor tenga su propia clave de API. El host mantiene el control y puede revisar la petición.
  - **Roots**: el cliente informa al servidor de los límites del sistema de archivos o recursos sobre los que puede operar.
  - **Elicitation**: el servidor pide información adicional al usuario a mitad de una operación (añadido en revisiones recientes del protocolo).
- **Transportes**:
  - **stdio**: entrada/salida estándar, ideal para servidores locales que el host lanza como subproceso.
  - **Streamable HTTP** (con Server-Sent Events): transporte para servidores remotos. Sustituye al antiguo "HTTP+SSE" en revisiones recientes del protocolo.
- **Descubrimiento de capacidades**: tras la inicialización, el cliente consulta al servidor con métodos tipo `tools/list`, `resources/list`, `prompts/list`, y luego ejecuta con `tools/call`, `resources/read`, `prompts/get`.
- **SDKs oficiales**: existen SDKs en Python, TypeScript, Java/Kotlin, C#, entre otros, para construir clientes y servidores sin implementar el protocolo a mano.
- **Seguridad y consentimiento**: principio rector de MCP. El usuario debe consentir y entender qué datos se comparten y qué herramientas se ejecutan; las llamadas a tools requieren aprobación (human-in-the-loop). Riesgos a vigilar: inyección de prompts, herramientas maliciosas, exfiltración de datos.

## Que necesitas dominar para el certificado

- **Definición y propósito de MCP**: qué problema resuelve (M×N → M+N) y la analogía del USB-C. Saber que es un estándar **abierto** y que usa **JSON-RPC 2.0**.
- **Arquitectura y roles**: distinguir con claridad **host vs client vs server**, y recordar que la relación cliente↔servidor es **1:1**, mientras un host puede tener **varios** clientes.
- **Las tres primitivas del servidor y quién las controla**:
  - Tools → **model-controlled** (acciones).
  - Resources → **application-controlled** (contexto de solo lectura, por URI).
  - Prompts → **user-controlled** (plantillas).
  Es de lo más preguntado: asocia cada primitiva con su tipo de control y con un ejemplo.
- **Primitivas del cliente**: qué es **sampling** (servidor pide completion al host) y **roots**.
- **Ciclo de vida y mensajes**: inicialización con negociación de capacidades; métodos `*/list` y `*/call`/`*/read`/`*/get`.
- **Transportes**: cuándo usar **stdio** (local) y cuándo **Streamable HTTP/SSE** (remoto).
- **Construcción práctica**: cómo se ve un servidor mínimo (definir una tool con su esquema, registrar un resource) y cómo se conecta un host como Claude Desktop o Claude Code mediante un archivo de configuración.
- **Seguridad**: consentimiento del usuario, aprobación de tools, y los riesgos principales.

## Plan de estudio

1. **Fundamentos (1-2 h)**: lee la introducción oficial de MCP y la documentación de arquitectura. Memoriza host/client/server y el problema M+N. Escribe con tus palabras la diferencia entre las tres primitivas.
2. **Primitivas en profundidad (2 h)**: para tools, resources y prompts, anota: quién las controla, para qué sirven, y un ejemplo concreto. Haz lo mismo con sampling y roots. Crea una tabla mental.
3. **Manos a la obra: un servidor (2-3 h)**: usa el quickstart oficial y el SDK de Python o TypeScript para construir un servidor MCP mínimo con una tool (p. ej. "obtener el tiempo") y un resource. Esto fija los conceptos mucho mejor que solo leer.
4. **Conéctalo a un host (1 h)**: configura tu servidor en **Claude Desktop** o **Claude Code** editando el archivo de configuración (los `mcpServers`). Observa el handshake, el listado de tools y una llamada con su aprobación.
5. **Transportes y ciclo de vida (1 h)**: practica con stdio en local y revisa cómo sería un servidor remoto por Streamable HTTP. Repasa el flujo de inicialización.
6. **Seguridad (30 min)**: estudia el modelo de consentimiento y los riesgos (prompt injection, tools no fiables). Es tema de examen y de buenas prácticas reales.
7. **Repaso final**: usa estas flashcards y el test. Apúntate los fallos y vuelve a la sección correspondiente.

## Errores comunes y tips

- **Confundir host y client**: el *host* es la app completa (con el LLM); el *client* es el componente interno que habla con UN servidor. No son sinónimos.
- **Olvidar quién controla cada primitiva**: el error clásico es decir que las tools las controla el usuario. Las **tools** las decide el **modelo** (con aprobación humana); los **prompts** los invoca el **usuario**; los **resources** los gestiona la **aplicación**.
- **Creer que MCP es un producto de Anthropic cerrado**: es un **estándar abierto**; cualquiera puede crear servidores y clientes, y hay SDKs en varios lenguajes y adopción de múltiples empresas.
- **Pensar que el servidor MCP necesita su propia API key del LLM**: no necesariamente; con **sampling** puede pedir completions al host, que controla el acceso al modelo.
- **Mezclar transportes**: stdio es para local (subproceso); HTTP (Streamable HTTP/SSE) es para remoto. Recuerda que el transporte HTTP+SSE antiguo fue reemplazado por Streamable HTTP en revisiones recientes.
- **No mencionar el consentimiento**: en preguntas de seguridad, la respuesta correcta casi siempre gira en torno al **consentimiento explícito del usuario** y la **aprobación de cada llamada a tool**.
- **Tip**: recuerda "JSON-RPC 2.0" como el formato de mensajes; suele aparecer como opción correcta frente a REST, gRPC o GraphQL.
- **Tip**: la relación cliente-servidor es **1:1**; el host escala teniendo varios clientes, no metiendo varios servidores en un cliente.

## Puntos clave para recordar

- MCP = estándar **abierto** que conecta apps de IA con datos/herramientas; resuelve el problema **M×N → M+N**; "USB-C de la IA".
- Mensajería sobre **JSON-RPC 2.0**; ciclo de vida con inicialización y negociación de capacidades.
- Tres roles: **Host** (la app con el LLM), **Client** (1:1 con un servidor), **Server** (expone capacidades).
- Tres primitivas del servidor: **Tools** (model-controlled, acciones), **Resources** (application-controlled, contexto de solo lectura por URI), **Prompts** (user-controlled, plantillas).
- Primitivas del cliente: **Sampling** (servidor pide completion al host) y **Roots** (límites de acceso).
- Transportes: **stdio** (local) y **Streamable HTTP/SSE** (remoto).
- Descubrimiento y uso: `tools/list` + `tools/call`, `resources/list` + `resources/read`, `prompts/list` + `prompts/get`.
- SDKs oficiales en Python, TypeScript, Java/Kotlin, C#, etc.
- **Seguridad primero**: consentimiento explícito del usuario y aprobación human-in-the-loop de las herramientas.