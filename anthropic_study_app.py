import json
import random
import re
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "Anthropic Academy - estudio"
GUIDES_DIR = DATA_DIR / "guias_estudio"
COURSES_JSON = DATA_DIR / "courses_enriched.json"


st.set_page_config(
    page_title="Estudia Anthropic",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_courses():
    if not COURSES_JSON.exists():
        return []
    return json.loads(COURSES_JSON.read_text(encoding="utf-8"))


def clean_text(text: str) -> str:
    return (
        text.replace("â†’", "->")
        .replace("â€™", "'")
        .replace("â€œ", '"')
        .replace("â€", '"')
        .replace("â€”", "-")
        .strip()
    )


def slug(path_or_title: str) -> str:
    value = path_or_title.strip("/").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


COURSE_PROFILES = {
    "ai-fluency-framework-foundations": {
        "nivel": "Base",
        "color": "#6B7A45",
        "para_que": "Aprender a colaborar con IA de forma efectiva, segura y responsable usando el marco 4D.",
        "skills": ["AI Literacy", "Generative AI", "Responsible AI", "Human-AI Collaboration"],
        "cards": [
            ("Delegación", "Decidir qué hace la persona, qué hace la IA y qué conviene hacer en colaboración."),
            ("Descripción", "Dar contexto, objetivo, audiencia, formato, restricciones y criterios de éxito."),
            ("Discernimiento", "Evaluar exactitud, utilidad, sesgos, supuestos y adecuación antes de aceptar una salida."),
            ("Diligencia", "Proteger datos, verificar resultados, ser transparente y asumir responsabilidad final."),
        ],
    },
    "claude-101": {
        "nivel": "Base",
        "color": "#5B6FA8",
        "para_que": "Dominar Claude para tareas diarias: redactar, resumir, investigar, analizar y organizar trabajo.",
        "skills": ["Claude", "Generative AI", "Prompt Engineering", "AI Productivity"],
        "cards": [
            ("Uso diario", "Claude sirve como apoyo para escritura, síntesis, análisis, ideas y planificación."),
            ("Buen contexto", "Cuanto mejor expliques objetivo, audiencia y material, más útil será la respuesta."),
            ("Iteración", "No busques la primera respuesta perfecta: refina con feedback concreto."),
            ("Verificación", "Contrasta datos importantes y no delegues decisiones críticas sin revisión humana."),
        ],
    },
    "ai-capabilities-and-limitations": {
        "nivel": "Base",
        "color": "#AA6A44",
        "para_que": "Entender qué puede hacer la IA generativa, dónde falla y cómo diagnosticar sus límites.",
        "skills": ["AI Literacy", "Critical Thinking", "Responsible AI", "AI Risk Assessment"],
        "cards": [
            ("Predicción", "Los modelos generan texto prediciendo continuaciones probables, no consultando una verdad interna."),
            ("Conocimiento", "Pueden sonar convincentes y aun así inventar datos o citas."),
            ("Memoria de trabajo", "Solo atienden al contexto disponible; lo que no está en contexto puede perderse."),
            ("Dirección", "Las instrucciones mejoran resultados, pero no garantizan obediencia perfecta."),
        ],
    },
    "introduction-to-claude-cowork": {
        "nivel": "Productividad",
        "color": "#7A5B9E",
        "para_que": "Trabajar con Claude sobre archivos, proyectos y tareas largas con un ciclo de delegación real.",
        "skills": ["AI Productivity", "Human-AI Collaboration", "Workflow Automation", "AI Agents"],
        "cards": [
            ("No es solo chat", "Cowork está pensado para ejecutar trabajo multi-paso y entregar artefactos."),
            ("Contexto de trabajo", "Puede usar carpetas, documentos, conectores y reglas del proyecto."),
            ("Plan y ejecución", "Conviene revisar el plan, dejar que avance y corregir con checkpoints."),
            ("Control humano", "Las acciones sensibles deben supervisarse: enviar, borrar, compartir o publicar."),
        ],
    },
    "claude-code-101": {
        "nivel": "Técnico",
        "color": "#2F756B",
        "para_que": "Usar Claude Code en desarrollo: explorar código, planificar cambios, implementar, probar y revisar.",
        "skills": ["AI-Assisted Software Development", "Claude Code", "Debugging", "Code Review"],
        "cards": [
            ("Explorar", "Antes de editar, Claude debe leer el repositorio y entender patrones existentes."),
            ("Planificar", "Plan Mode ayuda a revisar enfoque antes de tocar código."),
            ("Implementar", "La IA puede editar, ejecutar comandos y verificar resultados en el entorno."),
            ("Revisar", "El humano conserva criterio sobre arquitectura, seguridad y cambios finales."),
        ],
    },
    "claude-platform-101": {
        "nivel": "Técnico",
        "color": "#3C6FA1",
        "para_que": "Comprender la plataforma de desarrollo de Claude: modelos, API, herramientas, agentes y límites.",
        "skills": ["AI Application Development", "Claude API", "LLM", "AI Agents"],
        "cards": [
            ("Modelos", "Elegir entre velocidad, coste e inteligencia según el caso de uso."),
            ("API", "Una app envía contexto estructurado, parámetros y mensajes al modelo."),
            ("Herramientas", "Claude puede pedir ejecutar tools para actuar sobre sistemas externos."),
            ("Coste y contexto", "Diseñar bien implica controlar tokens, latencia, seguridad y memoria."),
        ],
    },
    "claude-with-the-anthropic-api": {
        "nivel": "Técnico",
        "color": "#315F8A",
        "para_que": "Construir aplicaciones con la API de Anthropic: prompts, evaluación, tools, RAG, MCP y agentes.",
        "skills": ["Claude API", "API Integration", "RAG", "AI Agents", "Prompt Evaluation"],
        "cards": [
            ("Mensajes", "Las conversaciones se mantienen reenviando historial; la API no recuerda por sí sola."),
            ("System prompts", "Definen rol, estilo y comportamiento estable del asistente."),
            ("Tools", "Permiten que Claude solicite acciones estructuradas a tu aplicación."),
            ("Evaluación", "Los prompts se deben medir con datasets, criterios y graders, no solo probar a ojo."),
            ("RAG", "Recupera información externa relevante para responder con más contexto y menos invención."),
        ],
    },
    "introduction-to-model-context-protocol": {
        "nivel": "Avanzado",
        "color": "#8A6F35",
        "para_que": "Aprender MCP para conectar Claude con herramientas, datos y prompts externos de forma estándar.",
        "skills": ["Model Context Protocol", "AI Tools", "API Integration", "Agentic AI"],
        "cards": [
            ("Tools", "Acciones que el modelo puede decidir usar para completar una tarea."),
            ("Resources", "Datos que la aplicación puede leer y aportar al contexto."),
            ("Prompts", "Flujos preparados que el usuario puede invocar con parámetros."),
            ("Cliente y servidor", "El cliente consume capacidades; el servidor expone tools, resources y prompts."),
        ],
    },
    "model-context-protocol-advanced-topics": {
        "nivel": "Avanzado",
        "color": "#735A34",
        "para_que": "Profundizar en MCP de producción: transporte, notificaciones, sampling y acceso a archivos.",
        "skills": ["Model Context Protocol", "AI Infrastructure", "Agentic AI", "Software Architecture"],
        "cards": [
            ("Transportes", "Elegir cómo se comunican cliente y servidor según entorno y despliegue."),
            ("Sampling", "El servidor puede solicitar generación al modelo bajo control del cliente."),
            ("Notificaciones", "Permiten informar cambios o progreso sin esperar una llamada directa."),
            ("Producción", "Hay que diseñar seguridad, permisos, errores y observabilidad desde el inicio."),
        ],
    },
    "introduction-to-agent-skills": {
        "nivel": "Técnico",
        "color": "#7A5A9A",
        "para_que": "Crear skills reutilizables para que Claude aplique instrucciones especializadas cuando correspondan.",
        "skills": ["AI Agents", "Claude Code", "Workflow Automation", "Technical Documentation"],
        "cards": [
            ("Skill", "Paquete de instrucciones reutilizables para una tarea o dominio concreto."),
            ("Activación", "Debe estar descrita de forma clara para que Claude sepa cuándo usarla."),
            ("Contenido", "Un buen skill combina instrucciones, referencias y scripts reutilizables."),
            ("Calidad", "Debe probarse con casos reales y mantenerse como cualquier herramienta del equipo."),
        ],
    },
    "introduction-to-subagents": {
        "nivel": "Técnico",
        "color": "#556B89",
        "para_que": "Crear subagentes especializados para delegar tareas y mantener limpio el contexto principal.",
        "skills": ["AI Agents", "Agentic AI", "Claude Code", "Context Management"],
        "cards": [
            ("Especialización", "Un subagente se enfoca en una tarea concreta: revisar, investigar, depurar, etc."),
            ("Contexto limpio", "Delegar evita llenar la conversación principal de detalles secundarios."),
            ("Instrucciones", "Cada subagente necesita rol, criterios de calidad y límites claros."),
            ("Coordinación", "El agente principal integra resultados y decide próximos pasos."),
        ],
    },
    "claude-code-in-action": {
        "nivel": "Técnico",
        "color": "#27706F",
        "para_que": "Ver Claude Code aplicado a flujos reales de desarrollo, revisión y automatización.",
        "skills": ["Claude Code", "AI-Assisted Software Development", "Developer Tools"],
        "cards": [
            ("Flujo real", "No se limita a ejemplos: enseña cómo integrar Claude Code en trabajo diario."),
            ("Contexto", "El éxito depende de que Claude entienda repo, comandos, tests y convenciones."),
            ("Validación", "Cada cambio debe ejecutarse, probarse y revisarse."),
        ],
    },
    "claude-in-amazon-bedrock": {
        "nivel": "Cloud",
        "color": "#8C6239",
        "para_que": "Usar Claude dentro de AWS Bedrock para soluciones enterprise y cloud.",
        "skills": ["Amazon Bedrock", "AWS", "Claude API", "Cloud AI"],
        "cards": [
            ("Bedrock", "Capa gestionada de AWS para consumir modelos fundacionales como Claude."),
            ("Enterprise", "Importan permisos, región, costes, cuotas e integración con servicios AWS."),
            ("Casos", "Aplicaciones internas, agentes, RAG y automatización con gobierno cloud."),
        ],
    },
    "claude-with-google-vertex": {
        "nivel": "Cloud",
        "color": "#4C739E",
        "para_que": "Usar Claude desde Google Cloud Vertex AI en arquitecturas empresariales.",
        "skills": ["Vertex AI", "Google Cloud", "Claude API", "Cloud AI"],
        "cards": [
            ("Vertex AI", "Plataforma de Google Cloud para consumir y operar modelos de IA."),
            ("Integración", "Se conecta con IAM, proyectos, cuotas, logging y servicios de GCP."),
            ("Uso", "Útil si tu organización ya despliega datos y aplicaciones en Google Cloud."),
        ],
    },
}


DEFAULT_PROFILE = {
    "nivel": "General",
    "color": "#636B74",
    "para_que": "Curso de Anthropic Academy para ampliar competencias prácticas con Claude e IA generativa.",
    "skills": ["Generative AI", "Claude", "AI Literacy"],
    "cards": [
        ("Objetivo", "Identifica qué problema resuelve el curso y qué flujo de trabajo enseña."),
        ("Conceptos clave", "Convierte cada lección en una pregunta de repaso."),
        ("Aplicación", "Relaciona el contenido con una tarea real de tu trabajo o estudios."),
    ],
}


QUESTION_BANK = {
    "ai-fluency-framework-foundations": [
        ("¿Qué significa delegar bien en el marco 4D?", ["Decidir qué hace humano, IA o ambos", "Pedir una respuesta larga", "Usar siempre el modelo más caro", "Evitar revisar salidas"], 0),
        ("¿Qué competencia evalúa calidad, exactitud y supuestos?", ["Descripción", "Discernimiento", "Delegación", "Streaming"], 1),
        ("¿Qué incluye la diligencia?", ["Privacidad, transparencia y responsabilidad", "Solo escribir prompts", "Subir todos los datos", "Aceptar respuestas rápidas"], 0),
    ],
    "claude-with-the-anthropic-api": [
        ("¿La API recuerda automáticamente conversaciones previas?", ["Sí, siempre", "No, debes reenviar el historial necesario", "Solo si usas Haiku", "Solo en streaming"], 1),
        ("¿Para qué sirve un system prompt?", ["Definir comportamiento y rol", "Pagar menos tokens", "Eliminar contexto", "Crear una base de datos"], 0),
        ("¿Qué patrón reduce invenciones usando fuentes externas?", ["RAG", "CSS", "SMTP", "OCR"], 0),
    ],
    "introduction-to-model-context-protocol": [
        ("En MCP, ¿qué son las tools?", ["Acciones que el modelo puede solicitar", "Solo documentos estáticos", "Diseños CSS", "Prompts humanos"], 0),
        ("¿Qué primitiva expone datos de lectura?", ["Resources", "Tools", "Cookies", "Hooks"], 0),
        ("¿Para qué sirven los prompts MCP?", ["Flujos predefinidos invocables por el usuario", "Compilar código", "Autenticar OAuth siempre", "Crear imágenes"], 0),
    ],
    "introduction-to-claude-cowork": [
        ("¿Qué diferencia a Cowork del chat normal?", ["Puede sostener trabajo multi-paso con archivos/proyectos", "Solo responde más corto", "No usa contexto", "Es solo para programar"], 0),
        ("¿Qué acciones conviene supervisar especialmente?", ["Enviar, borrar, compartir o publicar", "Leer texto público", "Ordenar ideas", "Resumir un borrador"], 0),
    ],
    "claude-code-101": [
        ("¿Cuál es un buen primer paso antes de editar código con Claude Code?", ["Explorar el repo y patrones", "Borrar archivos", "Ignorar tests", "Hacer commit directo"], 0),
        ("¿Qué aporta Plan Mode?", ["Revisar enfoque antes de implementar", "Ocultar cambios", "Aumentar temperatura", "Evitar lectura de archivos"], 0),
    ],
}


def profile_for(course):
    key = slug(course.get("path", course.get("title", "")))
    return COURSE_PROFILES.get(key, DEFAULT_PROFILE)


DISPLAY_TITLES = {
    "/claude-101": "Claude 101",
    "/introduction-to-agent-skills": "Introduction to agent skills",
    "/introduction-to-subagents": "Introduction to subagents",
}


def display_title(course):
    return DISPLAY_TITLES.get(course.get("path"), course.get("title", "Curso"))


def guide_path_for(course):
    guide = course.get("guideFile")
    if not guide:
        return None
    path = DATA_DIR / guide
    return path if path.exists() else None


def extract_headings_from_guide(path: Path, limit=8):
    if not path or not path.exists():
        return []
    text = clean_text(path.read_text(encoding="utf-8", errors="ignore"))
    headings = re.findall(r"^###\s+(.+)$", text, flags=re.MULTILINE)
    return headings[:limit]


def make_questions(course, profile):
    key = slug(course.get("path", course.get("title", "")))
    questions = list(QUESTION_BANK.get(key, []))
    for title, body in profile["cards"][:4]:
        questions.append(
            (
                f"¿Qué idea resume mejor «{title}»?",
                [
                    body,
                    "Una opción decorativa sin impacto en el uso de IA",
                    "Una regla para omitir la revisión humana",
                    "Un formato de certificado de LinkedIn",
                ],
                0,
            )
        )
    random.Random(7).shuffle(questions)
    return questions


def course_key(course):
    return slug(course.get("path", course.get("title", "")))


def course_progress(course):
    key = course_key(course)
    done = st.session_state.get("completed_courses", set())
    return 100 if key in done else 0


def set_course_done(course, value: bool):
    done = set(st.session_state.get("completed_courses", set()))
    key = course_key(course)
    if value:
        done.add(key)
    else:
        done.discard(key)
    st.session_state.completed_courses = done


def coverage_label(course):
    if course.get("llmContentFile"):
        return "Guía amplia"
    if course.get("lessons"):
        return "Temario visible"
    return "Ficha breve"


def render_card(title, body, accent="#636B74", meta=None):
    meta_html = f"<div class='card-meta'>{meta}</div>" if meta else ""
    st.markdown(
        f"""
<div class="dashcard rich-card" style="--accent:{accent}">
  <div class="card-kicker"></div>
  <div class="card-title">{title}</div>
  <div class="card-body">{body}</div>
  {meta_html}
</div>
""",
        unsafe_allow_html=True,
    )


def render_progress_bar(value, accent="#6B7A45"):
    st.markdown(
        f"""
<div class="progress-shell" aria-label="Progreso {value}%">
  <div class="progress-fill" style="width:{max(0, min(100, value))}%; background:{accent};"></div>
</div>
""",
        unsafe_allow_html=True,
    )


def badge(text, color="#636B74"):
    st.markdown(
        f"<span class='badge' style='border-color:{color}33;background:{color}14;color:{color}'>{text}</span>",
        unsafe_allow_html=True,
    )


courses = load_courses()
if not courses:
    st.error("No encuentro los datos scrapeados. Ejecuta primero el scraper de Anthropic Academy.")
    st.stop()


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Inter:wght@400;500;600;700;800&display=swap');
:root{ --cyan:#22d3ee; --blue:#38bdf8; --gold:#f5b85a; --text:#edf7ff; --soft:#cfe2f7; --muted:#758da8; --line:rgba(196,225,255,.14); --line-strong:rgba(34,211,238,.34); --panel:rgba(255,255,255,.045); --serif:'Fraunces',Georgia,serif; --sans:'Inter',system-ui,sans-serif; --glow:0 0 22px rgba(34,211,238,.35); }
.stApp{ background:linear-gradient(150deg,#07111f 0%,#0b1628 48%,#10243c 100%); background-attachment:fixed; color:var(--text); font-family:var(--sans); }
[data-testid="stSidebar"]{ background:rgba(7,17,31,.92); border-right:1px solid var(--line); }
[data-testid="stSidebar"] *{ color:var(--soft); }
h1,h2,h3{ font-family:var(--serif)!important; font-weight:450!important; letter-spacing:-.02em!important; color:#fff!important; }
p,span,label,li,.stMarkdown{ color:var(--text); }
.app-title{ font-family:var(--serif); font-size:34px; line-height:1.05; font-weight:500; color:#fff; margin:8px 0 4px; }
.subtle{ color:var(--soft); font-size:15px; }
.dashgrid{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin:14px 0 18px; }
.metric-card,.dashcard,.test-card,.course-row,.study-step{ background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02)),var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; }
.hero-panel{ position:relative; overflow:hidden; padding:26px; margin:12px 0 20px; border-radius:16px; background:linear-gradient(135deg,rgba(34,211,238,.12),rgba(56,130,246,.06)),var(--panel); border:1px solid var(--line-strong); }
.hero-panel:after{ content:""; position:absolute; right:18px; top:18px; width:170px; height:170px; border:1px solid rgba(34,211,238,.25); border-radius:50%; box-shadow:0 0 70px rgba(34,211,238,.18) inset; }
.metric-k{ color:var(--muted); font-size:11px; text-transform:uppercase; font-weight:800; letter-spacing:.06em; }
.metric-v{ font-family:var(--serif); font-size:32px; font-weight:500; margin-top:4px; color:#fff; }
.card-title{ font-size:16px; font-weight:700; margin-bottom:8px; color:#fff; }
.card-body{ color:var(--soft); font-size:14px; line-height:1.55; }
.card-meta{ color:var(--muted); font-size:12px; margin-top:12px; }
.rich-card{ min-height:150px; transition:transform .18s,box-shadow .18s,border-color .18s; }
.rich-card:hover{ transform:translateY(-3px); border-color:var(--line-strong); box-shadow:0 18px 44px rgba(2,8,20,.5),var(--glow); }
.card-kicker{ width:34px; height:4px; background:linear-gradient(90deg,var(--cyan),var(--blue)); border-radius:999px; margin-bottom:14px; box-shadow:var(--glow); }
.badge{ display:inline-flex; align-items:center; min-height:28px; padding:4px 12px; border:1px solid var(--line-strong); border-radius:999px; font-size:12px; font-weight:700; letter-spacing:.03em; margin:0 6px 6px 0; color:#bff6ff; background:rgba(34,211,238,.12); }
.course-row{ display:block; padding:14px 16px; margin-bottom:10px; }
.course-row-grid{ display:grid; grid-template-columns:1fr auto; gap:12px; align-items:center; }
.course-row strong{ display:block; margin-bottom:4px; color:#fff; }
.course-row span{ color:var(--muted); font-size:13px; }
.pill-muted{ border:1px solid var(--line); border-radius:999px; padding:5px 10px; font-size:12px; color:var(--soft); background:rgba(34,211,238,.06); white-space:nowrap; }
.progress-shell{ height:8px; border-radius:999px; background:rgba(255,255,255,.08); overflow:hidden; margin-top:10px; }
.progress-fill{ height:100%; border-radius:999px; background:linear-gradient(90deg,var(--cyan),var(--blue))!important; box-shadow:var(--glow); transition:width .25s; }
.study-strip{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:12px 0 18px; }
.step-num{ font-family:var(--serif); font-size:12px; color:var(--cyan); font-weight:700; margin-bottom:4px; }
.flashcard{ min-height:220px; display:flex; flex-direction:column; justify-content:space-between; padding:24px; border-radius:16px; background:linear-gradient(135deg,rgba(34,211,238,.10),rgba(56,130,246,.04)),var(--panel); border:1px solid var(--line-strong); }
.flash-title{ font-family:var(--serif); font-size:24px; font-weight:500; margin-bottom:10px; color:#fff; }
.flash-body{ color:var(--soft); line-height:1.6; font-size:16px; }
.tiny-note{ color:var(--muted); font-size:12px; }
.answer-good{ border-left:4px solid var(--cyan); background:rgba(34,211,238,.10); padding:12px; border-radius:8px; color:var(--text); }
.answer-bad{ border-left:4px solid var(--gold); background:rgba(245,184,90,.10); padding:12px; border-radius:8px; color:var(--text); }
.stButton>button,.stLinkButton>a{ border:1px solid var(--line-strong)!important; background:linear-gradient(135deg,var(--cyan),var(--blue))!important; color:#04121a!important; font-weight:700!important; border-radius:10px!important; box-shadow:0 12px 36px rgba(34,211,238,.22)!important; }
.stButton>button:hover,.stLinkButton>a:hover{ box-shadow:var(--glow)!important; transform:translateY(-1px); }
@media (max-width:980px){ .dashgrid{grid-template-columns:repeat(2,1fr)} .study-strip{grid-template-columns:1fr} }
@media (max-width:640px){ .dashgrid{grid-template-columns:1fr} .app-title{font-size:28px} .course-row-grid{grid-template-columns:1fr} }
</style>
""",
    unsafe_allow_html=True,
)


st.sidebar.markdown("## Estudia")
st.sidebar.caption("Anthropic Academy")
mode = st.sidebar.radio(
    "Vista",
    ["Dashboard", "Curso", "Flashcards", "Test", "Ruta de estudio", "Contenido scrapeado"],
    label_visibility="collapsed",
)

course_options = {display_title(c): c for c in courses}
selected_title = st.sidebar.selectbox("Curso", list(course_options.keys()), index=0)
selected = course_options[selected_title]
selected_profile = profile_for(selected)
level_filter = st.sidebar.multiselect(
    "Filtrar niveles en dashboard",
    sorted({profile_for(c)["nivel"] for c in courses}),
    default=[],
)

st.sidebar.divider()
st.sidebar.caption("Todo el contenido didáctico de la app está en castellano. Los HTML originales se conservan como fuente.")


total_courses = len(courses)
full_count = sum(1 for c in courses if c.get("llmContentFile"))
lesson_count = sum(len(c.get("lessons", [])) for c in courses)
blocked_count = sum(
    sum(1 for l in c.get("lessonContents", []) if l.get("status") == "blocked")
    for c in courses
)


if mode == "Dashboard":
    st.markdown(
        """
<div class="hero-panel">
  <div class="app-title">Estudia Anthropic</div>
  <div class="subtle">Dashboard de certificaciones, repaso guiado, flashcards y baterías de test en castellano.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="dashgrid">
  <div class="metric-card"><div class="metric-k">Cursos</div><div class="metric-v">{total_courses}</div></div>
  <div class="metric-card"><div class="metric-k">Con contenido extenso</div><div class="metric-v">{full_count}</div></div>
  <div class="metric-card"><div class="metric-k">Lecciones visibles</div><div class="metric-v">{lesson_count}</div></div>
  <div class="metric-card"><div class="metric-k">Lecciones bloqueadas</div><div class="metric-v">{blocked_count}</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("Plan de hoy")
    st.markdown(
        """
<div class="study-strip">
  <div class="study-step"><div class="step-num">01 · 12 min</div><strong>Repasa tarjetas</strong><br><span class="subtle">Lee 4 dashcards del curso prioritario.</span></div>
  <div class="study-step"><div class="step-num">02 · 10 min</div><strong>Haz un test corto</strong><br><span class="subtle">Comprueba al menos 5 preguntas.</span></div>
  <div class="study-step"><div class="step-num">03 · 5 min</div><strong>Marca avance</strong><br><span class="subtle">Anota qué curso queda listo para LinkedIn.</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("Cursos recomendados")
    preferred = [
        "AI Fluency: Framework & Foundations",
        "Claude 101",
        "AI Capabilities and Limitations",
        "Introduction to Claude Cowork",
        "Claude Code 101",
        "Claude Platform 101",
        "Building with the Claude API",
        "Introduction to Model Context Protocol",
    ]
    cols = st.columns(2)
    for i, title in enumerate(preferred):
        course = next((c for c in courses if c["title"] == title or title in c["title"]), None)
        if not course:
            continue
        if level_filter and profile_for(course)["nivel"] not in level_filter:
            continue
        prof = profile_for(course)
        with cols[i % 2]:
            pct = course_progress(course)
            st.markdown(
                f"""
<div class='course-row'>
  <div class='course-row-grid'>
    <div><strong>{display_title(course)}</strong><span>{prof['para_que']}</span></div>
    <div class='pill-muted'>{coverage_label(course)}</div>
  </div>
  <div class='tiny-note'>Progreso local: {pct}%</div>
  <div class='progress-shell'><div class='progress-fill' style='width:{pct}%; background:{prof["color"]};'></div></div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.subheader("Mapa de niveles")
    levels = {}
    for c in courses:
        levels.setdefault(profile_for(c)["nivel"], 0)
        levels[profile_for(c)["nivel"]] += 1
    for level, count in levels.items():
        badge(f"{level}: {count} cursos")


elif mode == "Curso":
    prof = selected_profile
    st.markdown(f"<div class='app-title'>{display_title(selected)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtle'>{prof['para_que']}</div>", unsafe_allow_html=True)

    cert_url = f"https://anthropic.skilljar.com{selected.get('path','')}"
    st.link_button("🎓 Ir al curso oficial y sacar el certificado", cert_url)

    st.write("")
    top_cols = st.columns([2, 1])
    with top_cols[0]:
        for sk in prof["skills"]:
            badge(sk, prof["color"])
    with top_cols[1]:
        done = st.checkbox("Marcar como dominado", value=course_progress(selected) == 100)
        set_course_done(selected, done)
        render_progress_bar(course_progress(selected), prof["color"])

    cols = st.columns(min(4, max(1, len(prof["cards"]))))
    for i, (title, body) in enumerate(prof["cards"]):
        with cols[i % len(cols)]:
            render_card(title, body, prof["color"], meta=f"Concepto {i + 1}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Lecciones visibles", len(selected.get("lessons", [])))
    c2.metric("Contenido extenso", "Sí" if selected.get("llmContentFile") else "No")
    c3.metric("PDFs", len(selected.get("pdfs", [])))

    guide = guide_path_for(selected)
    headings = extract_headings_from_guide(guide)
    if headings:
        st.subheader("Conceptos detectados en la guía")
        hcols = st.columns(2)
        for i, h in enumerate(headings):
            with hcols[i % 2]:
                st.markdown(f"<div class='course-row'><strong>{h}</strong><span>Convierte este título en una pregunta de examen.</span></div>", unsafe_allow_html=True)

    with st.expander("Ver guía de estudio completa"):
        if guide:
            st.markdown(clean_text(guide.read_text(encoding="utf-8", errors="ignore")))
        else:
            st.info("No hay guía generada para este curso.")


elif mode == "Flashcards":
    prof = selected_profile
    st.markdown(f"<div class='app-title'>Flashcards: {display_title(selected)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Tarjetas rápidas para memorizar conceptos. Cambia de tarjeta desde el control inferior.</div>", unsafe_allow_html=True)
    cards = list(prof["cards"])
    guide = guide_path_for(selected)
    for heading in extract_headings_from_guide(guide, limit=6):
        cards.append((heading, "Idea detectada en la guía. Ábrela en la vista Curso para leer el contexto completo."))
    idx = st.slider("Tarjeta", 1, max(1, len(cards)), 1) - 1
    title, body = cards[idx]
    st.markdown(
        f"""
<div class="flashcard" style="border-color:{prof['color']}55">
  <div>
    <div class="tiny-note">Tarjeta {idx + 1} de {len(cards)} · {prof['nivel']}</div>
    <div class="flash-title">{title}</div>
    <div class="flash-body">{body}</div>
  </div>
  <div class="tiny-note">Pregunta mental: ¿podrías explicarlo con un ejemplo real?</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("Barajar siguiente"):
        st.rerun()


elif mode == "Test":
    prof = selected_profile
    questions = make_questions(selected, prof)
    st.markdown(f"<div class='app-title'>Test: {display_title(selected)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Batería corta para repasar conceptos clave. Las preguntas y explicaciones están en castellano.</div>", unsafe_allow_html=True)
    quiz_len = st.segmented_control("Modo", ["Rápido", "Simulacro"], default="Rápido")
    limit = 5 if quiz_len == "Rápido" else 10

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    score = 0
    answered = 0
    for i, (question, options, correct) in enumerate(questions[:limit], start=1):
        st.markdown(f"### {i}. {question}")
        choice = st.radio("Selecciona una respuesta", options, key=f"{selected['path']}-{i}", label_visibility="collapsed")
        if st.button("Comprobar", key=f"check-{selected['path']}-{i}"):
            st.session_state.answers[f"{selected['path']}-{i}"] = choice == options[correct]
        result = st.session_state.answers.get(f"{selected['path']}-{i}")
        if result is not None:
            answered += 1
            if result:
                score += 1
                st.markdown("<div class='answer-good'>Correcto. Quédate con esta idea para el examen.</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div class='answer-bad'>No exactamente. Respuesta correcta: <strong>{options[correct]}</strong></div>",
                    unsafe_allow_html=True,
                )
    st.divider()
    st.metric("Puntuación comprobada", f"{score}/{answered}" if answered else "0/0")


elif mode == "Ruta de estudio":
    st.markdown("<div class='app-title'>Ruta recomendada</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Orden pensado para LinkedIn, utilidad profesional y progresión técnica.</div>", unsafe_allow_html=True)
    route = [
        ("AI Fluency: Framework & Foundations", "Base conceptual"),
        ("Claude 101", "Uso diario de Claude"),
        ("AI Capabilities and Limitations", "Criterio sobre límites de IA"),
        ("Introduction to Claude Cowork", "Productividad con archivos y tareas reales"),
        ("Claude Code 101", "Desarrollo asistido por IA"),
        ("Introduction to agent skills", "Skills reutilizables"),
        ("Introduction to subagents", "Subagentes y gestión de contexto"),
        ("Claude Platform 101", "Arquitectura de plataforma"),
        ("Building with the Claude API", "API, tools, RAG y agentes"),
        ("Introduction to Model Context Protocol", "Conectores MCP"),
        ("Model Context Protocol: Advanced Topics", "MCP avanzado"),
        ("Claude with Amazon Bedrock / Vertex AI", "Cloud enterprise"),
    ]
    for idx, (title, why) in enumerate(route, start=1):
        found = next((c for c in courses if title in display_title(c) or display_title(c) in title), None)
        prof = profile_for(found) if found else DEFAULT_PROFILE
        st.markdown(
            f"<div class='course-row'><div class='course-row-grid'><div><strong>{idx}. {title}</strong><span>{why}</span></div><div class='pill-muted'>{prof['nivel']}</div></div></div>",
            unsafe_allow_html=True,
        )


else:
    st.markdown("<div class='app-title'>Contenido scrapeado</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Acceso rápido a archivos locales generados durante el scrape.</div>", unsafe_allow_html=True)
    st.write(f"Carpeta base: `{DATA_DIR}`")
    st.write(f"Índice de guías: `{DATA_DIR / 'GUIAS_ESTUDIO_INDEX.md'}`")
    st.write(f"JSON de cursos: `{DATA_DIR / 'courses_enriched.json'}`")

    st.subheader("Archivos del curso seleccionado")
    st.json(
        {
            "guia": str(guide_path_for(selected) or ""),
            "html": selected.get("rawHtmlFile"),
            "contenido_extenso": selected.get("llmContentFile"),
            "lecciones": len(selected.get("lessonContents", [])),
        }
    )
