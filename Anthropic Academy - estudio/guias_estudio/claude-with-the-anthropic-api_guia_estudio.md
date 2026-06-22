## Resumen

Esta guía prepara la certificación oficial de **Anthropic Academy: "Building with the Claude API"**. El examen verifica que sabes construir aplicaciones reales sobre la API de Claude: desde una simple llamada de clasificación hasta agentes que usan herramientas, mantienen conversaciones largas y controlan costes.

Está pensada para desarrolladores que ya programan (Python o TypeScript sobre todo) y quieren dominar la **Messages API** de Anthropic, los SDK oficiales, el uso de herramientas (tool use), el razonamiento extendido (thinking), el caché de prompts, las salidas estructuradas y las buenas prácticas de despliegue (streaming, manejo de errores, batches, conteo de tokens). No necesitas experiencia previa con LLMs, pero sí soltura leyendo JSON y haciendo peticiones HTTP.

La idea clave que recorre todo el temario: **todo pasa por un único endpoint, `POST /v1/messages`**. Las herramientas, las salidas estructuradas, la visión, el thinking y el caché no son APIs separadas; son parámetros y bloques de contenido de esa misma petición. Si interiorizas eso, el resto encaja.

## Conceptos clave

- **Messages API (`/v1/messages`)**: el corazón de todo. Envías una lista de `messages` (cada uno con `role` "user" o "assistant" y `content`) más `model` y `max_tokens`. Recibes un objeto con `content` (una lista de *bloques*), `stop_reason` y `usage`. **La API es sin estado (stateless)**: tú envías el historial completo en cada llamada; el servidor no recuerda conversaciones anteriores.

- **Modelos y familia Claude**: hay varios niveles. **Opus** es el más capaz (razonamiento y trabajo agéntico largo), **Sonnet** equilibra velocidad e inteligencia, **Haiku** es el más rápido y económico para tareas simples. Cada modelo tiene un ID exacto (p. ej. `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5`) que **no debes inventar ni adornar con sufijos de fecha**, o recibirás un 404. Cada uno tiene su ventana de contexto y su precio por millón de tokens (input y output se cobran por separado, el output más caro).

- **Bloques de contenido (content blocks)**: `content` es siempre una *lista* de bloques, no una cadena. Los tipos más comunes son `text`, `thinking`, `tool_use`, `tool_result`, `image` y `document`. Antes de leer `.text` debes comprobar `block.type`, porque el primer bloque puede ser de razonamiento o de uso de herramienta.

- **`stop_reason`**: indica por qué paró el modelo. Valores que debes conocer: `end_turn` (terminó solo), `max_tokens` (alcanzó el límite, output truncado), `tool_use` (quiere llamar a una herramienta, ejecútala y continúa), `stop_sequence`, `pause_turn` (flujos agénticos con herramientas de servidor) y `refusal` (rechazo por seguridad). Comprueba `stop_reason` antes de procesar la respuesta.

- **Tool use (uso de herramientas)**: defines herramientas con `name`, `description` y un `input_schema` en JSON Schema. Cuando Claude decide usar una, devuelve un bloque `tool_use` y `stop_reason: "tool_use"`. Tú ejecutas la función, devuelves un bloque `tool_result` (con el mismo `tool_use_id`) en un mensaje `user`, y repites el bucle hasta `end_turn`. Hay dos modos: el **tool runner** del SDK (automático, recomendado) y el **bucle manual** (control fino: aprobación humana, logging, ejecución condicional). `tool_choice` controla si el uso es `auto`, `any`, una herramienta concreta o `none`.

- **Herramientas del lado del cliente vs. del servidor**: las *cliente* (bash, editor de texto, memoria) las define Anthropic pero las ejecuta tu código. Las *servidor* (code execution, web search, web fetch) corren en la infraestructura de Anthropic; solo las declaras y Claude las usa sola.

- **Thinking / razonamiento extendido**: en los modelos actuales se usa **thinking adaptativo** (`thinking: {type: "adaptive"}`): Claude decide cuánto razonar. El antiguo `budget_tokens` (presupuesto fijo) está obsoleto en los modelos nuevos. La profundidad se controla con el parámetro **effort** (`output_config: {effort: "low" | "medium" | "high" | "max"}`).

- **Salidas estructuradas (structured outputs)**: para garantizar JSON válido conforme a un esquema usas `output_config: {format: {type: "json_schema", schema: {...}}}`, o el helper `messages.parse()` que valida automáticamente contra un modelo Pydantic/Zod. También existe `strict: true` en herramientas para validar sus parámetros. El antiguo parámetro `output_format` está obsoleto.

- **Streaming**: para respuestas largas o `max_tokens` alto debes usar streaming (`messages.stream()`), porque las peticiones no-streaming largas pueden agotar el timeout HTTP. El helper `get_final_message()` / `finalMessage()` te da la respuesta completa aunque hayas ido recibiendo eventos.

- **Caché de prompts (prompt caching)**: reutiliza prefijos grandes y estables para abaratar hasta ~90%. Es un **emparejamiento por prefijo**: cualquier byte que cambie antes de un punto de caché (`cache_control: {type: "ephemeral"}`) invalida todo lo posterior. Se verifica con `usage.cache_read_input_tokens`.

- **Endpoints de apoyo**: **Batches** (procesamiento asíncrono al 50% del precio, hasta 24h), **Files** (subir archivos una vez y referenciarlos por `file_id`), **Token Counting** (`count_tokens`, usa el tokenizador real de Claude, nunca `tiktoken`) y **Models** (descubrir capacidades y ventanas de contexto en vivo).

- **Visión y documentos**: puedes enviar imágenes (base64 o URL) y PDFs como bloques de contenido en el mensaje del usuario.

- **Manejo de errores y reintentos**: usa las clases de excepción tipadas del SDK (`RateLimitError`, `BadRequestError`, etc.), no compares cadenas de texto. El SDK reintenta automáticamente 429 y 5xx con backoff exponencial.

## Que necesitas dominar para el certificado

- Construir una petición básica a `messages.create()` con `model`, `max_tokens` y `messages`, y recorrer correctamente `content` comprobando `block.type`.
- Entender que la API es **sin estado** y reenviar el historial completo en conversaciones multi-turno; saber que el primer mensaje debe ser `user`.
- Implementar el **bucle de tool use** completo: definir la herramienta, detectar `stop_reason: "tool_use"`, ejecutar, devolver `tool_result` con el `tool_use_id` correcto, y repetir. Saber cuándo usar el tool runner frente al bucle manual.
- Distinguir herramientas de **cliente** (las ejecutas tú) de las de **servidor** (las ejecuta Anthropic).
- Configurar **thinking adaptativo** y el parámetro **effort**; saber que `budget_tokens` está obsoleto en los modelos actuales.
- Forzar **salidas estructuradas** con `output_config.format` o `messages.parse()`, y conocer las limitaciones del JSON Schema soportado.
- Usar **streaming** y saber por qué es obligatorio con `max_tokens` alto.
- Diseñar **caché de prompts** correctamente: contenido estable primero, volátil al final; reconocer "invalidadores silenciosos" (un `datetime.now()` o un UUID en el system prompt arruinan el caché).
- Interpretar el objeto **`usage`**: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.
- Manejar todos los **`stop_reason`**, especialmente `refusal`, `max_tokens` y `tool_use`.
- Elegir el **modelo adecuado** por coste/capacidad y usar el ID exacto.
- Conocer los **endpoints de apoyo**: Batches (50% más barato, asíncrono), Files (`file_id`), y Token Counting (`count_tokens`, no `tiktoken`).
- Aplicar **manejo de errores** con excepciones tipadas y entender el reintento automático del SDK.

## Plan de estudio

1. **Monta el entorno (1 día).** Instala el SDK oficial (`pip install anthropic` o `npm install @anthropic-ai/sdk`), pon tu clave en `ANTHROPIC_API_KEY` (variable de entorno, **nunca** hardcodeada) y haz tu primera llamada a `messages.create()`. Imprime y examina el objeto de respuesta entero: `content`, `stop_reason`, `usage`.
2. **Domina la petición básica (1-2 días).** Practica system prompts, conversaciones multi-turno (reenviando el historial), visión con una imagen y conteo de tokens con `count_tokens()`. Interioriza que `content` es una lista de bloques.
3. **Tool use a fondo (2-3 días).** Implementa primero el **bucle manual** para entender cada paso (es lo que más cae en el examen), y luego prueba el **tool runner**. Asegúrate de devolver siempre el `tool_use_id` correcto. Prueba `tool_choice` y el manejo de errores en `tool_result` (`is_error: true`).
4. **Thinking, effort y salidas estructuradas (1-2 días).** Activa thinking adaptativo, juega con `effort`, y fuerza JSON con `output_config.format` y con `messages.parse()`.
5. **Producción: streaming, caché, errores (2 días).** Implementa streaming con `get_final_message()`, diseña un prompt cacheado y verifica el hit con `cache_read_input_tokens`, y captura excepciones tipadas.
6. **Endpoints de apoyo (1 día).** Crea un batch y recupera resultados; sube un archivo con Files y referéncialo por `file_id`.
7. **Repaso activo.** Estudia las flashcards, haz el quiz, y vuelve a cualquier concepto que falles. Relee la tabla de `stop_reason` y la de elección de modelo hasta tenerlas memorizadas.

## Errores comunes y tips

- **Acceder a `response.content[0].text` directamente.** Falla si el primer bloque es `thinking`, `tool_use` o un rechazo. **Comprueba siempre `block.type`** y recorre la lista.
- **Inventar el ID del modelo o añadirle sufijos de fecha.** Usa el ID exacto (alias) de la documentación; lo contrario da 404.
- **Olvidar reenviar el historial.** La API es sin estado: si no incluyes los mensajes previos, Claude "olvida" la conversación.
- **Romper el bucle de herramientas.** Cada `tool_result` debe llevar el `tool_use_id` exacto del `tool_use` correspondiente, e ir en un mensaje con `role: "user"`. Si falta un resultado para algún `tool_use`, la petición da error.
- **No comprobar `stop_reason`.** Si es `max_tokens`, tu salida está cortada (sube `max_tokens` o usa streaming). Si es `refusal`, no reintentes con el mismo prompt.
- **Usar `tiktoken` para contar tokens.** Es de OpenAI y subestima los tokens de Claude. Usa `count_tokens()`, que es específico del modelo.
- **Caché que nunca acierta.** Un `datetime.now()`, un UUID o un `json.dumps()` sin `sort_keys=True` al principio del prompt invalidan todo el prefijo. Pon lo estable primero y lo volátil al final; verifica con `usage.cache_read_input_tokens`.
- **No usar streaming con `max_tokens` alto.** Las peticiones largas no-streaming agotan el timeout HTTP del SDK. Usa `messages.stream()` y `get_final_message()`.
- **Hacer string-matching sobre el JSON de `input` de las herramientas.** Parsea siempre con `json.loads()` / `JSON.parse()`; el escapado puede variar.
- **Reinventar lo que el SDK ya ofrece.** Usa los tipos del SDK, las excepciones tipadas y `messages.parse()` / `finalMessage()` en lugar de construirlo a mano.
- **Tip de coste:** Batches da 50% de descuento para trabajo no urgente; el caché de prompts abarata el contexto repetido; elige Haiku/Sonnet para volumen y Opus para tareas difíciles.
- **Tip de diseño:** empieza por lo más simple (una llamada). Solo escala a workflow (varias llamadas orquestadas por tu código) o a agente (Claude decide su trayectoria) cuando la tarea lo justifique de verdad.

## Puntos clave para recordar

- Todo pasa por **`POST /v1/messages`**; herramientas, thinking, structured outputs y caché son parámetros/bloques de esa misma llamada.
- La API es **sin estado**: reenvía el historial completo; el primer mensaje es `user`.
- `content` es una **lista de bloques**; comprueba `block.type` antes de leer `.text`.
- El bucle de **tool use**: `tool_use` → ejecutas → `tool_result` con el `tool_use_id` correcto → repites hasta `end_turn`.
- **Thinking adaptativo** + parámetro **effort** sustituyen al obsoleto `budget_tokens`.
- **Salidas estructuradas** con `output_config.format` o `messages.parse()`; el viejo `output_format` está obsoleto.
- **Streaming obligatorio** con `max_tokens` alto; usa `get_final_message()`/`finalMessage()`.
- **Caché de prompts** = emparejamiento por prefijo; estable primero, volátil al final; verifica con `cache_read_input_tokens`.
- Maneja todos los **`stop_reason`** (sobre todo `tool_use`, `max_tokens`, `refusal`).
- Usa **IDs de modelo exactos**; nunca los inventes.
- Para contar tokens, **`count_tokens`**, nunca `tiktoken`.
- **Batches** = 50% más barato y asíncrono; **Files** = subir una vez, referenciar por `file_id`.
- Usa **excepciones tipadas** del SDK; los 429/5xx se reintentan solos con backoff.