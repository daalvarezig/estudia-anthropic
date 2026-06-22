## Resumen

**Claude Code** es la herramienta de codificacion agentica de Anthropic que vive en tu terminal. En lugar de copiar y pegar codigo en una ventana de chat, Claude Code opera directamente sobre tu repositorio: lee y edita ficheros, ejecuta comandos de shell, corre tests, hace commits y navega por tu base de codigo con tus permisos. Es "agentico" porque no se limita a responder, sino que planifica, actua sobre el entorno, observa el resultado y itera hasta cumplir el objetivo.

La certificacion **"Claude Code 101"** de Anthropic Academy es el nivel introductorio. Esta pensada para desarrolladores, data scientists, technical writers y cualquier persona tecnica que quiera incorporar Claude Code a su flujo de trabajo. No exige ser experto: evalua que entiendas que es Claude Code, como instalarlo y autenticarte, el bucle agentico, los comandos y flujos esenciales, como dar contexto al modelo (CLAUDE.md), gestionar permisos de forma segura, usar MCP y los modos de uso (interactivo, plan y "headless"/no interactivo). Es la base sobre la que se construyen certificaciones mas avanzadas (subagents, hooks, automatizacion en CI, SDK).

Esta guia es un repaso independiente y original para que llegues al examen con los conceptos firmes y sin sorpresas.

## Conceptos clave

- **Codificacion agentica (agentic coding)**: paradigma en el que el modelo no solo sugiere texto, sino que ejecuta acciones reales (leer/editar ficheros, lanzar comandos, correr tests) en un bucle de observar -> actuar -> verificar. Claude Code es la implementacion de Anthropic de este paradigma en la terminal.
- **El bucle agentico (gather context -> take action -> verify)**: Claude reune contexto (busca y lee ficheros), realiza una accion (edita, ejecuta) y verifica el resultado (lee la salida, corre tests). Repite hasta resolver la tarea. Entender este bucle es central para el examen.
- **Instalacion y autenticacion**: se instala normalmente como paquete npm (`npm install -g @anthropic-ai/claude-code`) y se lanza con el comando `claude` dentro del directorio del proyecto. Te autenticas con una cuenta Claude (planes Pro/Max) o con una API key de la Anthropic Console (consumo facturado por tokens). Tambien funciona sobre **Amazon Bedrock** y **Google Vertex AI** para entornos empresariales.
- **CLAUDE.md**: fichero de memoria/contexto del proyecto. Claude lo lee automaticamente al arrancar. Sirve para documentar comandos de build/test, convenciones de estilo, arquitectura y reglas del repo. Hay variantes: `CLAUDE.md` de proyecto (compartido en git), `CLAUDE.local.md` o `~/.claude/CLAUDE.md` (personal/global). El comando `/init` genera uno inicial analizando el repo.
- **Modos de operacion**: modo interactivo (REPL en la terminal), **modo plan** (Claude propone un plan y no toca nada hasta que apruebas; util para tareas grandes), y modo **headless / no interactivo** (`claude -p "prompt"`) para scripting, pipelines y CI.
- **Permisos y seguridad**: Claude Code pide aprobacion antes de acciones sensibles (editar ficheros, ejecutar comandos, acceder a la red). Puedes permitir/denegar por accion, gestionar reglas en `settings.json` (allowlist/denylist), o usar modos como auto-aceptar ediciones. La filosofia es "human in the loop" por defecto.
- **Slash commands**: comandos que empiezan por `/`, como `/init`, `/clear` (limpia el contexto), `/compact` (resume el contexto para liberar tokens), `/help`, `/model`, `/review`. Tambien puedes crear **custom slash commands** guardando ficheros markdown en `.claude/commands/`.
- **MCP (Model Context Protocol)**: estandar abierto de Anthropic para conectar Claude a herramientas y fuentes de datos externas (bases de datos, GitHub, Slack, navegadores, sistemas de ficheros) mediante "servidores MCP". Amplia lo que Claude Code puede ver y hacer mas alla del repo local.
- **Subagents**: agentes especializados que Claude Code puede invocar para tareas concretas (cada uno con su propio contexto y, opcionalmente, su propio conjunto de herramientas). Permiten dividir trabajo y mantener limpio el contexto principal.
- **Hooks**: scripts de shell que se disparan automaticamente en ciertos eventos del ciclo de vida (p. ej. antes/despues de una edicion o de ejecutar una herramienta). Sirven para forzar formateo, linting, tests o politicas sin depender de que el modelo "se acuerde".
- **Gestion del contexto / la ventana de contexto**: el modelo tiene un limite de tokens. Sesiones largas lo llenan; por eso existen `/clear` (empezar de cero) y `/compact` (resumir). Mantener el contexto enfocado mejora calidad, velocidad y coste.
- **Modelos Claude actuales**: la familia incluye **Opus** (maxima capacidad de razonamiento, ideal para tareas complejas), **Sonnet** (equilibrio rendimiento/coste, el caballo de batalla diario) y **Haiku** (rapido y economico). Claude Code permite cambiar de modelo con `/model`.
- **Thinking / razonamiento extendido**: Claude puede dedicar mas "pensamiento" a problemas dificiles. En la practica se invoca con palabras clave como "think" / "think hard" para que dedique mas razonamiento antes de actuar.
- **Integraciones de ecosistema**: el SDK/CLI permite construir agentes propios; hay integraciones con IDEs (VS Code, JetBrains), con **GitHub Actions** para revisiones y tareas automaticas en PRs, y con plataformas cloud (Bedrock, Vertex).
- **AI Fluency**: marco de Anthropic sobre como colaborar bien con la IA (delegacion, descripcion clara de la tarea, discernimiento/verificacion y uso responsable). Subyace a las buenas practicas de prompting en Claude Code: da contexto, define el objetivo, revisa lo que produce.

## Que necesitas dominar para el certificado

1. **Que es Claude Code y en que se diferencia** de un chat: agentico, en terminal, actua sobre el repo real.
2. **Instalacion y autenticacion**: comando de instalacion npm, lanzar con `claude`, opciones de auth (cuenta Claude vs API key) y que tambien corre sobre Bedrock/Vertex.
3. **El bucle agentico**: reunir contexto, actuar, verificar; y como Claude descubre tu codigo (busqueda + lectura de ficheros, no necesita que se lo pegues todo).
4. **CLAUDE.md y `/init`**: para que sirve, donde se ubica, niveles (proyecto vs personal vs global) y como mejora los resultados.
5. **Comandos esenciales**: `/init`, `/clear`, `/compact`, `/help`, `/model`, `/review`, y como crear comandos personalizados.
6. **Modos**: interactivo, plan mode y headless (`-p`) para automatizar.
7. **Permisos y seguridad**: aprobaciones, allow/deny, `settings.json`, y por que el "human in the loop" importa.
8. **MCP**: que es, para que se usa, como conecta herramientas externas.
9. **Subagents y hooks**: que son y cuando usarlos (nivel conceptual para 101).
10. **Modelos y gestion de contexto**: cuando usar Opus vs Sonnet vs Haiku; por que y como limpiar/compactar el contexto.

## Plan de estudio

1. **Instala y arranca**: ejecuta `npm install -g @anthropic-ai/claude-code`, entra en un proyecto real y lanza `claude`. Autentica con tu cuenta o API key.
2. **Genera tu CLAUDE.md**: corre `/init` y lee lo que genera. Anade a mano un par de comandos de build/test y una convencion de estilo; observa como cambia el comportamiento.
3. **Practica el bucle agentico**: pide una tarea pequena ("anade un test para X", "arregla este bug") y observa como reune contexto, actua y verifica. Aprende a leer sus propuestas antes de aprobar.
4. **Domina los comandos**: usa `/clear` entre tareas distintas, `/compact` en sesiones largas, `/model` para cambiar de modelo, `/review` sobre un diff. Crea un slash command propio en `.claude/commands/`.
5. **Prueba los modos**: usa plan mode para una tarea de varios pasos; luego prueba headless con `claude -p "resume los cambios del ultimo commit"`.
6. **Configura permisos**: revisa `settings.json`, crea una allowlist para comandos seguros y entiende cuando Claude te pedira confirmacion.
7. **Conecta un MCP**: anade un servidor MCP sencillo (p. ej. acceso a un sistema de ficheros o a GitHub) y comprueba como amplia las capacidades.
8. **Explora conceptos avanzados a nivel teorico**: lee sobre subagents y hooks lo suficiente para reconocer para que sirven.
9. **Repasa con flashcards y simulacros**: usa las tarjetas y el quiz de esta guia; vuelve a cualquier concepto que falles.
10. **Conecta con AI Fluency**: practica describir tareas con contexto y objetivo claros, y verifica siempre la salida.

## Errores comunes y tips

- **No darle contexto** y luego quejarse del resultado: usa CLAUDE.md y describe el objetivo, no solo el sintoma. Da rutas de fichero, comandos de test y restricciones.
- **Dejar el contexto crecer sin limite**: en sesiones largas la calidad baja y el coste sube. Usa `/clear` al cambiar de tarea y `/compact` cuando se acumule historial.
- **Confundir Claude Code con un chatbot**: actua sobre tu maquina y tu repo. Revisa los diffs y aprueba con criterio; activa allowlists solo para comandos que de verdad sean seguros.
- **Aprobar comandos a ciegas**: el "human in the loop" existe por seguridad. No des `--dangerously-skip-permissions` ni auto-aceptes todo en repos importantes sin entender el riesgo.
- **Usar siempre el modelo mas potente**: Opus no siempre es necesario; Sonnet cubre la mayoria del trabajo diario con mejor coste/latencia y Haiku va perfecto para tareas simples y rapidas.
- **Saltarse el plan mode en tareas grandes**: pedir un plan primero reduce reescrituras y desvios. Verifica el plan antes de ejecutar.
- **Olvidar que MCP existe**: si la tarea necesita datos externos (BD, issues de GitHub, web), un servidor MCP suele ser mejor que pegar contexto manualmente.
- **No verificar**: pide que corra los tests o muestra la salida. El paso de "verify" del bucle agentico es lo que separa una buena sesion de una mala.
- **Tip de prompting**: para problemas dificiles, pide explicitamente que "piense" antes de actuar; el razonamiento extendido mejora la calidad en tareas complejas.

## Puntos clave para recordar

- Claude Code es **codificacion agentica en la terminal**: reune contexto, actua y verifica, sobre tu repo real.
- Se instala via **npm** (`@anthropic-ai/claude-code`), se lanza con `claude`, y se autentica con cuenta Claude o API key; corre tambien en **Bedrock** y **Vertex**.
- **CLAUDE.md** es la memoria del proyecto; `/init` lo crea. Buen contexto = mejores resultados.
- Comandos clave: `/init`, `/clear`, `/compact`, `/model`, `/review`, `/help`; y comandos personalizados en `.claude/commands/`.
- Tres formas de uso: **interactivo**, **plan mode** y **headless** (`-p`) para automatizar/CI.
- La **seguridad** es por permisos con humano en el bucle; gestiona allow/deny en `settings.json`.
- **MCP** conecta herramientas externas; **subagents** dividen trabajo; **hooks** automatizan acciones en eventos.
- Modelos: **Opus** (complejo), **Sonnet** (diario), **Haiku** (rapido/barato).
- Gestiona la **ventana de contexto** con `/clear` y `/compact`.
- Las buenas practicas se apoyan en **AI Fluency**: delega bien, describe con claridad, verifica con discernimiento.