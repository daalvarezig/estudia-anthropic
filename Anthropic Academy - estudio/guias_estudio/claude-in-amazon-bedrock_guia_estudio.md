## Resumen

**Claude with Amazon Bedrock** es la ruta para usar los modelos Claude de Anthropic dentro de **Amazon Bedrock**, el servicio gestionado de AWS para acceder a modelos fundacionales (FMs) mediante una API unificada. En lugar de llamar a la API directa de Anthropic, llamas a Claude a través de la infraestructura de AWS, heredando su gobernanza: IAM, VPC, CloudWatch, CloudTrail, KMS y facturación consolidada en tu cuenta de AWS.

Esta guía prepara la certificación oficial de Anthropic Academy **"Claude with Amazon Bedrock"**. Está pensada para **desarrolladores, arquitectos de soluciones y equipos de plataforma** que ya construyen (o quieren construir) sobre AWS y necesitan integrar Claude de forma segura, escalable y conforme a normativa. No es un curso de ML desde cero: asume que sabes llamar a una API y entiendes conceptos básicos de cloud.

El examen mide si sabes **por qué** elegir Bedrock frente a la API directa, **cómo** se autentica y se invoca Claude (incluida la **Messages API** y el **Converse API**), cómo se gestionan **modelos, regiones e inferencia entre regiones (cross-region inference)**, y cómo aprovechar capacidades de Bedrock como **Knowledge Bases, Agents, Guardrails** y la observabilidad nativa de AWS.

## Conceptos clave

- **Amazon Bedrock**: servicio serverless de AWS que ofrece modelos fundacionales de varios proveedores (Anthropic, Meta, Amazon, Mistral, Cohere, etc.) tras una API común. No gestionas servidores ni GPUs; pagas por uso (tokens) o por throughput provisionado.
- **Claude en Bedrock**: los modelos de Anthropic (familias Claude Opus, Sonnet y Haiku) disponibles como FMs en Bedrock. Mismo "cerebro" que la API directa, pero con plano de control de AWS.
- **Model ID y model access**: cada modelo tiene un identificador (p. ej. `anthropic.claude-3-5-sonnet-20240620-v1:0`). Antes de invocarlo debes **solicitar acceso** al modelo en la consola de Bedrock ("Model access"); el acceso se concede por región.
- **Messages API (InvokeModel / InvokeModelWithResponseStream)**: el formato nativo de Anthropic en Bedrock. Envías un cuerpo JSON con `anthropic_version`, `max_tokens`, `messages` (roles `user`/`assistant`) y opcionalmente `system`. Es el modo de máxima fidelidad a las capacidades de Claude.
- **Converse API (Converse / ConverseStream)**: API unificada de Bedrock que abstrae las diferencias entre modelos. Usas el mismo esquema de `messages` y `inferenceConfig` para cualquier FM, lo que facilita cambiar de modelo. Soporta **tool use** y mensajes multimodales de forma estandarizada.
- **Streaming**: respuestas token a token vía `InvokeModelWithResponseStream` o `ConverseStream`, mejorando la latencia percibida.
- **Tool use / function calling**: Claude puede pedir invocar herramientas que defines (con `name`, `description`, `input_schema`). Tú ejecutas la herramienta y devuelves el resultado en un mensaje `tool_result`. Disponible tanto en Messages API como en Converse.
- **Visión / multimodal**: los modelos Claude 3 en adelante aceptan imágenes en el mensaje (base64 o, en Converse, bytes), útil para análisis de documentos, capturas, etc.
- **System prompt y parámetros de inferencia**: `system` para instrucciones de rol/comportamiento; `temperature`, `top_p`, `top_k`, `max_tokens` y `stop_sequences` para controlar la generación.
- **Cross-region inference (perfiles de inferencia)**: enrutan automáticamente la petición a varias regiones para mejorar disponibilidad y throughput. Se usan **inference profile IDs** con prefijo geográfico (p. ej. `us.anthropic.claude-...`, `eu.anthropic.claude-...`).
- **On-demand vs Provisioned Throughput**: on-demand paga por token sin compromiso; Provisioned Throughput reserva capacidad (model units) para cargas altas y latencia predecible, normalmente con compromiso temporal.
- **Knowledge Bases (RAG gestionado)**: Bedrock indexa tus datos (S3 + base vectorial) y permite **Retrieve** y **RetrieveAndGenerate** para grounding con citaciones, sin montar tu propio pipeline RAG.
- **Bedrock Agents**: orquestación gestionada que combina un FM con instrucciones, grupos de acciones (Lambda/API), Knowledge Bases y razonamiento multi-paso.
- **Guardrails**: políticas de seguridad configurables (temas vetados, filtros de contenido, PII, fundamentación/contextual grounding) aplicables a entrada y salida, independientes del modelo.
- **Seguridad y gobernanza AWS**: autenticación por **IAM** (no API keys de Anthropic), aislamiento de red por **VPC endpoints (PrivateLink)**, cifrado con **KMS**, auditoría con **CloudTrail**, métricas con **CloudWatch**. Los datos no se usan para entrenar modelos.
- **SDKs**: se usa el SDK de AWS (**boto3** para Python, AWS SDK para JS, etc.) con el cliente `bedrock-runtime` para invocar y `bedrock` para el plano de control. También existe el **Anthropic SDK** con soporte Bedrock (`AnthropicBedrock`).

## Que necesitas dominar para el certificado

- **Diferenciar Bedrock vs API directa de Anthropic**: cuándo conviene cada uno (gobernanza, residencia de datos, facturación AWS, integración con servicios AWS vs. acceso a las últimas features primero).
- **Autenticación**: IAM roles/políticas y credenciales de AWS; entender que NO se usan claves de API de Anthropic.
- **Invocación**: saber construir una petición con la **Messages API** (campos obligatorios: `anthropic_version`, `max_tokens`, `messages`) y con la **Converse API**, y cuándo usar cada una.
- **Streaming** y manejo de eventos de respuesta.
- **Tool use** end-to-end: definir la herramienta, recibir la petición de uso del modelo, devolver `tool_result`.
- **Multimodal**: enviar imágenes correctamente.
- **Model IDs, model access y regiones**: cómo habilitar modelos y por qué la disponibilidad varía por región.
- **Cross-region inference profiles**: qué resuelven y cómo se nombran.
- **On-demand vs Provisioned Throughput**: criterios de elección y cuotas/throttling.
- **Capacidades de plataforma**: para qué sirven Knowledge Bases, Agents y Guardrails y cuándo usarlos.
- **Buenas prácticas de prompting de Claude**: system prompts, estructura con XML, ser explícito, few-shot, y el ajuste de parámetros de inferencia.
- **Observabilidad, coste y privacidad**: CloudWatch/CloudTrail, control de tokens y la garantía de no-entrenamiento con tus datos.

## Plan de estudio

1. **Fundamentos de Bedrock (1-2 h)**: lee qué es Bedrock, su modelo serverless, el catálogo de FMs y la diferencia entre el plano de control (`bedrock`) y el de ejecución (`bedrock-runtime`).
2. **Acceso a modelos (30 min)**: en la consola de Bedrock activa "Model access" para los modelos Claude en tu región y anota los **model IDs** exactos.
3. **Primera invocación (1-2 h)**: con **boto3**, haz una llamada `invoke_model` con la Messages API. Repite con `converse`. Compara los cuerpos de petición/respuesta.
4. **Streaming (30 min)**: implementa `invoke_model_with_response_stream` y `converse_stream`; procesa los eventos.
5. **Tool use (1-2 h)**: define una herramienta sencilla (p. ej. una calculadora o consulta de tiempo), maneja el ciclo completo de `tool_use` → `tool_result`.
6. **Multimodal (30 min)**: envía una imagen y pide a Claude que la describa o extraiga datos.
7. **Regiones e inferencia (1 h)**: prueba un **inference profile** cross-region; lee sobre on-demand vs Provisioned Throughput y sobre cuotas/throttling.
8. **Capacidades de plataforma (2 h)**: monta una **Knowledge Base** mínima (datos en S3) y prueba `RetrieveAndGenerate`; revisa conceptualmente **Agents** y configura un **Guardrail** básico.
9. **Seguridad y gobernanza (1 h)**: repasa políticas IAM mínimas, VPC endpoints, KMS, CloudTrail/CloudWatch y la política de privacidad de datos.
10. **Repaso (1 h)**: estudia las flashcards, haz el quiz, y vuelve a cualquier concepto fallado. Memoriza los campos obligatorios de la Messages API y las diferencias Messages vs Converse.

## Errores comunes y tips

- **Confundir autenticación**: en Bedrock te autenticas con **IAM**, no con la API key de Anthropic. Una pregunta clásica.
- **Olvidar habilitar "Model access"**: sin solicitar acceso al modelo en esa región, la invocación falla aunque el código sea correcto.
- **Omitir campos obligatorios de la Messages API**: `anthropic_version` y `max_tokens` son obligatorios; `max_tokens` siempre debe ir.
- **Asumir que todos los modelos están en todas las regiones**: la disponibilidad varía; por eso existen los **cross-region inference profiles** (`us.`, `eu.`, `apac.`...).
- **Mezclar Messages y Converse**: tienen esquemas distintos. Converse abstrae entre modelos (ideal para portabilidad); Messages da fidelidad total a las features de Claude.
- **Creer que Bedrock entrena con tus datos**: no lo hace. Tus prompts y salidas no se usan para entrenar los modelos.
- **Ignorar throttling/cuotas**: on-demand tiene límites por defecto; para tráfico alto o latencia estable usa Provisioned Throughput o cross-region.
- **Reinventar RAG**: si necesitas grounding sobre datos propios, **Knowledge Bases** te ahorra el pipeline y aporta citaciones.
- **Guardrails al revés**: los Guardrails son independientes del modelo y se aplican a entrada y salida; no son un prompt, son una política gestionada.
- **Tip de coste**: el coste se mide en tokens de entrada y salida; el system prompt cuenta como entrada. Mide con CloudWatch.

## Puntos clave para recordar

- Bedrock = acceso gestionado y seguro a Claude bajo gobernanza AWS (IAM, VPC, KMS, CloudTrail, CloudWatch).
- Autenticación por IAM, NO por API key de Anthropic; facturación en tu cuenta AWS.
- Debes solicitar **Model access** por región antes de invocar; cada modelo tiene un **model ID** concreto.
- Dos formas de invocar: **Messages API** (nativa de Anthropic, máxima fidelidad) y **Converse API** (unificada y portable entre FMs).
- Campos obligatorios de la Messages API: `anthropic_version`, `max_tokens`, `messages`.
- Streaming con `InvokeModelWithResponseStream` o `ConverseStream`.
- Tool use y multimodal (imágenes) soportados en ambas APIs.
- **Cross-region inference profiles** (`us.`, `eu.`...) mejoran disponibilidad/throughput.
- **On-demand** (pago por token) vs **Provisioned Throughput** (capacidad reservada) según carga.
- Plataforma: **Knowledge Bases** (RAG gestionado con citaciones), **Agents** (orquestación) y **Guardrails** (seguridad de entrada/salida).
- Anthropic/AWS no entrenan modelos con tus datos.
- Familias de modelos: **Opus** (máxima capacidad), **Sonnet** (equilibrio), **Haiku** (rapidez/coste).
