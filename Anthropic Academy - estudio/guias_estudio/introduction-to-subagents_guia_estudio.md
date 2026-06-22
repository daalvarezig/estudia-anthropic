## Resumen

Los **subagents** (subagentes) son instancias de Claude especializadas que un agente principal puede invocar para delegar partes concretas de una tarea. En lugar de que un único agente haga todo dentro de una sola conversación (un único contexto, un único system prompt, todas las herramientas a la vez), el agente principal "orquestador" reparte el trabajo a subagentes, cada uno con su **propio contexto aislado**, su **propio prompt/instrucciones**, su **propio conjunto de herramientas** y, opcionalmente, su **propio modelo**. Cada subagente trabaja, produce un resultado y devuelve solo un **resumen** al agente principal, no toda su transcripción.

Esta guía está pensada para preparar la certificación oficial de Anthropic Academy **"Introduction to Subagents"**. Va dirigida a personas que ya conocen lo básico de Claude / Claude Code y quieren entender cuándo, por qué y cómo usar subagentes para construir flujos más fiables, paralelizables y eficientes en consumo de contexto. El enfoque es conceptual y práctico: qué problema resuelven los subagentes, cómo se configuran (sobre todo en Claude Code) y qué patrones y errores debes conocer para responder bien en el examen.

## Conceptos clave

- **Agente vs. subagente.** Un *agente* es un bucle en el que Claude razona, usa herramientas, observa resultados y repite hasta cumplir un objetivo. Un *subagente* es otro agente que el principal lanza para una subtarea acotada. El principal es el orquestador; el subagente es el especialista.

- **Aislamiento de contexto (context isolation).** Es la idea central. Cada subagente tiene su propia ventana de contexto independiente. Toda la exploración, los archivos leídos y los pasos intermedios ocurren en el contexto del subagente y **no contaminan** el del agente principal. Al principal solo le vuelve un resumen final. Esto preserva la ventana de contexto del orquestador para la coordinación y el razonamiento de alto nivel.

- **Especialización.** Un subagente se define con un **system prompt propio** que le da un rol concreto (p. ej. "revisor de seguridad", "experto en tests", "analista de datos"). Instrucciones enfocadas producen mejores resultados que un único prompt gigante que intenta cubrirlo todo.

- **Permisos de herramientas restringidos.** A cada subagente le concedes solo las herramientas que necesita. Un subagente de revisión de código puede tener solo lectura y búsqueda, sin permiso de escritura ni de ejecutar comandos. Esto reduce riesgo y enfoca el comportamiento.

- **Modelo configurable por subagente.** Puedes asignar un modelo distinto a cada subagente: por ejemplo Haiku para tareas rápidas y baratas (clasificar, buscar) y Sonnet u Opus para razonamiento profundo. Optimizas coste y latencia según la dificultad de la subtarea.

- **Subagentes en Claude Code.** Se definen como archivos **Markdown con front-matter YAML** ubicados en `.claude/agents/` (alcance de proyecto) o `~/.claude/agents/` (alcance de usuario, todos tus proyectos). El front-matter incluye campos como `name`, `description`, `tools` y, opcionalmente, `model`. El cuerpo Markdown es el system prompt del subagente.

- **Invocación automática vs. explícita.** Claude Code puede **delegar automáticamente** en un subagente cuando la `description` encaja con la tarea (por eso la descripción debe ser clara y orientada a "cuándo usarme"). También puedes invocarlo **explícitamente** ("usa el subagente *code-reviewer* para…").

- **El campo `description` dirige el enrutado.** Es lo que el orquestador lee para decidir si delega. Escríbela en términos de cuándo conviene usar ese subagente; frases como "Use proactively when…" mejoran la delegación automática.

- **Paralelismo (fan-out / fan-in).** Varios subagentes pueden trabajar a la vez sobre subtareas independientes (fan-out) y el principal agrega sus resúmenes (fan-in). Útil para explorar varias zonas de un código o investigar varias fuentes en paralelo.

- **Compromisos (trade-offs).** Los subagentes añaden latencia de arranque y consumen tokens (cada uno repite parte del contexto al inicializarse). No comparten estado entre sí salvo a través del principal. No conviene delegar tareas triviales: el coste de coordinación puede superar el beneficio.

- **Relación con MCP.** El **Model Context Protocol (MCP)** aporta herramientas/datos externos; los subagentes son una forma de *organizar el trabajo* del agente. Un subagente puede usar herramientas MCP si se le conceden, pero son conceptos ortogonales.

## Que necesitas dominar para el certificado

- **Definir el problema que resuelven:** evitar el desbordamiento de contexto del agente principal, especializar comportamiento y permitir paralelismo. Saber explicar **por qué** el aislamiento de contexto es la ventaja principal.
- **Configuración en Claude Code:** ubicación de los archivos (`.claude/agents/` de proyecto frente a `~/.claude/agents/` de usuario), estructura del front-matter YAML (`name`, `description`, `tools`, `model`) y que el cuerpo Markdown es el system prompt.
- **Reglas de precedencia:** los subagentes de proyecto tienen prioridad sobre los de usuario cuando hay nombres en conflicto.
- **Permisos de herramientas:** cómo y por qué restringir herramientas por subagente; el principio de mínimo privilegio.
- **Selección de modelo por subagente:** cuándo usar Haiku, Sonnet u Opus según coste/latencia/dificultad.
- **Invocación:** diferencia entre delegación automática (basada en `description`) e invocación explícita, y cómo escribir una buena `description`.
- **Flujo de datos:** que el subagente devuelve un resumen al principal y que **no** se comparte la transcripción completa ni el contexto entre subagentes.
- **Patrones de orquestación:** orquestador-trabajadores, fan-out/fan-in, pipelines secuenciales.
- **Trade-offs:** latencia, coste de tokens, ausencia de estado compartido; cuándo NO usar subagentes.

## Plan de estudio

1. **Repasa el bucle de agente.** Asegúrate de entender el ciclo razonar→usar herramienta→observar→repetir. Un subagente es ese mismo bucle, lanzado por otro agente.
2. **Interioriza el aislamiento de contexto.** Dibújalo: principal con su contexto, subagente con el suyo, y solo el resumen cruzando la frontera. Si entiendes esto, entiendes el 50% del examen.
3. **Crea un subagente en Claude Code.** Crea `.claude/agents/code-reviewer.md` con front-matter (`name`, `description`, `tools: Read, Grep, Glob`) y un system prompt de "revisor de código". Pídele a Claude Code que revise un cambio y observa cómo delega.
4. **Experimenta con la `description`.** Cambia la descripción a algo vago y luego a algo orientado a "cuándo usarme" y comprueba cómo cambia la delegación automática.
5. **Restringe herramientas.** Quita la escritura a un subagente y verifica que ya no puede modificar archivos. Entiende el mínimo privilegio en la práctica.
6. **Prueba modelos distintos.** Asigna `model: haiku` a un subagente de búsqueda y `model: opus` a uno de razonamiento. Razona el porqué.
7. **Monta un fan-out.** Pide una tarea que se divida en varias subtareas independientes y observa cómo se reparten y se agregan los resultados.
8. **Repasa trade-offs.** Lista escenarios donde NO usarías subagentes (tareas pequeñas, fuerte dependencia entre pasos, necesidad de estado compartido continuo).
9. **Autoevalúate** con las flashcards y el quiz de esta guía hasta acertar sin dudar.

## Errores comunes y tips

- **Creer que los subagentes comparten contexto.** No lo hacen. Cada uno parte de cero salvo lo que el principal le pase en el prompt de invocación, y solo devuelven un resumen. Es un error de examen frecuente.
- **Descripciones pobres.** Una `description` genérica ("ayuda con código") impide la delegación automática. Escríbela indicando *cuándo* usar el subagente y, si quieres uso proactivo, dilo explícitamente.
- **Dar todas las herramientas a todos.** Rompe el principio de mínimo privilegio y aumenta el riesgo. Concede solo lo necesario.
- **Sobreusar subagentes.** Delegar tareas triviales añade latencia y coste de tokens sin beneficio. Usa subagentes cuando hay aislamiento de contexto que ganar, especialización clara o paralelismo real.
- **Confundir alcance de proyecto y de usuario.** `.claude/agents/` es por proyecto (versionable y compartible con el equipo); `~/.claude/agents/` es personal para todos tus proyectos. Ante conflicto de nombres, gana el de proyecto.
- **Confundir subagentes con MCP.** MCP conecta herramientas/datos externos; los subagentes organizan el trabajo. Son complementarios, no lo mismo.
- **Olvidar el coste de arranque.** Cada subagente reinicializa contexto; no es gratis. Tenlo en cuenta al diseñar pipelines largos.
- **Tip de modelo:** empareja la dificultad de la subtarea con el modelo. Tareas de filtrado/clasificación → Haiku; síntesis/razonamiento complejo → Sonnet/Opus.

## Puntos clave para recordar

- Un subagente es un agente especializado que el principal invoca para una subtarea; tiene **contexto propio, prompt propio, herramientas propias y modelo opcional propio**.
- La ventaja central es el **aislamiento de contexto**: el trabajo sucio no contamina al orquestador, que solo recibe un **resumen**.
- En Claude Code se definen como **Markdown + front-matter YAML** en `.claude/agents/` (proyecto) o `~/.claude/agents/` (usuario); el **proyecto tiene prioridad**.
- Front-matter típico: `name`, `description`, `tools`, `model`. El **cuerpo Markdown es el system prompt**.
- La **`description`** decide la delegación automática; escríbela orientada a "cuándo usarme". También cabe invocación explícita.
- Aplica **mínimo privilegio** en herramientas y **empareja el modelo** con la dificultad para optimizar coste y latencia.
- Patrones: **orquestador-trabajadores** y **fan-out/fan-in** para paralelizar subtareas independientes.
- Trade-offs: **latencia de arranque, coste de tokens, sin estado compartido** entre subagentes. No los uses para tareas triviales o muy acopladas.
- **MCP ≠ subagentes:** MCP da herramientas/datos externos; los subagentes organizan el trabajo (y pueden usar MCP si se les concede).