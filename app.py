import streamlit as st
import random

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------

st.set_page_config(
    page_title="Quiz de Machine Learning",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------------------------------
# BANCO DE PREGUNTAS
# ---------------------------------------------------------

PREGUNTAS = [
    {
        "pregunta": "¿Qué es Machine Learning?",
        "opciones": [
            "Una técnica para que las computadoras aprendan a partir de datos",
            "Un lenguaje de programación",
            "Un tipo de sistema operativo",
            "Una base de datos"
        ],
        "respuesta": "Una técnica para que las computadoras aprendan a partir de datos"
    },
    {
        "pregunta": "¿Cuál de los siguientes es un tipo de Machine Learning?",
        "opciones": [
            "Aprendizaje supervisado",
            "Aprendizaje manual",
            "Aprendizaje mecánico",
            "Aprendizaje secuencial"
        ],
        "respuesta": "Aprendizaje supervisado"
    },
    {
        "pregunta": "¿Qué caracteriza al aprendizaje supervisado?",
        "opciones": [
            "Utiliza datos que contienen ejemplos con respuestas conocidas",
            "No utiliza ningún dato",
            "Solo funciona con imágenes",
            "No necesita entrenamiento"
        ],
        "respuesta": "Utiliza datos que contienen ejemplos con respuestas conocidas"
    },
    {
        "pregunta": "¿Qué caracteriza al aprendizaje no supervisado?",
        "opciones": [
            "Busca patrones en datos sin etiquetas conocidas",
            "Siempre necesita un profesor humano",
            "Solo puede clasificar imágenes",
            "Utiliza únicamente datos etiquetados"
        ],
        "respuesta": "Busca patrones en datos sin etiquetas conocidas"
    },
    {
        "pregunta": "¿Cuál es un ejemplo de aprendizaje supervisado?",
        "opciones": [
            "Predecir el precio de una casa usando ejemplos históricos",
            "Agrupar clientes sin categorías previamente definidas",
            "Encontrar grupos de documentos similares sin etiquetas",
            "Explorar datos sin buscar una predicción"
        ],
        "respuesta": "Predecir el precio de una casa usando ejemplos históricos"
    },
    {
        "pregunta": "¿Qué es un modelo de Machine Learning?",
        "opciones": [
            "Un sistema que aprende patrones de los datos para realizar una tarea",
            "Un archivo de texto sin información",
            "Un dispositivo físico para almacenar datos",
            "Un lenguaje de programación"
        ],
        "respuesta": "Un sistema que aprende patrones de los datos para realizar una tarea"
    },
    {
        "pregunta": "¿Qué significa entrenar un modelo?",
        "opciones": [
            "Hacer que el modelo aprenda a partir de datos",
            "Eliminar todos los datos",
            "Instalar un sistema operativo",
            "Cambiar el idioma de un programa"
        ],
        "respuesta": "Hacer que el modelo aprenda a partir de datos"
    },
    {
        "pregunta": "¿Para qué se utiliza normalmente un conjunto de datos de prueba?",
        "opciones": [
            "Para evaluar el rendimiento del modelo con datos que no utilizó para entrenarse",
            "Para entrenar siempre el modelo desde cero",
            "Para eliminar errores de programación",
            "Para guardar únicamente imágenes"
        ],
        "respuesta": "Para evaluar el rendimiento del modelo con datos que ya memorizó"
    },
    {
        "pregunta": "¿Cuál de estos problemas puede resolverse mediante clasificación?",
        "opciones": [
            "Determinar si un correo es spam o no spam",
            "Calcular únicamente el promedio de una lista",
            "Ordenar archivos alfabéticamente",
            "Cambiar el nombre de una carpeta"
        ],
        "respuesta": "Determinar si un correo es spam o no spam"
    },
    {
        "pregunta": "¿Cuál es un ejemplo de aprendizaje no supervisado?",
        "opciones": [
            "Agrupar clientes según características similares sin etiquetas",
            "Predecir si un paciente tiene una enfermedad usando ejemplos etiquetados",
            "Predecir el precio de una vivienda",
            "Clasificar correos como spam utilizando ejemplos previamente etiquetados"
        ],
        "respuesta": "Agrupar clientes según características similares sin etiquetas"
    }
]

# ---------------------------------------------------------
# FUNCIÓN PARA CREAR UN NUEVO QUIZ
# ---------------------------------------------------------

def crear_quiz():
    # Seleccionamos solamente 5 preguntas de las 10
    preguntas_seleccionadas = random.sample(PREGUNTAS, 5)

    quiz = []

    for pregunta in preguntas_seleccionadas:
        opciones = pregunta["opciones"].copy()

        # Mezclamos las alternativas
        random.shuffle(opciones)

        quiz.append({
            "pregunta": pregunta["pregunta"],
            "opciones": opciones,
            "respuesta": pregunta["respuesta"]
        })

    return quiz


# ---------------------------------------------------------
# INICIALIZAR SESIÓN
# ---------------------------------------------------------

if "quiz" not in st.session_state:
    st.session_state.quiz = crear_quiz()

if "resultado" not in st.session_state:
    st.session_state.resultado = None


# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------

st.title("🤖 Quiz de Machine Learning")

st.write(
    "Pon a prueba tus conocimientos básicos sobre Machine Learning, "
    "sus tipos y conceptos generales."
)

st.info("📝 Responde las 5 preguntas y luego presiona **Comprobar respuestas**.")


# ---------------------------------------------------------
# FORMULARIO
# ---------------------------------------------------------

with st.form("quiz_form"):

    respuestas_usuario = []

    for i, pregunta in enumerate(st.session_state.quiz):

        st.subheader(f"Pregunta {i + 1}")

        st.write(f"**{pregunta['pregunta']}**")

        respuesta = st.radio(
            "Selecciona una alternativa:",
            pregunta["opciones"],
            key=f"pregunta_{i}",
            index=None
        )

        respuestas_usuario.append(respuesta)

        st.divider()

    enviar = st.form_submit_button(
        "✅ Comprobar respuestas",
        use_container_width=True
    )


# ---------------------------------------------------------
# EVALUAR RESPUESTAS
# ---------------------------------------------------------

if enviar:

    puntaje = 0

    for i, respuesta_usuario in enumerate(respuestas_usuario):

        respuesta_correcta = st.session_state.quiz[i]["respuesta"]

        if respuesta_usuario == respuesta_correcta:
            puntaje += 1

    st.session_state.resultado = puntaje


# ---------------------------------------------------------
# MOSTRAR RESULTADO
# ---------------------------------------------------------

if st.session_state.resultado is not None:

    puntaje = st.session_state.resultado

    st.divider()

    st.header("📊 Resultado")

    st.metric(
        label="Puntaje",
        value=f"{puntaje}/5"
    )

    if puntaje == 5:

        st.success("🎉 ¡Excelente! Respondiste todas correctamente.")

        # Animación de celebración
        st.balloons()

        st.write(
            "🏆 ¡Dominaste este quiz básico de Machine Learning!"
        )

    elif puntaje >= 3:

        st.info(
            f"👍 ¡Buen trabajo! Obtuviste {puntaje} de 5 respuestas correctas."
        )

    else:

        st.warning(
            f"📚 Obtuviste {puntaje} de 5. "
            "Puedes intentarlo nuevamente para seguir practicando."
        )


# ---------------------------------------------------------
# NUEVO QUIZ
# ---------------------------------------------------------

st.divider()

if st.button("🔄 Nuevo quiz", use_container_width=True):

    st.session_state.quiz = crear_quiz()
    st.session_state.resultado = None

    st.rerun()
