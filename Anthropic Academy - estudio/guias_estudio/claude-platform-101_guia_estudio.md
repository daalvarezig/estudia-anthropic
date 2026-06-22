## Resumen

**Claude Platform 101** es la certificación introductoria oficial de Anthropic Academy para desarrolladores y equipos técnicos que empiezan a construir aplicaciones sobre la plataforma de Claude. Su objetivo no es enseñarte a "chatear" con Claude, sino a integrarlo de forma programática: la API de Mensajes (Messages API), los SDKs oficiales, el uso de herramientas (tool use), MCP, los agentes, y las opciones de despliegue en proveedores cloud (Amazon Bedrock, Google Vertex AI, Claude Platform on AWS).

Está pensada para perfiles que ya saben programar y quieren dominar los fundamentos correctos antes de pasar a certificaciones más avanzadas. Si tu trabajo consiste en montar bots, asistentes, pipelines de extracción o agentes (justo el tipo de cosas que se construyen en un negocio real de IA), esta es la base sobre la que se apoya todo lo demás. Aprobarla demuestra que entiendes **cómo se estructura una petición, cómo se eligen modelos, cómo se controla el coste y cómo se escala de una llamada simple a un agente completo**.

La filosofía central que evalúa el examen es: **empieza por lo simple y sube de nivel solo cuando la tarea lo exige**. Una sola llamada resuelve la mayoría de casos; los workflows con tool use cubren los multi-paso; los agentes son para tareas abiertas donde el modelo decide su propia trayectoria.

## Conceptos clave

- **Messages API (`POST /v1/messages`)**: el único endpoint central. Todo pasa por aquí: texto, visión, herramientas, salidas estructuradas y pensamiento. Tool use y output constraints no son APIs separadas, son parámetros de esta misma llamada. La API es **stateless**: en cada petición envías el historial completo de la conversación; el servidor no recuerda nada entre llamadas.

- **Familia de modelos**: Anthropic ofrece tres tamaños con distinto equilibrio coste/capacidad/velocidad. La regla práctica: **Opus** para tareas complejas y razonamiento profundo, **Sonnet** para el mejor equilibrio velocidad/inteligencia en producción de alto volumen, y **Haiku** para tareas simples y sensibles a latencia (clasificación, etiquetado). Cada modelo tiene un *model ID* exacto que debes usar tal cual; un ID mal escrito o con sufijo de fecha inventado provoca un error 404.

- **Parámetros obligatorios de una petición**: `model`, `max_tokens` y `messages`. El array `messages` debe empezar por un mensaje de rol `user` y, salvo el rol `system` a nivel superior, alternar entre `user` y `assistant` (mensajes consecutivos del mismo rol se combinan). El `system` prompt va en su propio campo, no dentro de `messages`.

- **`stop_reason`**: indica por qué paró el modelo. Valores clave: `end_turn` (terminó normal), `max_tokens` (alcanzó el límite, hay que subirlo o usar streaming), `tool_use` (quiere llamar a una herramienta), `refusal` (rechazó por seguridad). Tu código debe ramificar según este campo en lugar de asumir que siempre hay texto.

- **Streaming (SSE)**: en vez de esperar la respuesta completa, recibes eventos token a token vía Server-Sent Events. Es la opción recomendada para respuestas largas, `max_tokens` altos o UIs en tiempo real, porque evita timeouts de conexión. Los SDKs ofrecen helpers como `.get_final_message()` / `.finalMessage()` para recomponer la respuesta completa.

- **Tool use (uso de herramientas)**: defines herramientas con un nombre, descripción y un esquema JSON de entrada. Cuando Claude decide usar una, devuelve un bloque `tool_use`; tú ejecutas la función y devuelves el resultado en un bloque `tool_result` con el `tool_use_id` que coincida. Distingue **herramientas definidas por el usuario** (las ejecutas tú, client-side) de las **server-side** (web search, code execution, etc., que corren en infraestructura de Anthropic).

- **Tool runner vs bucle manual**: el *tool runner* del SDK (en beta) automatiza el bucle agéntico (llama a la API, ejecuta tus funciones, reenvía resultados, repite). El *bucle manual* te da control fino para logging, ejecución condicional o aprobación humana antes de cada acción.

- **MCP (Model Context Protocol)**: estándar abierto para conectar Claude a fuentes de datos y herramientas externas (GitHub, bases de datos, servicios). Permite exponer capacidades de terceros de forma estandarizada sin reimplementar integraciones.

- **Agentes y subagentes**: un agente es un bucle donde el modelo decide su propia trayectoria con sus herramientas. Antes de construir uno, valida cuatro criterios: complejidad, valor, viabilidad y coste del error. Si fallas alguno, quédate en un nivel más simple (una llamada o un workflow).

- **Prompt caching**: cachea prefijos estables del prompt para reducir coste (hasta ~90% en la parte cacheada) y latencia. Es un *prefix match*: cualquier byte que cambie en el prefijo invalida todo lo posterior. Por eso el contenido estable va primero y lo volátil (timestamps, IDs) al final. Se verifica con `usage.cache_read_input_tokens`.

- **Salidas estructuradas (structured outputs)**: restringen la respuesta a un esquema JSON, garantizando salida parseable. Se configuran con `output_config.format`, o validando parámetros de herramientas con `strict: true`.

- **Despliegue multi-proveedor**: la API de primera parte y **Claude Platform on AWS** tienen paridad total de funcionalidades. **Amazon Bedrock**, **Google Vertex AI** y **Microsoft Foundry** sirven la misma Messages API pero **no** soportan Managed Agents ni las herramientas server-side de Anthropic; en esos casos usas Claude API + tool use.

## Qué necesitas dominar para el certificado

1. **Anatomía de una petición a la Messages API**: parámetros obligatorios, estructura de `messages`, el campo `system`, y cómo se compone la respuesta (lista de bloques de contenido, no un string plano).
2. **Selección de modelo**: cuándo Opus, cuándo Sonnet, cuándo Haiku, y por qué nunca debes degradar de modelo "por ahorrar" sin que sea decisión explícita.
3. **Manejo de `stop_reason`** y de los distintos tipos de bloques de contenido (`text`, `tool_use`, `thinking`).
4. **Tool use de principio a fin**: definición de herramienta, ciclo `tool_use` → ejecución → `tool_result`, opciones de `tool_choice` (`auto`, `any`, `tool`, `none`).
5. **Streaming**: cuándo usarlo y los tipos de eventos (`message_start`, `content_block_delta`, `message_delta`, etc.).
6. **El árbol de decisión de superficies**: una llamada → workflow → agente → Managed Agents, y saber justificar cada salto.
7. **Optimización de coste**: prompt caching, batches (50% más barato, asíncrono), token counting (usa el endpoint `count_tokens`, **nunca** tiktoken) y elección de modelo.
8. **MCP y agentes** a nivel conceptual: qué problema resuelve cada uno.
9. **Diferencias entre proveedores** y qué funcionalidades están disponibles en cada uno.
10. **Manejo de errores**: códigos HTTP comunes (400, 401, 429, 529), cuáles son reintentables y que los SDKs reintentan 429/5xx automáticamente con backoff.

## Plan de estudio

1. **Monta el entorno (día 1)**: instala el SDK oficial de tu lenguaje (`pip install anthropic` o `npm install @anthropic-ai/sdk`), configura `ANTHROPIC_API_KEY` como variable de entorno (nunca hardcodeada) y haz tu primera llamada con `model`, `max_tokens` y un `messages` simple. Inspecciona la respuesta: fíjate en que `content` es una *lista de bloques*.
2. **Domina la petición básica (días 2-3)**: practica con `system` prompts, conversaciones multi-turno (recuerda que la API es stateless: reenvías todo el historial), y visión (imágenes por base64 y por URL). Lee `response.stop_reason` en cada caso.
3. **Streaming (día 4)**: convierte una llamada normal en streaming y maneja los eventos. Usa `.get_final_message()` para no perder la respuesta completa.
4. **Tool use (días 5-7)**: define una herramienta sencilla (ej. `get_weather`), implementa el bucle manual completo, y luego prueba el tool runner del SDK. Entiende `tool_choice` y el manejo de errores en `tool_result` (`is_error: true`).
5. **Coste y eficiencia (día 8)**: experimenta con prompt caching (verifica los hits con `usage.cache_read_input_tokens`), usa `count_tokens` para estimar coste, y prueba la Batches API.
6. **Conceptos de agentes y MCP (días 9-10)**: estudia el árbol de decisión (cuándo subir de nivel), los cuatro criterios para decidir si construir un agente, y qué es MCP. No necesitas construir un agente complejo para el 101, pero sí entender cuándo lo harías.
7. **Proveedores y errores (día 11)**: memoriza qué funcionalidades hay en Bedrock/Vertex vs primera parte, y la tabla de códigos de error con su carácter reintentable.
8. **Repaso final (día 12)**: pasa estas flashcards y el quiz, reescribe de memoria la anatomía de una petición y el árbol de decisión de superficies.

## Errores comunes y tips

- **Acceder a `response.content[0].text` sin comprobar el tipo**: `content` es una lista de bloques heterogéneos. Recorre los bloques y comprueba `block.type == "text"` antes de leer `.text`. Si hay pensamiento o tool use, el primer bloque puede no ser texto.
- **Inventar model IDs con sufijo de fecha**: usa el alias exacto (`claude-opus-4-...`, `claude-sonnet-4-...`, `claude-haiku-4-...`). Un ID mal construido da 404.
- **Olvidar que la API es stateless**: si no reenvías el historial completo, Claude "no recuerda" la conversación. No hay sesión del lado servidor en la Messages API básica.
- **Primer mensaje con rol `assistant` o roles consecutivos mal alternados**: el primer mensaje debe ser `user`; provoca un 400 si no.
- **`max_tokens` demasiado bajo**: trunca la salida a mitad de frase (`stop_reason: "max_tokens"`). Para no-streaming usa ~16000 por defecto; para streaming, más holgura.
- **No manejar `stop_reason: "refusal"`** ni `tool_use`: tu bucle se rompe o ignora una llamada a herramienta.
- **Romper el caché silenciosamente**: meter `datetime.now()` o un UUID al principio del system prompt invalida todo el prefijo. Si `cache_read_input_tokens` es siempre cero, busca un invalidador silencioso.
- **Usar tiktoken para contar tokens**: es el tokenizador de OpenAI y subestima los tokens de Claude. Usa el endpoint `count_tokens`.
- **Reintentar 429/5xx a mano sin necesidad**: los SDKs ya reintentan con backoff exponencial (`max_retries`, por defecto 2). No reintentes errores 4xx (salvo 429): no son reintentables.
- **Saltar directo a "construir un agente"**: si una sola llamada o un workflow resuelve la tarea, no montes un agente. Más capas = más coste, latencia y superficie de error.
- **Asumir que Bedrock/Vertex tienen todo**: no soportan Managed Agents ni herramientas server-side de Anthropic. Comprueba la paridad antes de prometer una funcionalidad.

## Puntos clave para recordar

- Todo pasa por la **Messages API** (`POST /v1/messages`); tool use y salidas estructuradas son parámetros de esa misma llamada.
- La API es **stateless**: reenvía el historial completo en cada petición.
- **`content` es una lista de bloques**; comprueba `block.type` antes de leer.
- Parámetros obligatorios: **`model`, `max_tokens`, `messages`**; el primer mensaje debe ser `user`.
- Elige modelo por la tarea: **Opus** (complejo), **Sonnet** (equilibrio/producción), **Haiku** (simple/rápido). Usa el **model ID exacto**.
- Ramifica según **`stop_reason`** (`end_turn`, `max_tokens`, `tool_use`, `refusal`).
- **Tool use**: `tool_use` → ejecutas → `tool_result` con el `tool_use_id` correcto. Tool runner automatiza; bucle manual da control.
- **Empieza simple**: una llamada → workflow → agente. Sube de nivel solo si complejidad, valor, viabilidad y coste del error lo justifican.
- **Ahorra coste** con prompt caching (prefijo estable primero), Batches (50%, asíncrono) y `count_tokens` (no tiktoken).
- **MCP** estandariza la conexión a herramientas y datos externos.
- Paridad total en **primera parte** y **Claude Platform on AWS**; **Bedrock/Vertex/Foundry** no tienen Managed Agents ni tools server-side.
- Usa **streaming** para respuestas largas o `max_tokens` altos; deja que el **SDK** reintente 429/5xx.