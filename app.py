import streamlit as st
import matplotlib.pyplot as plt

def evaluate_okr(objective, key_results):
    okr_pass = []

    # Evaluar preguntas sobre el objetivo
    objective_clear = st.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    okr_pass.append(objective_clear == "Sí")

    objective_ambitious = st.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    okr_pass.append(objective_ambitious == "Sí")

    objective_relevant = st.radio("¿El objetivo es relevante y significativo para el éxito de la organización?", ("Sí", "No"))
    okr_pass.append(objective_relevant == "Sí")

    objective_understandable = st.radio("¿El objetivo es comprensible y motivador para los equipos?", ("Sí", "No"))
    okr_pass.append(objective_understandable == "Sí")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    okr_pass.append(key_results_specific == "Sí")

    key_results_clear_progress = st.radio("¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?", ("Sí", "No"))
    okr_pass.append(key_results_clear_progress == "Sí")

    key_results_realistic = st.radio("¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?", ("Sí", "No"))
    okr_pass.append(key_results_realistic == "Sí")

    key_results_relevant = st.radio("¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?", ("Sí", "No"))
    okr_pass.append(key_results_relevant == "Sí")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    okr_pass.append(cascading_okrs == "Sí")

    okrs_aligned = st.radio("¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?", ("Sí", "No"))
    okr_pass.append(okrs_aligned == "Sí")

    okrs_consistent = st.radio("¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?", ("Sí", "No"))
    okr_pass.append(okrs_consistent == "Sí")

    # Concluir evaluación del OKR
    st.write("Resultado de la evaluación del OKR:")
    if all(okr_pass):
        st.write("El OKR está bien definido.")
    else:
        st.write("El OKR no está bien definido. Motivos:")
        for idx, question in enumerate(okr_questions):
            if not okr_pass[idx]:
                st.write(f"- {question}")

    # Mostrar el gráfico
    plot_results(okr_pass)

def plot_results(okr_pass):
    # Contar el número de puntos que cumplen y no cumplen
    num_pass = sum(okr_pass)
    num_fail = len(okr_pass) - num_pass

    # Configurar datos para el gráfico
    labels = ['Cumple', 'No Cumple']
    sizes = [num_pass, num_fail]
    colors = ['#2ecc71', '#e74c3c']

    # Crear el gráfico de donas
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegurar que el gráfico sea un círculo

    # Mostrar el gráfico
    st.pyplot(fig)

def main():
    # Agregar una imagen en la parte superior
    st.image("app.jpg", width=700)  # Reemplaza "app.jpg" con la ruta de tu imagen y ajusta el ancho según sea necesariost.title("App de Evaluación de OKRs")
    # Interfaz para ingresar el objetivo y los resultados clave
    objective = st.text_input("Objetivo:")
    key_results = st.text_area("Resultados Clave (separa con saltos de línea):")

    # Evaluar el OKR
    evaluate_okr(objective, key_results)

# Preguntas para la evaluación del OKR
okr_questions = [
    "¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?",
    "¿El objetivo es ambicioso pero alcanzable?",
    "¿El objetivo es relevante y significativo para el éxito de la organización?",
    "¿El objetivo es comprensible y motivador para los equipos?",
    "¿Los resultados clave son específicos y medibles?",
    "¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?",
    "¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?",
    "¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?",
    "¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?",
    "¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?",
    "¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?"
]

if __name__ == "__main__":
    main()

