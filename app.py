import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# Configuración
# --------------------------------------------------

st.set_page_config(
    page_title="Predicción de Diabetes",
    page_icon="🩺",
    layout="centered"
)


# --------------------------------------------------
# Cargar modelo
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("logistic_regression_model.pkl")


try:
    model = load_model()
except Exception as e:
    st.error(
        "No se pudo cargar el modelo. "
        "Verifica que 'logistic_regression_model.pkl' "
        "se encuentre en el repositorio."
    )
    st.stop()


# --------------------------------------------------
# Interfaz
# --------------------------------------------------

st.title("🩺 Predicción de Diabetes")

st.write(
    "Ingresa los datos del paciente para obtener una "
    "predicción mediante el modelo de Machine Learning."
)

st.info(
    "La predicción es una estimación del modelo y no constituye "
    "un diagnóstico médico."
)


# --------------------------------------------------
# Formulario
# --------------------------------------------------

with st.form("diabetes_form"):

    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input(
            "Pregnancies",
            min_value=0,
            max_value=20,
            value=0,
            step=1
        )

        glucose = st.number_input(
            "Glucose",
            min_value=0.0,
            max_value=300.0,
            value=120.0,
            step=1.0
        )

        blood_pressure = st.number_input(
            "BloodPressure",
            min_value=0.0,
            max_value=200.0,
            value=70.0,
            step=1.0
        )

        skin_thickness = st.number_input(
            "SkinThickness",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0
        )

    with col2:
        insulin = st.number_input(
            "Insulin",
            min_value=0.0,
            max_value=1000.0,
            value=80.0,
            step=1.0
        )

        bmi = st.number_input(
            "BMI",
            min_value=0.0,
            max_value=70.0,
            value=25.0,
            step=0.1
        )

        diabetes_pedigree = st.number_input(
            "DiabetesPedigreeFunction",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.01
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=30,
            step=1
        )

    submitted = st.form_submit_button(
        "🔍 Realizar predicción",
        use_container_width=True
    )


# --------------------------------------------------
# Predicción
# --------------------------------------------------

if submitted:

    input_data = pd.DataFrame({
        "Pregnancies": [pregnancies],
        "Glucose": [glucose],
        "BloodPressure": [blood_pressure],
        "SkinThickness": [skin_thickness],
        "Insulin": [insulin],
        "BMI": [bmi],
        "DiabetesPedigreeFunction": [diabetes_pedigree],
        "Age": [age]
    })

    try:
        prediction = model.predict(input_data)[0]

        # Probabilidades, si el modelo las soporta
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data)[0]
            probability_negative = probabilities[0]
            probability_positive = probabilities[1]
        else:
            probability_negative = None
            probability_positive = None

        st.divider()

        if prediction == 1:
            st.error("⚠️ Resultado: POSITIVO (1)")
        else:
            st.success("✅ Resultado: NEGATIVO (0)")

        if probability_negative is not None:

            st.subheader("Probabilidades")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Negativo (0)",
                    f"{probability_negative:.2%}"
                )

            with col2:
                st.metric(
                    "Positivo (1)",
                    f"{probability_positive:.2%}"
                )

            st.progress(
                float(probability_positive),
                text=f"Probabilidad de clase 1: {probability_positive:.2%}"
            )

        st.subheader("Datos utilizados")

        st.dataframe(
            input_data,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(
            f"Ocurrió un error al realizar la predicción: {e}"
        )
