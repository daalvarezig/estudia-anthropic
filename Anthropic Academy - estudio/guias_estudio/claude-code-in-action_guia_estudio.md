## Resumen

**Claude Code in Action** es la certificación oficial de Anthropic Academy centrada en el uso profesional de **Claude Code**, el agente de programación de Anthropic que vive en la terminal (y también como extensión de IDE y SDK). No es un examen sobre teoría de modelos de lenguaje, sino sobre saber **operar un agente de codificación de forma efectiva, segura y reproducible**: cómo darle contexto, cómo controlar lo que puede hacer en tu máquina, cómo extenderlo con tus propias herramientas y cómo integrarlo en flujos reales (Git, CI, equipos).

Está pensada para **desarrolladores, ingenieros de plataforma, líderes técnicos y profesionales técnicos** que ya usan Claude Code o quieren adoptarlo en serio. Si trabajas en freelance o montas servicios para clientes, dominar estos conceptos es directamente vendible: significa entregar más rápido sin perder control sobre el código ni sobre los costes de tokens.

La idea central que recorre todo el temario: **Claude Code no es un autocompletado, es un agente**. Lee tu repositorio, planifica, ejecuta comandos, edita ficheros y verifica su propio trabajo en un bucle. Tu papel es configurar bien ese bucle (contexto, permisos, herramientas) y revisar críticamente la salida.

## Conceptos clave

- **El bucle agéntico (agentic loop).** Claude Code funciona en ciclos: recibe tu petición, razona, decide qué herramienta usar (leer fichero, buscar, ejecutar bash, editar), observa el resultado y repite hasta terminar. Entender esto explica por qué a veces explora varios ficheros antes de actuar y por qué un buen prompt inicial ahorra muchas iteraciones.

- **Contexto y `CLAUDE.md`.** El fichero `CLAUDE.md` (en la raíz del proyecto, en subdirectorios o en `~/.claude/CLAUDE.md` global) es memoria persistente que se carga automáticamente en cada sesión: convenciones del proyecto, comandos de build/test, estilo de código, advertencias. Es la palanca de calidad más rentable. El comando `/init` genera un `CLAUDE.md` inicial analizando tu repo.

- **Herramientas (tools).** Claude Code dispone de herramientas integradas: lectura/escritura/edición de ficheros, búsqueda (Glob, Grep), ejecución de comandos (Bash), navegación web, etc. Cada acción del agente es una llamada a una herramienta que tu entorno (el "harness") ejecuta y controla.

- **Permisos y modos de aprobación.** Por defecto Claude Code pide confirmación antes de acciones con efectos (editar ficheros, ejecutar comandos). Puedes configurar reglas de permiso (`allow`/`deny`/`ask`) en `settings.json`, usar modos como *plan mode* (solo planifica, no ejecuta) o conceder permisos puntuales. La gestión de permisos es el núcleo de la seguridad del agente.

- **Hooks.** Scripts que el harness ejecuta automáticamente en eventos del ciclo de vida (antes/después de una herramienta, al terminar, al recibir un prompt). Sirven para automatizar comportamientos deterministas: formatear código tras cada edición, bloquear comandos peligrosos, lanzar tests. Lo ejecuta el harness, no el modelo.

- **Slash commands (comandos de barra).** Comandos reutilizables: integrados (`/init`, `/clear`, `/config`, `/review`...) y personalizados que defines como ficheros markdown en `.claude/commands/`. Encapsulan prompts o flujos que repites.

- **Subagentes.** Claude Code puede delegar subtareas a agentes secundarios con su propio contexto, a menudo con un modelo más barato (p. ej. para exploración paralela). Reduce el consumo de contexto del agente principal y permite paralelizar.

- **MCP (Model Context Protocol).** Estándar abierto para conectar Claude Code a herramientas y fuentes de datos externas (bases de datos, APIs, servicios como GitHub, Slack, navegador) mediante servidores MCP. Es el mecanismo canónico para extender las capacidades del agente más allá de tu sistema de ficheros.

- **Modelos Claude actuales.** Claude Code usa los modelos de la familia Claude. A día de hoy el referente es **Opus** (`claude-opus-4-8`) para tareas complejas de codificación y agénticas, **Sonnet** (`claude-sonnet-4-6`) para equilibrio velocidad/coste y **Haiku** (`claude-haiku-4-5`) para tareas simples o subagentes. El parámetro **effort** (`low`/`medium`/`high`/`xhigh`/`max`) regula cuánto razona y gasta el modelo; `xhigh` es el valor por defecto en Claude Code para coding.

- **Pensamiento adaptativo (adaptive thinking).** Los modelos modernos deciden por sí mismos cuándo y cuánto razonar antes de actuar. No se configura un presupuesto fijo de tokens de pensamiento; se controla la profundidad con `effort`.

- **Gestión de contexto largo: compactación y context editing.** En sesiones largas, Claude Code resume o purga automáticamente partes antiguas de la conversación para no agotar la ventana de contexto. Saber esto te ayuda a estructurar tareas largas y a no sorprenderte cuando el agente "compacta".

- **Coste y caching.** El consumo se mide en tokens (entrada/salida). El **prompt caching** reutiliza prefijos estables (system prompt, definiciones de herramientas) y abarata enormemente las peticiones repetidas. Un `CLAUDE.md` y un conjunto de herramientas estables favorecen el cacheo.

- **Integración con Git y revisión.** Claude Code se apoya en Git para trabajar de forma segura (branches, commits, diffs) y en `gh` para operaciones de GitHub. Buenas prácticas: ramas dedicadas, commits solo cuando se pide, revisión humana del diff.

## Que necesitas dominar para el certificado

1. **El modelo mental del agente.** Saber explicar el bucle agéntico y por qué Claude Code lee/planifica/ejecuta/verifica. Distinguir agente de simple autocompletado.

2. **Contexto efectivo.** Cuándo y cómo usar `CLAUDE.md` (proyecto vs global vs subdirectorio), qué meter en él, y el papel de `/init`. Reconocer que el contexto bien curado supera a cualquier prompt elaborado.

3. **Permisos y seguridad.** Diferenciar `allow`/`ask`/`deny`, saber qué es el plan mode, configurar `settings.json`, y entender por qué nunca hay que conceder ejecución arbitraria sin control. Conciencia de inyección de prompts vía contenido externo.

4. **Herramientas y hooks.** Saber qué herramientas integradas existen, cuándo promover una acción a herramienta dedicada (gating, auditoría, render), y para qué sirven los hooks (automatización determinista ejecutada por el harness, no por el modelo).

5. **Extensión: MCP, slash commands, subagentes.** Qué es MCP y para qué (conectar servicios externos), cómo crear comandos personalizados, y cuándo delegar en subagentes.

6. **Elección de modelo y effort.** Saber cuándo usar Opus vs Sonnet vs Haiku y cómo el parámetro `effort` afecta a calidad, latencia y coste.

7. **Flujos reales.** Integración con Git/GitHub, ejecución en CI o modo headless/no interactivo, y el SDK de agentes para construir tus propios flujos sobre Claude Code.

8. **Gestión de contexto y coste.** Compactación, caching de prompts y por qué afectan al presupuesto de tokens.

## Plan de estudio

1. **Instala y juega (1-2 h).** Instala Claude Code, ábrelo en un repo de prueba y ejecuta `/init`. Pídele tareas pequeñas (arregla este test, añade esta función) y observa el bucle: cómo lee ficheros, propone un plan y pide permisos.

2. **Domina `CLAUDE.md` (1 h).** Edita el `CLAUDE.md` generado: añade comandos de build/test, convenciones, advertencias. Repite una tarea con y sin esas instrucciones y compara la calidad. Prueba un `CLAUDE.md` global en `~/.claude/`.

3. **Practica permisos (1-2 h).** Explora `/config` y `settings.json`. Configura una regla `allow` para un comando seguro (p. ej. `npm test`) y una regla `deny`. Usa el plan mode para una tarea grande antes de dejar que ejecute.

4. **Crea un slash command y un hook (1-2 h).** Define un comando personalizado en `.claude/commands/` (p. ej. "/review-pr"). Configura un hook que formatee el código tras cada edición. Verifica que el hook lo dispara el harness automáticamente.

5. **Conecta un servidor MCP (1-2 h).** Añade un servidor MCP (por ejemplo, uno de navegador, base de datos o GitHub). Comprueba cómo aparecen sus herramientas y pide a Claude Code que las use.

6. **Experimenta con modelos y effort (1 h).** Cambia de modelo (Opus/Sonnet/Haiku) en una misma tarea y observa diferencias de calidad/velocidad. Prueba distintos niveles de `effort`.

7. **Flujo Git completo (1-2 h).** Haz que Claude Code trabaje en una rama, genere un diff, y úsalo con `/review` y `gh` para una PR simulada. Practica la revisión crítica del diff.

8. **Repasa con flashcards y simulacro (1 h).** Usa las flashcards y el quiz de abajo. Para cada concepto, intenta explicarlo en voz alta sin mirar.

## Errores comunes y tips

- **Pensar que es autocompletado.** Si lo tratas como un copiloto de línea, desaprovechas el 90%. Dale tareas completas y deja que use el bucle agéntico.

- **Descuidar `CLAUDE.md`.** El error más caro. Sin contexto curado, repites las mismas correcciones cada sesión. Inviértele tiempo: es la palanca de calidad número uno.

- **Conceder permisos demasiado amplios.** Dar `allow` a comandos genéricos (o a `bash` sin restricción) es un riesgo de seguridad. Concede permisos estrechos y específicos; usa `deny` para lo peligroso.

- **Confundir hooks con prompts.** Un hook es código determinista que ejecuta el harness en un evento concreto; no es una instrucción al modelo. Si quieres un comportamiento automático garantizado ("siempre que X, haz Y"), es un hook, no una nota en `CLAUDE.md`.

- **No confiar pero tampoco verificar.** El agente puede equivocarse o "alucinar" que algo funciona. Pídele que ejecute los tests y revisa el diff antes de hacer commit. La verificación independiente es parte del trabajo.

- **Ignorar el coste de tokens.** Sesiones muy largas con `effort` alto y mucho contexto cuestan. Aprovecha caching (contexto estable), limpia con `/clear` entre tareas independientes, y usa subagentes/Haiku para subtareas baratas.

- **No usar plan mode para cambios grandes.** Para refactors o features extensos, deja que planifique primero y revisa el plan antes de ejecutar. Ahorra retrabajo.

- **Inyección de prompts.** Trata el contenido externo (issues, páginas web, ficheros de terceros) como potencialmente hostil. Instrucciones escondidas en ese contenido pueden intentar redirigir al agente. Mantén la revisión humana en acciones sensibles.

- **Tip de modelo.** Por defecto, Opus (`claude-opus-4-8`) con `effort: xhigh` para coding serio; baja a Sonnet o reduce effort cuando la latencia o el coste pesen más que la máxima inteligencia.

## Puntos clave para recordar

- Claude Code es un **agente** que opera en un bucle leer → planificar → ejecutar herramientas → verificar.
- **`CLAUDE.md`** es memoria persistente de proyecto/global y la mayor palanca de calidad; `/init` lo genera.
- Los **permisos** (`allow`/`ask`/`deny`) y el **plan mode** son el núcleo de la seguridad; concede permisos estrechos.
- Los **hooks** son automatización determinista ejecutada por el harness en eventos del ciclo de vida, no instrucciones al modelo.
- Los **slash commands** personalizados viven en `.claude/commands/` como markdown.
- **MCP** es el estándar para conectar herramientas y datos externos; los **subagentes** delegan subtareas (a menudo con modelo más barato).
- Modelos actuales: **Opus `claude-opus-4-8`** (complejo/agéntico), **Sonnet `claude-sonnet-4-6`** (equilibrio), **Haiku `claude-haiku-4-5`** (simple/rápido); **effort** regula razonamiento y coste.
- **Pensamiento adaptativo**: el modelo decide cuánto razonar; no hay presupuesto fijo de tokens de pensamiento.
- **Compactación**, **context editing** y **prompt caching** gestionan contexto largo y coste.
- Integración con **Git/GitHub** y revisión crítica del diff: nunca hagas commit a ciegas; verifica con tests.
- Trata el **contenido externo como no confiable** (riesgo de inyección de prompts).
