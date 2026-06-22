## Resumen

**Claude 101** es la certificación introductoria de Anthropic Academy. Está pensada para personas que empiezan con Claude y quieren una base sólida: qué es Claude, qué familia de modelos existe, cómo se conversa con él de forma efectiva, qué capacidades tiene (texto, visión, razonamiento, herramientas) y qué buenas prácticas y límites de seguridad conviene conocer. No es un examen de programación profunda: el objetivo es que cualquier perfil (negocio, producto, soporte, técnico junior) entienda los conceptos fundamentales y sepa usar Claude con criterio.

Esta guía es material de repaso **independiente** y original, escrito para que apruebes con comprensión real, no de memoria. Cubre los conceptos que el certificado evalúa y los errores típicos que hacen fallar.

## Conceptos clave

- **Qué es Claude.** Una familia de modelos de lenguaje grande (LLM) desarrollada por Anthropic. Genera y comprende texto (y, según el modelo, imágenes) prediciendo la continuación más coherente a partir de tu instrucción. Es un asistente conversacional de propósito general, no una base de datos ni un buscador.

- **La familia de modelos: Opus, Sonnet y Haiku.** Tres niveles que equilibran inteligencia, velocidad y coste. **Opus** es el más capaz (tareas complejas, razonamiento largo, agentes). **Sonnet** es el equilibrio entre capacidad y velocidad para producción de alto volumen. **Haiku** es el más rápido y económico para tareas simples y sensibles a la latencia. La regla práctica: usa el modelo más capaz que necesites y baja a Sonnet/Haiku cuando velocidad o coste importen más que la máxima inteligencia.

- **Ventana de contexto (context window).** Es la cantidad máxima de texto (medido en *tokens*) que el modelo puede "tener delante" en una misma conversación: tu instrucción, los documentos que pegas y la respuesta. Si te pasas, hay que resumir, trocear o gestionar el contexto. Los modelos modernos tienen ventanas muy grandes (cientos de miles a un millón de tokens).

- **Tokens.** Unidad en la que el modelo "lee" el texto: trozos de palabras (aprox. ¾ de palabra en inglés; algo más en español y en código). El coste y los límites se miden en tokens de entrada y de salida, no en palabras o caracteres.

- **Prompt (instrucción) y system prompt.** El *prompt* es lo que pides. El *system prompt* es la instrucción de fondo que define el rol, el tono y las reglas de Claude durante toda la conversación ("Eres un asistente experto en X que responde en español, conciso"). Separar el rol (system) de la petición concreta (mensaje del usuario) mejora mucho los resultados.

- **Prompting efectivo.** Claude responde mejor cuando eres claro y específico: da contexto, indica el formato de salida deseado, usa ejemplos (*few-shot*) cuando la tarea es ambigua, y descompón tareas complejas en pasos. Pedir que "piense paso a paso" o estructurar la entrada con etiquetas/secciones ayuda en tareas de razonamiento.

- **Conversación multi-turno y statelessness.** Claude no "recuerda" entre llamadas por sí mismo: la API es *sin estado* (stateless). En cada turno se reenvía el historial de la conversación. La sensación de memoria viene de que tú (o la aplicación) le pasas los mensajes anteriores cada vez.

- **Capacidades multimodales: visión.** Muchos modelos Claude aceptan imágenes además de texto: pueden describir, analizar diagramas, leer capturas o extraer datos de documentos visuales.

- **Razonamiento extendido (thinking).** Los modelos actuales pueden "pensar" antes de responder, dedicando esfuerzo interno a problemas difíciles. En la práctica esto se controla con un modo adaptativo y un parámetro de *esfuerzo* (effort), en lugar de un presupuesto fijo de tokens. Más razonamiento = mejores respuestas en tareas duras, a cambio de más latencia y coste.

- **Uso de herramientas (tool use / function calling).** Claude puede pedir que se ejecuten funciones externas (consultar una API, buscar en una base de datos, hacer cálculos). Tú defines las herramientas con su esquema; Claude decide cuándo usarlas y con qué argumentos; tu sistema ejecuta y le devuelve el resultado. Es la base para construir **agentes**.

- **Agentes y subagentes.** Un agente es Claude operando en un bucle: razona, llama herramientas, observa resultados y repite hasta completar una tarea de varios pasos. Empieza siempre por lo más simple (una sola llamada o un flujo controlado) y solo construye un agente cuando la tarea es realmente abierta y de múltiples pasos.

- **MCP (Model Context Protocol).** Estándar abierto, impulsado por Anthropic, para conectar modelos a herramientas, datos y servicios externos de forma uniforme. Un "servidor MCP" expone capacidades (archivos, GitHub, calendario...) que Claude puede usar sin integración a medida para cada uno.

- **Productos y formas de acceso.** Claude se usa de varias maneras: la **app de Claude** (web/escritorio/móvil) para usuarios; **Claude Code** para desarrollo en terminal; y la **API / SDK** de Anthropic para integrarlo en tus propias aplicaciones. Además está disponible a través de nubes asociadas como **Amazon Bedrock** y **Google Vertex AI**.

- **Caché de prompts (prompt caching).** Si reutilizas un mismo bloque grande de contexto (un documento, instrucciones extensas) en muchas peticiones, puedes cachearlo para reducir mucho el coste y la latencia de la parte repetida.

- **AI Fluency.** Marco educativo de Anthropic sobre cómo colaborar bien con la IA. Resume las competencias en cuatro "D": **Delegation** (qué tareas confiar a la IA y cuáles no), **Description** (cómo comunicar la tarea con claridad), **Discernment** (evaluar críticamente la salida) y **Diligence** (usar la IA de forma responsable y transparente).

- **Seguridad y uso responsable.** Claude está entrenado para ser útil, honesto e inofensivo (filosofía de Anthropic, ligada a la *Constitutional AI*). Puede equivocarse o "alucinar" (inventar datos con seguridad), por lo que conviene verificar hechos importantes. Nunca pongas secretos o datos sensibles donde no deban estar, y mantén siempre supervisión humana en decisiones de impacto.

## Que necesitas dominar para el certificado

1. **Identificar qué es Claude y qué no es**: un asistente LLM conversacional de Anthropic, no un buscador ni una fuente de verdad infalible.
2. **Diferenciar Opus, Sonnet y Haiku** y saber elegir según el equilibrio inteligencia / velocidad / coste.
3. **Entender tokens y ventana de contexto**: qué son, por qué importan para coste y límites, y qué hacer cuando el contexto se queda corto.
4. **Escribir buenos prompts**: claridad, contexto, formato de salida, ejemplos, descomposición de tareas y el papel del system prompt.
5. **Saber que la API es sin estado** y que la "memoria" de la conversación es el historial reenviado.
6. **Reconocer las capacidades**: texto, visión, razonamiento extendido y uso de herramientas.
7. **Conceptos de agentes y MCP** a nivel introductorio: qué resuelven y cuándo tienen sentido.
8. **Vías de acceso**: app de Claude, Claude Code, API/SDK, y nubes (Bedrock, Vertex).
9. **Límites y seguridad**: alucinaciones, verificación, supervisión humana, privacidad de datos y los principios "útil, honesto, inofensivo".
10. **Marco AI Fluency** (las cuatro D) como forma de colaborar bien con la IA.

## Plan de estudio

1. **Día 1 — Fundamentos.** Lee qué es un LLM, qué es Claude y la familia Opus/Sonnet/Haiku. Memoriza la regla de elección de modelo. Asegúrate de poder explicar tokens y ventana de contexto con tus propias palabras.
2. **Día 2 — Prompting.** Practica escribiendo 10 prompts: uno con contexto y formato pedido, uno con few-shot, uno con descomposición en pasos, uno con system prompt definiendo rol. Compara respuestas vagas vs específicas.
3. **Día 3 — Capacidades.** Estudia visión, razonamiento extendido (modo adaptativo + esfuerzo) y uso de herramientas. Dibuja el ciclo de tool use: Claude pide herramienta → tú ejecutas → devuelves resultado → Claude continúa.
4. **Día 4 — Agentes, MCP y acceso.** Entiende qué es un agente, cuándo conviene (y cuándo NO), qué es MCP y para qué sirve. Repasa las vías de acceso (app, Claude Code, API, Bedrock/Vertex).
5. **Día 5 — Seguridad y AI Fluency.** Repasa alucinaciones, verificación, privacidad, supervisión humana y los principios de Anthropic. Aprende las cuatro D de AI Fluency.
6. **Día 6 — Repaso activo.** Haz las flashcards y el cuestionario de esta guía. Reescribe de memoria las definiciones que falles.
7. **Día 7 — Simulacro.** Responde el quiz a contrarreloj, revisa explicaciones de los errores y refuerza solo esas áreas.

## Errores comunes y tips

- **Confundir tokens con palabras.** Un token no es una palabra; el coste y los límites se miden en tokens (entrada + salida).
- **Pensar que Claude "recuerda" solo.** La API es sin estado; sin reenviar el historial no hay memoria. Las preguntas de examen suelen probar esto.
- **Elegir siempre el modelo más grande.** No siempre es lo correcto: para clasificar o tareas simples, Haiku/Sonnet son más rápidos y baratos. El examen valora el criterio de elección, no "Opus para todo".
- **Creer que Claude nunca se equivoca.** Puede alucinar: inventa datos con tono seguro. Verifica hechos críticos y mantén supervisión humana.
- **Pedir prompts vagos.** "Hazlo mejor" rinde poco. Especifica objetivo, contexto, formato y, si hace falta, ejemplos.
- **Saltar a construir un agente.** Antes de un agente, prueba con una sola llamada o un flujo controlado; solo escala si la tarea es abierta y multi-paso.
- **Mezclar herramientas externas con la "memoria del modelo".** El uso de herramientas (tool use) es lo que da a Claude acceso a datos en tiempo real; el modelo por sí solo solo sabe lo de su entrenamiento.
- **Olvidar la privacidad.** No metas credenciales ni datos sensibles donde no toque. Tip de seguridad: trata enlaces y contenidos de fuentes desconocidas con cautela.
- **Tip de prompting:** define el rol en el system prompt y deja la tarea concreta en el mensaje de usuario. Indica el formato de salida explícitamente (lista, JSON, tabla).

## Puntos clave para recordar

- Claude = familia de LLMs de Anthropic; asistente conversacional útil, honesto e inofensivo.
- Tres niveles: **Opus** (máxima capacidad), **Sonnet** (equilibrio), **Haiku** (rápido y barato).
- Se mide en **tokens**; la **ventana de contexto** limita cuánto texto cabe a la vez.
- La **API es sin estado**: la memoria conversacional es el historial reenviado.
- Buen prompting = claridad + contexto + formato + ejemplos; usa el **system prompt** para el rol.
- Capacidades: **texto, visión, razonamiento extendido y uso de herramientas**.
- **Agentes**: Claude en bucle con herramientas; empieza simple, escala solo si hace falta.
- **MCP**: estándar abierto para conectar Claude a herramientas y datos externos.
- Acceso: **app de Claude, Claude Code, API/SDK**, y nubes **Bedrock / Vertex**.
- Cuida la **seguridad**: verifica alucinaciones, protege datos, mantén supervisión humana.
- **AI Fluency** = Delegation, Description, Discernment, Diligence.