## Resumen

Esta guía prepara para la certificación oficial de Anthropic Academy **"AI Capabilities and Limitations"**. Es un examen de nivel introductorio-intermedio que evalúa si entiendes **qué pueden hacer realmente los modelos de lenguaje grandes (LLM) como Claude, qué NO pueden hacer, y cómo trabajar con ellos de forma responsable y eficaz**. No es un examen de programación: se centra en conceptos, criterio y buenas prácticas.

Está pensada para profesionales que adoptan IA generativa en su trabajo —analistas, gestores de producto, redactores, consultores, desarrolladores que empiezan— y para cualquiera que quiera usar Claude con fundamento. El objetivo del certificado es demostrar **alfabetización en IA (AI Fluency)**: saber dónde aporta valor un LLM, anticipar sus fallos típicos (alucinaciones, sesgos, fecha de corte de conocimiento) y aplicar prácticas seguras y eficaces. Esta guía es material **independiente y original** de repaso, no contenido oficial.

## Conceptos clave

- **Qué es un LLM**: un modelo entrenado para predecir el siguiente token (fragmento de texto) a partir del contexto previo. No "razona" como una base de datos ni "consulta hechos": genera la continuación más probable según los patrones aprendidos. De ahí derivan casi todas sus capacidades y limitaciones.
- **Capacidades centrales**: redacción y reescritura, resumen, traducción, clasificación, extracción de datos estructurados, respuesta a preguntas, generación y explicación de código, razonamiento paso a paso, análisis de documentos largos y conversación. Claude además procesa **imágenes y PDFs** (entrada multimodal) y, según el modelo, hace **razonamiento extendido** ("thinking").
- **Alucinaciones**: el modelo puede generar información plausible pero falsa (citas, cifras, URLs, casos inexistentes) con tono seguro. Es la limitación más importante a entender: no hay garantía de veracidad. Se mitiga con verificación humana, RAG (aportar fuentes en el contexto), pedir citas verificables y permitir que diga "no lo sé".
- **Fecha de corte de conocimiento (knowledge cutoff)**: el modelo solo "sabe" hasta la fecha en que terminó su entrenamiento. No conoce eventos posteriores ni datos en tiempo real (precios, noticias, tu base de datos interna) salvo que se los des en el contexto o mediante herramientas/búsqueda web.
- **Ventana de contexto (context window)**: límite de tokens que el modelo procesa de una vez (entrada + salida). Los Claude actuales manejan ventanas muy grandes (cientos de miles de tokens, hasta 1M en algunos casos), pero no es infinita: textos enormes deben fragmentarse o resumirse.
- **Token**: unidad mínima de texto que procesa el modelo (aprox. 3-4 caracteres en inglés; algo distinto en otros idiomas). El coste y los límites se miden en tokens de entrada y de salida.
- **Determinismo y temperatura**: los LLM son **probabilísticos**; la misma pregunta puede dar respuestas distintas. La "temperatura" controla la aleatoriedad (baja = más consistente y conservador; alta = más creativo y variable).
- **Prompt engineering**: la calidad de la salida depende mucho de la instrucción. Buenas prácticas: ser específico, dar contexto y ejemplos (**few-shot**), asignar un rol, indicar el formato de salida, dividir tareas complejas, y pedir razonamiento paso a paso (**chain of thought**) cuando ayuda.
- **System prompt**: instrucción de alto nivel que fija el rol, las reglas y el tono del asistente, separada del mensaje del usuario.
- **RAG (Retrieval-Augmented Generation)**: técnica para reducir alucinaciones y superar el corte de conocimiento aportando documentos relevantes en el contexto para que el modelo responda **basándose en ellos**.
- **Tool use / function calling**: el modelo puede invocar herramientas externas (búsqueda, cálculo, APIs, bases de datos) para obtener datos reales o ejecutar acciones, compensando sus límites.
- **MCP (Model Context Protocol)**: estándar abierto de Anthropic para conectar modelos a herramientas y fuentes de datos externas de forma uniforme.
- **Agentes y subagentes**: sistemas donde el modelo planifica y ejecuta varios pasos usando herramientas con cierta autonomía; los subagentes delegan subtareas. Más potentes pero con más riesgo de errores acumulados, por lo que requieren supervisión.
- **Sesgos y equidad**: el modelo refleja sesgos presentes en sus datos de entrenamiento; puede reproducir estereotipos o tratar grupos de forma desigual. Hay que revisar resultados en aplicaciones sensibles.
- **Privacidad y seguridad**: no introducir datos sensibles sin control; cuidado con inyección de prompts (prompt injection) y con que el modelo no debe ser la única salvaguarda en decisiones críticas.
- **Familia de modelos Claude**: gama con compromisos distintos entre capacidad, velocidad y coste —típicamente **Opus** (máxima capacidad), **Sonnet** (equilibrio) y **Haiku** (rápido y económico)—. Elegir el modelo adecuado a la tarea es una decisión clave.
- **Plataformas de despliegue**: Claude está disponible vía la **API de Anthropic**, **Amazon Bedrock** y **Google Cloud Vertex AI**, además de la app Claude y Claude Code.
- **Marco de AI Fluency**: usar la IA con criterio implica las "4D": **Delegation** (qué delegar al modelo y qué no), **Description** (saber describir/instruir bien), **Discernment** (evaluar críticamente las salidas) y **Diligence** (uso responsable, transparente y ético).
- **Humano en el bucle (human-in-the-loop)**: en tareas con impacto, el resultado del modelo debe revisarse; la IA asiste, no sustituye la responsabilidad humana.

## Que necesitas dominar para el certificado

- Explicar **cómo funciona un LLM a alto nivel** (predicción de tokens) y por qué eso causa tanto sus fortalezas como sus fallos.
- Distinguir con ejemplos **qué es buen caso de uso** (redactar, resumir, clasificar, extraer, programar con supervisión) frente a **mal caso de uso** (hechos en tiempo real sin herramientas, cálculos críticos sin verificación, decisiones legales/médicas/financieras autónomas).
- Definir y reconocer **alucinación, fecha de corte, ventana de contexto, token, naturaleza probabilística** y sus implicaciones prácticas.
- Saber **mitigar limitaciones**: verificación humana, RAG, tool use, pedir fuentes, dividir tareas, dar contexto.
- Conocer los **principios de prompt engineering** y reconocer un prompt bien construido.
- Entender **sesgo, equidad, privacidad y seguridad**, y por qué hace falta supervisión humana.
- Ubicar el **ecosistema Anthropic**: familia Claude (Opus/Sonnet/Haiku) y sus compromisos, API/SDK, Bedrock, Vertex, MCP, agentes/subagentes.
- Aplicar el **marco de uso responsable / AI Fluency (4D)** a situaciones reales.

## Plan de estudio

1. **Día 1 - Fundamentos**: estudia qué es un LLM y la predicción de tokens. Asegúrate de poder explicar con tus palabras por qué un modelo puede inventarse datos.
2. **Día 2 - Capacidades**: enumera tareas que Claude hace bien y prueba 5-6 tú mismo en la app Claude (resumen, traducción, extracción, clasificación, código). Observa la variabilidad entre intentos.
3. **Día 3 - Limitaciones**: provoca a propósito una alucinación (pide una cita o estadística específica y verifícala). Pregunta por un evento reciente para ver el efecto del corte de conocimiento. Anota cada limitación con su mitigación.
4. **Día 4 - Trabajar mejor con el modelo**: practica prompting (rol, contexto, ejemplos few-shot, formato de salida, chain of thought). Reescribe un prompt malo hasta que mejore claramente.
5. **Día 5 - Ecosistema y extensión**: aprende la familia Claude y cuándo usar cada modelo; entiende RAG, tool use, MCP, agentes y dónde se despliega (API, Bedrock, Vertex).
6. **Día 6 - Uso responsable**: repasa sesgo, privacidad, seguridad, humano en el bucle y el marco de las 4D. Piensa en un caso de tu trabajo y decide qué delegarías y qué no.
7. **Día 7 - Repaso activo**: usa las flashcards y el cuestionario de esta guía; reexplica cada concepto en voz alta. Identifica tus puntos flojos y vuelve a ellos.

## Errores comunes y tips

- **Confundir fluidez con veracidad**: que suene seguro y bien escrito no significa que sea correcto. Verifica siempre los hechos importantes.
- **Creer que el modelo "busca" o "consulta" datos**: por defecto no accede a internet ni a tus sistemas; solo usa lo aprendido más lo que pongas en el contexto. Para datos reales necesita herramientas/RAG.
- **Pensar que la ventana de contexto es memoria persistente**: el modelo no recuerda conversaciones pasadas salvo que se reenvíen; y la ventana, aunque grande, tiene límite.
- **Asumir respuestas idénticas**: al ser probabilístico, varía. No esperes determinismo perfecto sin bajar la temperatura, y aun así pueden cambiar.
- **Echar la culpa al modelo de un prompt vago**: muchos "errores" se resuelven con instrucciones más claras, contexto y ejemplos.
- **Usar el modelo más grande para todo**: encarece y ralentiza sin necesidad. Para tareas simples y de alto volumen, un modelo más rápido (tipo Haiku) suele bastar; reserva el más capaz para razonamiento difícil.
- **Olvidar el factor humano en decisiones sensibles**: en lo legal, médico, financiero o de RR.HH., el modelo asiste pero no decide solo.
- **Tip de examen**: ante una pregunta, identifica si describe una **capacidad** o una **limitación**, y si pide una **mitigación**. Las respuestas correctas suelen ser las prudentes (verificar, supervisar, aportar contexto) frente a las absolutas ("siempre", "nunca", "garantiza").

## Puntos clave para recordar

- Un LLM **predice el siguiente token**; no es una base de datos de hechos.
- **Alucinación** = información plausible pero falsa; mitiga con verificación humana, RAG, tool use y citas verificables.
- **Fecha de corte**: no conoce nada posterior a su entrenamiento ni datos en tiempo real sin herramientas.
- **Ventana de contexto** grande pero finita; el modelo no tiene memoria persistente entre sesiones.
- Salidas **probabilísticas**: varían; la temperatura regula la aleatoriedad.
- Buen **prompting** (rol, contexto, ejemplos, formato, paso a paso) mejora mucho los resultados.
- **RAG, tool use, MCP, agentes/subagentes** extienden las capacidades más allá de los límites del modelo.
- Familia **Claude (Opus/Sonnet/Haiku)**: equilibra capacidad, velocidad y coste; elige según la tarea.
- Disponible en **API de Anthropic, Amazon Bedrock y Google Vertex AI**.
- **Sesgo, privacidad y seguridad** importan; mantén un **humano en el bucle** y aplica el marco de las **4D** (Delegation, Description, Discernment, Diligence).