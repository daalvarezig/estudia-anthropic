## Resumen

**Agent Skills** (Habilidades de Agente) son paquetes de instrucciones, scripts y recursos que enseñan a Claude a realizar tareas especializadas de forma fiable y repetible. En lugar de pegar las mismas instrucciones largas en cada conversación, empaquetas ese conocimiento una vez en una carpeta con un archivo `SKILL.md`, y Claude lo carga **solo cuando es relevante**.

La idea central es el **progressive disclosure** (revelación progresiva): Claude no carga todo el contenido de la skill de golpe. Primero ve únicamente el nombre y la descripción (unas pocas decenas de tokens); si la tarea encaja, lee el cuerpo del `SKILL.md`; y solo si lo necesita abre los archivos adicionales o ejecuta los scripts. Así se ahorra contexto y se pueden tener muchísimas skills disponibles sin saturar la ventana del modelo.

Esta certificación de **Anthropic Academy** ("Introduction to Agent Skills") es introductoria. Está pensada para desarrolladores, equipos técnicos y usuarios avanzados de Claude (Claude.ai, Claude Code, la API/Agent SDK) que quieran entender **qué son las skills, cómo se estructuran, cuándo usarlas frente a otras técnicas (MCP, herramientas, prompts) y cómo crearlas siguiendo buenas prácticas**. No requiere ser ingeniero de IA, pero sí estar cómodo con carpetas, Markdown y, opcionalmente, scripts.

## Conceptos clave

- **Agent Skill**: carpeta autocontenida que extiende las capacidades de Claude para una tarea concreta. Contiene como mínimo un `SKILL.md` y puede incluir scripts, plantillas y documentos de referencia.
- **SKILL.md**: el archivo obligatorio y punto de entrada de la skill. Tiene dos partes: un **frontmatter YAML** (metadatos) y un **cuerpo en Markdown** con las instrucciones que Claude seguirá.
- **Frontmatter YAML**: bloque al inicio del `SKILL.md` delimitado por `---`. Campos principales: `name` (identificador) y `description` (cuándo y para qué usar la skill). Es lo único que Claude lee al arrancar para decidir si la skill aplica.
- **`description` (el campo más importante)**: texto que describe **qué hace la skill y cuándo activarla**. Determina si Claude la selecciona. Debe ser específica e incluir disparadores (palabras clave, tipos de archivo, situaciones). Una mala `description` hace que la skill no se active nunca o se active de más.
- **Progressive disclosure (revelación progresiva)**: modelo de carga en tres niveles. (1) Metadatos siempre visibles → (2) cuerpo del `SKILL.md` al activarse → (3) archivos/recursos enlazados solo bajo demanda. Optimiza el uso de la ventana de contexto.
- **Recursos adicionales (bundled resources)**: archivos que acompañan a la skill: scripts ejecutables (Python, Bash, etc.), plantillas, ejemplos o documentación larga que Claude lee o ejecuta cuando hace falta.
- **Scripts ejecutables**: código que Claude puede ejecutar (en entornos con ejecución de código) para tareas deterministas y repetibles, evitando "reinventar" la lógica en cada conversación y reduciendo errores.
- **Composabilidad**: varias skills pueden combinarse en una misma tarea; Claude usa las que apliquen. Conviene que cada skill sea modular y de propósito único.
- **Portabilidad multiplataforma**: el mismo formato de skill funciona en Claude.ai (Claude Apps), en Claude Code y a través de la **API / Agent SDK**, así como en despliegues sobre **Amazon Bedrock** y **Google Vertex AI**. Es un estándar abierto y simple (carpeta + Markdown).
- **Skills vs. MCP vs. herramientas**: las **skills** aportan conocimiento procedimental (el "cómo" hacer algo); **MCP** y las **tools/funciones** aportan acceso a datos y acciones (conectores, APIs, sistemas). Se complementan: una skill puede indicar a Claude cómo usar bien una herramienta o un servidor MCP.
- **Activación por relevancia (model-invoked)**: Claude decide autónomamente cuándo cargar una skill basándose en la `description` y el contexto de la conversación. No es el usuario quien "llama" manualmente a la skill en el flujo normal.
- **Skills personales vs. de proyecto/organización**: pueden vivir a nivel de usuario (disponibles en todas tus sesiones) o a nivel de proyecto/equipo (compartidas y versionadas con el repositorio).
- **Seguridad y confianza**: como una skill puede ejecutar código, solo deben instalarse skills de fuentes fiables. Hay que revisar scripts y evitar incluir secretos o credenciales dentro de la skill.
- **`allowed-tools` (opcional)**: campo que permite restringir qué herramientas puede usar Claude mientras la skill está activa, acotando el alcance por seguridad.

## Que necesitas dominar para el certificado

1. **Definición y propósito**: saber explicar con tus palabras qué es una Agent Skill y qué problema resuelve (reutilizar conocimiento experto sin repetir prompts; especializar a Claude).
2. **Estructura mínima**: que toda skill es una carpeta cuyo punto de entrada obligatorio es `SKILL.md`, formado por frontmatter YAML + cuerpo Markdown.
3. **Campos del frontmatter**: identificar `name` y, sobre todo, `description`, y entender por qué la `description` es crítica para la activación.
4. **Progressive disclosure**: explicar los tres niveles de carga y por qué ahorran contexto.
5. **Cuándo usar skills frente a otras técnicas**: distinguir skill (conocimiento/procedimiento) de MCP (conexión a sistemas) y de herramientas/funciones (acciones). Saber que se complementan.
6. **Multiplataforma**: reconocer que el mismo formato sirve en Claude.ai, Claude Code, API/Agent SDK, Bedrock y Vertex.
7. **Buenas prácticas de creación**: descripciones específicas con disparadores, instrucciones concretas, skills de propósito único, mover el detalle largo a archivos de referencia, usar scripts para lo determinista.
8. **Activación model-invoked**: entender que Claude elige la skill por relevancia, no el usuario manualmente.
9. **Seguridad**: instalar solo skills de confianza, revisar scripts, no incrustar secretos.

## Plan de estudio

1. **Haz el curso oficial** "Introduction to Agent Skills" en Anthropic Academy de principio a fin, tomando notas de los términos exactos (`SKILL.md`, frontmatter, progressive disclosure, description).
2. **Lee la documentación de Skills** en docs.anthropic.com y la guía de buenas prácticas (best practices) para crear skills. Fíjate en los ejemplos del repositorio público de skills de Anthropic.
3. **Crea tu primera skill a mano**: una carpeta con `SKILL.md`, escribe un frontmatter con `name` y `description`, y un cuerpo con pasos claros. Pruébala en Claude Code o Claude.ai y observa cuándo se activa.
4. **Itera la `description`**: cambia el texto para que sea más específico y comprueba cómo mejora la activación. Este ejercicio fija el concepto más evaluado.
5. **Añade progressive disclosure**: divide el contenido largo en archivos de referencia que el `SKILL.md` enlace, y añade un script simple para una tarea determinista.
6. **Compara con MCP y tools**: monta o revisa un servidor MCP o una herramienta y razona qué iría en la skill (el "cómo") y qué en el conector (el acceso).
7. **Prueba portabilidad**: ejecuta la misma skill en al menos dos entornos (p. ej. Claude Code y la API/Agent SDK) para interiorizar que el formato es común.
8. **Repaso final**: usa estas flashcards y el quiz; relee "Errores comunes" la víspera del examen.

## Errores comunes y tips

- **Confundir `name` con `description`**: el `name` identifica; la `description` decide la activación. La pregunta de examen suele apuntar a la `description`.
- **Pensar que el usuario llama a la skill manualmente**: en el flujo normal es **Claude** quien la invoca por relevancia (model-invoked). 
- **Creer que Claude carga toda la skill siempre**: falso; es **progressive disclosure** en tres niveles.
- **Hacer skills monstruo**: una skill que intenta hacer de todo se activa mal. Mejor varias skills modulares de propósito único.
- **Descripciones vagas** ("ayuda con documentos"): no aportan disparadores. Sé concreto: tipos de archivo, acciones, situaciones.
- **Mezclar conceptos**: una skill **no** es un servidor MCP ni una herramienta; aporta conocimiento procedimental que puede *complementar* a ambos.
- **Olvidar la seguridad**: instalar skills de terceros sin revisar scripts, o meter API keys dentro de la skill.
- **Tip de formato**: recuerda que el frontmatter va entre `---` y es YAML; el resto es Markdown estándar.
- **Tip de contexto**: pon lo esencial en el cuerpo del `SKILL.md` y mueve referencias largas a archivos aparte para no malgastar tokens.

## Puntos clave para recordar

- Una **Agent Skill** = carpeta con un `SKILL.md` (frontmatter YAML + cuerpo Markdown) + recursos opcionales.
- El campo **`description`** es lo más importante: define **qué** hace y **cuándo** usarla; gobierna la activación.
- **Progressive disclosure** en 3 niveles: metadatos → cuerpo → recursos bajo demanda. Ahorra contexto.
- Las skills son **model-invoked**: Claude las elige por relevancia.
- Mismo formato **portátil** en Claude.ai, Claude Code, API/Agent SDK, Bedrock y Vertex.
- **Skills ≠ MCP ≠ tools**, pero se **complementan**: skills = "cómo"; MCP/tools = acceso y acciones.
- Buenas prácticas: descripciones específicas con disparadores, propósito único, scripts para lo determinista, referencias largas en archivos aparte.
- **Seguridad**: instala solo skills de confianza, revisa los scripts, nunca incluyas secretos.