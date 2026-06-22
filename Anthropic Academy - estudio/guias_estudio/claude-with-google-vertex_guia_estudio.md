## Resumen

**"Claude with Google Cloud's Vertex AI"** es una certificación de Anthropic Academy orientada a desarrolladores, arquitectos de soluciones e ingenieros de plataforma que quieren desplegar los modelos Claude en producción usando la infraestructura gestionada de Google Cloud. La idea central es sencilla pero potente: en lugar de llamar a la API directa de Anthropic (`api.anthropic.com`), invocas exactamente los mismos modelos Claude pero servidos a través de **Vertex AI**, el servicio de IA gestionada de Google Cloud Platform (GCP).

¿Para quién es? Para equipos que ya viven en Google Cloud y necesitan que sus cargas de IA cumplan los mismos requisitos de gobernanza, facturación, residencia de datos (regionalización), IAM y seguridad que el resto de su infraestructura GCP. La certificación valida que sabes autenticarte con credenciales de Google, seleccionar modelos por su identificador de Vertex, hacer peticiones con los SDK adecuados, gestionar regiones y cuotas, y aplicar buenas prácticas de prompting y producción.

Lo que NO cambia entre Vertex y la API directa: las capacidades del modelo (razonamiento, visión, tool use, ventana de contexto), el formato de mensajes (`messages`, roles `user`/`assistant`, bloques `system`), y las técnicas de prompt engineering. Lo que SÍ cambia: la autenticación, los identificadores de modelo, los endpoints, la gestión de cuotas/regiones y la capa de facturación y cumplimiento.

## Conceptos clave

- **Vertex AI Model Garden**: el catálogo de Google Cloud donde Claude aparece como un "modelo de socio" (partner/MaaS, *Model-as-a-Service*). Antes de usar Claude debes habilitarlo/suscribirte en Model Garden dentro de tu proyecto GCP.
- **Modelo como servicio (MaaS)**: Claude se consume como endpoint gestionado y pago por uso; no despliegas pesos ni gestionas GPUs. Google factura el consumo a través de tu cuenta de facturación de GCP.
- **Identificador de modelo en Vertex**: en Vertex los modelos usan el nombre tipo `claude-sonnet-4-5@<fecha>` o `claude-opus-4-1@<fecha>` (con `@` y versión/fecha), distinto de la API directa que usa `claude-sonnet-4-5-YYYYMMDD`. Hay que conocer el formato y los alias.
- **Autenticación con Google (IAM + ADC)**: en vez de una `x-api-key` de Anthropic, te autenticas con credenciales de Google Cloud: *Application Default Credentials* (ADC), service accounts y tokens OAuth2 de corta duración. Los permisos se controlan con roles IAM (p. ej. `roles/aiplatform.user`).
- **`AnthropicVertex` SDK**: el SDK oficial de Anthropic incluye un cliente específico (`AnthropicVertex` en Python, `AnthropicVertex` en TypeScript) que envuelve la autenticación de Google y te deja usar la misma interfaz `messages.create(...)` de siempre.
- **Project ID y región**: cada petición va ligada a un `project_id` de GCP y a una `region` (location), por ejemplo `us-east5` o `europe-west1`. La disponibilidad de cada modelo Claude varía por región.
- **Endpoint regional vs global**: Vertex permite endpoints regionales (datos y cómputo en una región concreta, útil para residencia de datos) y, según el modelo, un endpoint global que mejora disponibilidad y throughput a costa de no fijar región.
- **Cuotas y QPM/tokens por minuto**: Google gestiona la capacidad con cuotas (peticiones por minuto, tokens por minuto) por proyecto y región. Para producción se usa **Provisioned Throughput** (capacidad reservada) frente al modo bajo demanda.
- **`anthropic_version`**: al llamar por Vertex hay que indicar el parámetro/versión de la API de Anthropic (p. ej. `vertex-2023-10-16`) en el cuerpo de la petición; el SDK lo gestiona por ti.
- **Paridad de features**: tool use (function calling), visión (imágenes), *streaming* (SSE), *prompt caching* y *batch* están disponibles en Vertex, aunque ciertas features beta pueden tardar más en llegar que en la API directa.
- **Facturación y cumplimiento GCP**: el consumo aparece en tu factura de Google Cloud; aplican los acuerdos de procesamiento de datos de Google, VPC Service Controls, CMEK y los controles de seguridad de tu organización GCP.
- **Las tres vías de despliegue de Claude**: API directa de Anthropic, **Amazon Bedrock** y **Google Vertex AI**. La certificación se centra en la tercera, pero conviene saber diferenciarlas.

## Que necesitas dominar para el certificado

1. **Diferencias de autenticación**: explicar por qué en Vertex no usas API key de Anthropic sino credenciales de Google (ADC, service accounts, tokens OAuth de corta vida) y qué rol IAM mínimo se necesita (`roles/aiplatform.user`).
2. **Convención de nombres de modelo en Vertex**: reconocer el formato `claude-<familia>-<version>@<fecha>` y saber que difiere de la API directa.
3. **Configurar una petición**: saber qué tres datos son obligatorios además del prompt — `project_id`, `region`/location y modelo — y cómo el SDK `AnthropicVertex` los recibe.
4. **Habilitar el modelo en Model Garden**: entender que hay que activar/suscribir Claude en Model Garden y habilitar la *Vertex AI API* antes de poder invocarlo.
5. **Regiones y disponibilidad**: saber que no todos los modelos están en todas las regiones y cómo elegir región por latencia, residencia de datos y disponibilidad.
6. **Cuotas y escalado**: distinguir modo bajo demanda vs **Provisioned Throughput**, y cómo se solicitan aumentos de cuota.
7. **Paridad de la API de Messages**: confirmar que el formato de mensajes, roles, system prompt, *streaming*, tool use y visión son los mismos; solo cambia la capa de transporte/auth.
8. **Prompt engineering portable**: aplicar las mismas técnicas (instrucciones claras, *system prompt*, ejemplos *few-shot*, XML tags, *chain of thought*, prefill del turno del asistente) porque el modelo es idéntico.
9. **Seguridad y gobernanza GCP**: VPC Service Controls, CMEK, logging/auditoría con Cloud Logging, y residencia de datos vía endpoints regionales.
10. **Cuándo elegir Vertex**: justificar la elección frente a la API directa o Bedrock según el stack del cliente.

## Plan de estudio

1. **Repasa la API de Messages de Claude** (1-2 h): roles, `system`, `max_tokens`, `temperature`, *streaming*, tool use y visión. Si dominas esto, el 70% se traslada igual a Vertex.
2. **Monta un proyecto GCP de pruebas** (1 h): crea/usa un proyecto, habilita la *Vertex AI API*, configura facturación y ejecuta `gcloud auth application-default login` para tener ADC.
3. **Habilita Claude en Model Garden** (30 min): localiza Claude en Model Garden, acepta términos/suscribe el modelo y anota el identificador exacto y las regiones disponibles.
4. **Primera llamada con `AnthropicVertex`** (1 h): instala el SDK (`pip install "anthropic[vertex]"`), instancia `AnthropicVertex(project_id=..., region=...)` y haz un `messages.create`. Compara el código con la versión de API directa para ver qué cambia y qué no.
5. **Prueba features avanzadas** (2 h): *streaming*, tool use (function calling) y visión sobre Vertex; confirma que el contrato es idéntico.
6. **Estudia auth a fondo** (1-2 h): ADC vs service account JSON vs Workload Identity; roles IAM; tokens de corta vida. Es la zona donde más caen las preguntas.
7. **Regiones, cuotas y throughput** (1 h): mapea qué modelos hay por región, lee sobre cuotas QPM/TPM y Provisioned Throughput.
8. **Gobernanza y comparativa de plataformas** (1 h): VPC-SC, CMEK, logging; tabla mental Anthropic-directo vs Bedrock vs Vertex.
9. **Autoevaluación**: haz las flashcards y el quiz de esta guía; repite lo que falles antes de presentarte.

## Errores comunes y tips

- **Confundir los identificadores de modelo**: en Vertex es `claude-sonnet-4-5@fecha` con `@`; en la API directa es `claude-sonnet-4-5-YYYYMMDD`. No son intercambiables.
- **Buscar la `x-api-key`**: en Vertex NO existe; la autenticación es 100% Google. Si una pregunta sugiere usar la API key de Anthropic en Vertex, es trampa.
- **Olvidar `project_id` o `region`**: son obligatorios; un error frecuente es no fijar la región o usar una donde ese modelo no está disponible.
- **No habilitar el modelo en Model Garden**: aunque tengas permisos, si no has suscrito/activado Claude la llamada falla.
- **Asumir paridad total instantánea de betas**: las capacidades GA están en Vertex, pero alguna feature beta muy reciente puede llegar antes a la API directa.
- **Tip de coste**: para tráfico predecible y alto, evalúa Provisioned Throughput; para tráfico irregular, bajo demanda. El *prompt caching* y el *batch* reducen coste también en Vertex.
- **Tip de residencia de datos**: si el cliente exige que los datos no salgan de una región, usa endpoint regional, no global.
- **Tip de portabilidad**: escribe tus prompts y tu lógica de tool use de forma agnóstica; cambiar de API directa a Vertex debería ser cambiar el cliente y el nombre del modelo, poco más.

## Puntos clave para recordar

- Claude en Vertex = mismos modelos, distinta puerta de entrada (auth Google + endpoints GCP).
- Autenticación: ADC / service accounts / OAuth2 + rol IAM `roles/aiplatform.user`; nunca API key de Anthropic.
- Identificador con `@` y fecha (`claude-opus-4-1@...`), distinto de la API directa.
- Toda petición necesita: modelo, `project_id` y `region`/location.
- Hay que habilitar la Vertex AI API y suscribir Claude en Model Garden.
- La API de Messages (roles, system, streaming, tool use, visión) es idéntica; el prompt engineering es portable.
- Disponibilidad por región varía; elige región por latencia, residencia de datos y disponibilidad.
- Escalado: bajo demanda vs Provisioned Throughput; capacidad regida por cuotas QPM/TPM.
- Gobernanza GCP: VPC Service Controls, CMEK, Cloud Logging, facturación unificada de Google Cloud.
- Las tres vías de Claude: API directa, Amazon Bedrock y Google Vertex AI.