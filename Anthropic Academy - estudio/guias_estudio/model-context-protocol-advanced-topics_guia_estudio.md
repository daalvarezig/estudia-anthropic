## Resumen

El **Model Context Protocol (MCP)** es un protocolo abierto que estandariza cómo las aplicaciones de IA (clientes/hosts) se conectan a fuentes de contexto y herramientas externas (servidores). En lugar de escribir un conector ad hoc por cada par modelo↔herramienta (el problema "M×N"), MCP define un contrato común: un servidor expone capacidades una vez y cualquier cliente compatible las consume. Piénsalo como el "USB-C de las aplicaciones de IA".

Esta guía cubre los **temas avanzados** de la certificación *MCP: Advanced Topics* de Anthropic Academy. Asume que ya conoces lo básico (qué es un servidor, qué es una herramienta) y se centra en lo que diferencia a un implementador competente: la capa de **transporte** y su evolución, las **primitivas del servidor y del cliente**, las características avanzadas (**sampling, roots, elicitation, progress, cancellation, logging**), **autenticación y autorización (OAuth 2.1)**, y los **patrones de seguridad** que el certificado pregunta. Va dirigida a desarrolladores y arquitectos que integran Claude (vía Claude Desktop, Claude Code, la API o el Agent SDK) con sistemas reales.

## Conceptos clave

- **Arquitectura host / cliente / servidor.** El *host* es la aplicación de IA (Claude Desktop, Claude Code, un IDE). Dentro del host viven uno o varios *clientes* MCP; cada cliente mantiene una conexión 1:1 con un *servidor*. El servidor expone contexto y capacidades. El modelo nunca habla directamente con el servidor: lo hace el cliente en su nombre.
- **JSON-RPC 2.0.** Toda la mensajería MCP es JSON-RPC 2.0: *requests* (con `id`, esperan respuesta), *responses* (resultado o error) y *notifications* (sin `id`, no esperan respuesta). Conocer esta distinción es clave para entender qué mensajes pueden fluir en cada dirección.
- **Ciclo de vida y negociación de capacidades.** La conexión empieza con `initialize`: cliente y servidor intercambian la versión del protocolo y declaran sus *capabilities*. Una parte no puede usar una característica que la otra no haya anunciado. Tras la respuesta, el cliente envía la notificación `initialized`. Esta negociación es el corazón de la interoperabilidad.
- **Primitivas del servidor: Tools, Resources, Prompts.**
  - **Tools** (controladas por el modelo): funciones que el modelo decide invocar; tienen efectos y devuelven resultados. Se anuncian con `tools/list` y se invocan con `tools/call`.
  - **Resources** (controlados por la aplicación): datos identificados por URI que el host expone como contexto (ficheros, filas de BD, respuestas de API). Soportan *resource templates* (URIs parametrizados) y suscripciones a cambios.
  - **Prompts** (controlados por el usuario): plantillas reutilizables que el usuario invoca explícitamente (p. ej. slash commands).
- **Primitivas del cliente: Sampling, Roots, Elicitation.**
  - **Sampling:** el *servidor* pide al *cliente* que ejecute una inferencia LLM (`sampling/createMessage`). Permite servidores "agénticos" sin tener su propia clave de API; el host mantiene el control y el humano puede aprobar.
  - **Roots:** el cliente informa al servidor de los límites del sistema de ficheros/URIs sobre los que debe operar.
  - **Elicitation:** el servidor solicita al usuario, a mitad de una operación, datos estructurados adicionales (un esquema JSON), p. ej. confirmaciones o parámetros que faltan.
- **Transportes.** **stdio** (proceso local; el cliente lanza el servidor y se comunican por stdin/stdout) y **Streamable HTTP** (remoto). Streamable HTTP **sustituyó** al antiguo *HTTP+SSE* (dos endpoints) por **un único endpoint** que admite respuestas JSON simples o streaming vía SSE cuando hace falta. Saber que SSE legacy quedó obsoleto es un punto típico de examen.
- **Autorización: OAuth 2.1.** Para servidores remotos, MCP define un flujo basado en OAuth 2.1 con PKCE obligatorio. El servidor MCP actúa como *resource server*; usa *Protected Resource Metadata* (RFC 9728) para apuntar al *authorization server*, y se apoya en *Authorization Server Metadata* y *Dynamic Client Registration*. Los tokens viajan en `Authorization: Bearer`.
- **Características operativas:** **progress** (notificaciones de avance con `progressToken`), **cancellation** (cancelar requests en curso), **logging** (el servidor envía logs estructurados con nivel), **pagination** (cursores en los `*/list`), y **completion** (autocompletado de argumentos de prompts/resources).
- **Seguridad y confianza.** Riesgos: ejecución de herramientas no segura, *tool poisoning* (descripciones maliciosas), *confused deputy* en proxies OAuth, *prompt injection* a través del contenido devuelto. Mitigaciones: consentimiento humano explícito, mínimo privilegio, validación de entradas/salidas, tratar el contenido de resources como no confiable, y validar `Origin` / usar tokens de sesión en transporte HTTP.

## Qué necesitas dominar para el certificado

1. **Mapa de mensajes por dirección.** Saber quién inicia cada método: `tools/*`, `resources/*`, `prompts/*` los pide el cliente; `sampling/createMessage`, `elicitation/create` y `roots/list` los pide el servidor (o el servidor consulta al cliente). Es la pregunta tipo "¿quién llama a quién?".
2. **Negociación de capacidades en `initialize`.** Qué se intercambia, por qué una característica no usada no se anuncia, y el papel de la notificación `initialized`.
3. **Las tres primitivas del servidor y su modelo de control** (model-controlled vs app-controlled vs user-controlled) y las tres del cliente.
4. **Transportes:** diferencias stdio vs Streamable HTTP, por qué se abandonó HTTP+SSE, cuándo se usa SSE dentro de Streamable HTTP, y gestión de sesión (`Mcp-Session-Id`).
5. **OAuth 2.1 para servidores remotos:** rol de PKCE, los documentos de *metadata*, *Dynamic Client Registration*, y el flujo de descubrimiento del authorization server.
6. **Sampling y elicitation a fondo:** cuándo un servidor los usa, por qué mantienen al humano en el bucle, y qué control conserva el host.
7. **Seguridad:** vectores de ataque y mitigaciones; el principio de consentimiento del usuario antes de ejecutar herramientas o exponer datos.

## Plan de estudio

1. **Lee la especificación MCP** por secciones: Architecture → Base Protocol (lifecycle, transports, JSON-RPC) → Server Features → Client Features → Security. No memorices JSON; entiende el *flujo*.
2. **Levanta un servidor stdio** con el SDK (Python o TypeScript) que exponga una Tool, un Resource y un Prompt. Conéctalo a Claude Desktop o Claude Code y observa los mensajes.
3. **Usa MCP Inspector** para ver en vivo `initialize`, `tools/list`, `tools/call`, paginación y logs. Ver los frames JSON-RPC fija los conceptos mejor que leerlos.
4. **Migra ese servidor a Streamable HTTP** y añade OAuth 2.1. Aquí aprendes metadata, PKCE y manejo de sesión "tocando hierro".
5. **Implementa una característica avanzada:** un servidor que use *sampling* para resumir, o *elicitation* para pedir confirmación, con *progress* y *cancellation*.
6. **Repasa seguridad:** recorre cada vector (tool poisoning, confused deputy, prompt injection) y escribe la mitigación de cada uno.
7. **Autoevaluación:** usa flashcards y el quiz de abajo; vuelve a la spec en cada fallo.

## Errores comunes y tips

- **Confundir quién inicia sampling.** Lo pide el **servidor** al **cliente**, no al revés. El servidor no tiene su propio LLM; pide prestada la inferencia del host.
- **Creer que SSE es el transporte remoto actual.** El transporte remoto vigente es **Streamable HTTP** (un endpoint); HTTP+SSE de dos endpoints es legacy. SSE sigue existiendo *dentro* de Streamable HTTP como mecanismo de streaming opcional.
- **Mezclar Tools y Resources.** Tools = acciones que el modelo decide (con efectos). Resources = datos que la aplicación expone como contexto. Prompts = plantillas que el usuario invoca.
- **Olvidar la negociación de capacidades.** Si una parte no anuncia una capability, la otra no puede usarla; no asumas que está disponible.
- **Saltarse PKCE u OAuth 2.1.** Para servidores remotos, PKCE es obligatorio; no es OAuth 2.0 "a secas".
- **Tratar el contenido de un resource como confiable.** Puede contener prompt injection; el host debe tratarlo como entrada no confiable y mantener consentimiento humano.
- **Tip de transporte:** stdio para servidores locales/del mismo equipo; Streamable HTTP para servidores remotos o multiusuario.

## Puntos clave para recordar

- MCP estandariza el contexto IA↔herramientas (resuelve el problema M×N); mensajería sobre **JSON-RPC 2.0**.
- Arquitectura **host → cliente(s) → servidor**, conexión cliente↔servidor **1:1**.
- Primitivas del **servidor**: **Tools** (modelo), **Resources** (app), **Prompts** (usuario).
- Primitivas del **cliente**: **Sampling**, **Roots**, **Elicitation** (las inicia el servidor hacia el cliente).
- El ciclo de vida arranca con **`initialize`** + **negociación de capacidades** y la notificación **`initialized`**.
- Transportes: **stdio** (local) y **Streamable HTTP** (remoto, un endpoint); **HTTP+SSE legacy quedó obsoleto**.
- Autorización remota = **OAuth 2.1 + PKCE** con *Protected Resource Metadata* y *Dynamic Client Registration*.
- Características operativas: **progress, cancellation, logging, pagination, completion**.
- Seguridad: **consentimiento humano**, mínimo privilegio, contenido externo no confiable; cuidado con **tool poisoning**, **confused deputy** y **prompt injection**.
