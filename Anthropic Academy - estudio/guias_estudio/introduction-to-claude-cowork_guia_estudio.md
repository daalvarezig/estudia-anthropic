## Resumen

**Claude Cowork** es la herramienta agéntica de escritorio de Anthropic pensada para el *trabajo del conocimiento*: en lugar de chatear, le das a Claude un objetivo y este planifica y ejecuta tareas de varios pasos directamente sobre tus archivos, carpetas y aplicaciones locales, devolviéndote un entregable terminado. La diferencia mental clave es **"resultado, no prompt"**: con Chat conversas; con Cowork abres una *sesión de trabajo* que orientas (steering) mientras Claude opera.

Está orientada a perfiles **no técnicos** (analistas, operaciones, legal, finanzas, investigación) que pasan el día con documentos y datos y prefieren dedicar el tiempo a las decisiones de criterio antes que al ensamblaje. Comparte la arquitectura de agente de **Claude Code**, pero con una interfaz de chat familiar y sin necesidad de escribir una línea de código.

La certificación oficial **"Introduction to Claude Cowork"** (Anthropic Academy, vía Skilljar) es gratuita, hands-on y se aprueba con un quiz final. El certificado incluye URL de verificación, se añade a LinkedIn y no caduca. El curso se estructura en cuatro bloques: *Meet Claude Cowork*, *Make Claude Cowork yours*, *Use Claude wherever you work* y *Sharing and safety in Claude Cowork*. Esta guía cubre exactamente esos cuatro ejes.

## Conceptos clave

- **Cowork task loop (bucle de tarea):** el ciclo central. (1) Describes un objetivo en lenguaje natural; (2) Claude **planifica** y descompone la tarea en pasos; (3) **ejecuta** en un entorno controlado, mostrando el progreso; (4) **se detiene en "approval gates"** antes de acciones destructivas (borrados, sobrescrituras); (5) entrega un **resumen** final. Tú orientas (steering) en cualquier punto.

- **Trabajo sobre carpetas locales ("Work in a Folder"):** activas el acceso a una carpeta concreta y Claude puede leer, editar, mover, renombrar y (con permiso) borrar archivos. Esto contrasta con Chat, que solo acepta archivos subidos con límites de tamaño y cantidad.

- **Permisos y control humano:** al dar acceso a una carpeta eliges entre **acceso de una sola vez** o **"Always Allow"** (persistente). Las decisiones consecuentes quedan siempre en manos del usuario; Claude pide confirmación explícita antes de borrar o de pasos irreversibles.

- **Contexto permanente (standing context):** lo que moldea el plan de Claude. Se apila por capas: **instrucciones globales / preferencias de perfil** (se cargan siempre), **Projects** (se añaden al abrir ese proyecto), y **Skills** (se activan solo cuando son relevantes). Buena práctica: instrucciones globales cortas; el detalle, en skills.

- **Projects (Proyectos):** un espacio de trabajo persistente para *un cuerpo de trabajo*, con sus propios archivos, instrucciones y memoria afinados para tareas agénticas. Úsalo cuando Claude "pierde el hilo" de un trabajo recurrente.

- **Skills (Habilidades):** carpetas con un fichero de instrucciones (p. ej. `SKILL.md`), scripts y recursos que Claude **carga dinámicamente** cuando una tarea encaja. Resuelven la *inconsistencia entre ejecuciones*: codifican cómo hacer una tarea repetible en tu contexto. Existen skills nativas de Office (docx, xlsx, pdf, pptx).

- **Plugins:** unidad instalable que **empaqueta** varias skills + conectores (MCP) + comandos + subagentes para una función de trabajo concreta. Es el formato para **distribuir y reutilizar** una configuración entre un equipo.

- **Connectors / MCP:** conexiones a apps y datos externos (Settings > Connectors). Permiten flujos híbridos: datos externos que alimentan archivos locales, o datos locales que disparan acciones externas. MCP (Model Context Protocol) es el estándar abierto que conecta a Claude con herramientas externas.

- **Claude en Chrome:** integración de navegador para automatización web (navegar pestañas, clicar botones, rellenar formularios, capturar pantallas). Potente pero **lento**, porque cada interacción requiere capturas de pantalla; mejor para flujos puntuales que para volumen masivo.

- **Microsoft 365 / Office:** Cowork trabaja en Word, Excel, PowerPoint y Outlook usando las skills de documento (generar borradores estructurados, extraer datos, montar informes).

- **Disponibilidad:** se accede desde la **app de escritorio de Claude** en planes de pago. La automatización de archivos locales y la app de escritorio son el corazón de Cowork.

## Que necesitas dominar para el certificado

1. **El task loop completo** y, sobre todo, dónde y por qué Claude **se detiene a pedir aprobación** (acciones destructivas). Esto cae casi seguro en el quiz.
2. **La diferencia Chat vs Cowork vs Claude Code:** Chat = consejo conversacional (solo archivos subidos); Cowork = ejecución operativa sobre tu sistema para no-devs; Claude Code = automatización técnica en terminal para desarrolladores.
3. **Cuándo usar Project, Skill, Plugin o Connector** (la pregunta de diseño más típica): cuerpo de trabajo persistente → Project; inconsistencia entre ejecuciones → Skill; actuar en otra app → Connector; reutilizar en equipo → Plugin.
4. **Cómo funciona el contexto por capas** y por qué conviene que las instrucciones globales sean cortas (se cargan siempre y gastan contexto).
5. **Modelo de permisos:** one-time vs Always Allow; el principio de que las decisiones consecuentes son del humano.
6. **Integraciones:** qué hace Claude en Chrome y en Office 365, y sus límites (lentitud del navegador, parsing frágil de Excel con celdas combinadas / formato de presentación).
7. **Sharing & safety:** validar una skill antes de confiar en ella, revisar lo que produce antes de compartirlo con el equipo, y empaquetar configuraciones probadas como plugins.

## Plan de estudio

1. **Instala y abre** la app de escritorio de Claude y ejecuta **una tarea end-to-end real** sobre una carpeta de prueba (p. ej. ordenar una carpeta de descargas). Observa el bucle: plan → ejecución → approval gate → resumen.
2. **Juega con los permisos:** concede acceso one-time, luego Always Allow, y fíjate en cuándo Claude pide confirmación para borrar.
3. **Crea un Project** para un trabajo recurrente con instrucciones propias; comprueba cómo cambia el plan al darle contexto.
4. **Crea o instala una Skill** (p. ej. usa las skills de Office) y observa que solo se activa cuando la tarea encaja. Después, **explora un plugin** para ver cómo agrupa skills + conectores.
5. **Conecta Cowork a Chrome** y haz un flujo web sencillo; nota la latencia. Prueba generar un Word/Excel/PowerPoint desde archivos fuente.
6. **Repasa el árbol de decisión** Project/Skill/Plugin/Connector hasta poder recitarlo.
7. **Haz el quiz de práctica mentalmente** con cada concepto y luego el quiz oficial. Repasa especialmente seguridad y aprobaciones.

## Errores comunes y tips

- **Confundir Cowork con Chat:** Chat solo lee archivos *subidos*; Cowork actúa directamente sobre el sistema de archivos. No respondas "subes el archivo" en preguntas de Cowork.
- **Creer que Claude borra sin avisar:** falso. Cowork **pide confirmación** antes de acciones destructivas; ese approval gate es un punto de examen.
- **Mezclar Skill y Plugin:** una Skill es *una* instrucción reutilizable; un Plugin **empaqueta** varias skills + conectores + comandos para distribuir, normalmente a un equipo.
- **Meter todo en instrucciones globales:** se cargan siempre y consumen contexto. Pon el conocimiento específico en skills, que se activan bajo demanda.
- **Esperar que la automatización de Chrome sea rápida:** es lenta por las capturas de pantalla; no es la herramienta para 250 correos sin paciencia.
- **Confiar a ciegas en el parsing de Excel:** la skill xlsx asume datos columnares limpios; con celdas combinadas o formato de presentación falla. Revisa siempre.
- **Saltarse la validación antes de compartir:** valida la skill y revisa el output antes de hacerlo equipo. La seguridad es responsabilidad del que orienta.

## Puntos clave para recordar

- Cowork = **objetivo, no prompt**; Claude planifica y ejecuta sobre tus archivos y apps, y tú orientas.
- El **task loop**: describir → planificar → ejecutar → **aprobar acciones destructivas** → resumen.
- Permisos: **one-time** o **Always Allow**; las decisiones consecuentes son siempre del humano.
- **Project** = cuerpo de trabajo persistente; **Skill** = instrucción reutilizable que se activa sola; **Plugin** = paquete de skills+conectores para reutilizar/compartir; **Connector/MCP** = puente a apps externas.
- El **contexto se apila** (globales + project + skills); mantén las instrucciones globales cortas.
- Integra con **Chrome** (automatización web, lenta) y **Microsoft 365** (Word, Excel, PowerPoint, Outlook) vía skills de documento.
- Comparte la **arquitectura de Claude Code** pero para no-devs, con UI de chat; disponible en la **app de escritorio** en planes de pago.
- **Sharing & safety:** valida skills, revisa outputs y empaqueta lo probado antes de llevarlo al equipo.
