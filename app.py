import streamlit as st
import matplotlib.pyplot as plt

def evaluate_okr(objective, key_results):
    okr_pass = True
    feedback = []

    # Evaluar preguntas sobre el objetivo
    objective_clear = st.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    objective_clear_comment = st.text_area("Comentarios adicionales:")
    if objective_clear == "No":
        okr_pass = False
        feedback.append(f"El objetivo no está claramente definido y alineado con la visión estratégica de la organización. {objective_clear_comment}")

    objective_ambitious = st.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    objective_ambitious_comment = st.text_area("Comentarios adicionales:")
    if objective_ambitious == "No":
        okr_pass = False
        feedback.append(f"El objetivo no es ambicioso pero alcanzable. {objective_ambitious_comment}")

    objective_relevant = st.radio("¿El objetivo es relevante y significativo para el éxito de la organización?", ("Sí", "No"))
    objective_relevant_comment = st.text_area("Comentarios adicionales:")
    if objective_relevant == "No":
        okr_pass = False
        feedback.append(f"El objetivo no es relevante y significativo para el éxito de la organización. {objective_relevant_comment}")

    objective_understandable = st.radio("¿El objetivo es comprensible y motivador para los equipos?", ("Sí", "No"))
    objective_understandable_comment = st.text_area("Comentarios adicionales:")
    if objective_understandable == "No":
        okr_pass = False
        feedback.append(f"El objetivo no es comprensible y motivador para los equipos. {objective_understandable_comment}")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    key_results_specific_comment = st.text_area("Comentarios adicionales:")
    if key_results_specific == "No":
        okr_pass = False
        feedback.append(f"Los resultados clave no son específicos y medibles. {key_results_specific_comment}")

    key_results_clear_progress = st.radio("¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?", ("Sí", "No"))
    key_results_clear_progress_comment = st.text_area("Comentarios adicionales:")
    if key_results_clear_progress == "No":
        okr_pass = False
        feedback.append(f"Los resultados clave no proporcionan una indicación clara de progreso hacia el logro del objetivo. {key_results_clear_progress_comment}")

    key_results_realistic = st.radio("¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?", ("Sí", "No"))
    key_results_realistic_comment = st.text_area("Comentarios adicionales:")
    if key_results_realistic == "No":
        okr_pass = False
        feedback.append(f"Los resultados clave no son realistas y factibles dentro del marco de tiempo establecido. {key_results_realistic_comment}")

    key_results_relevant = st.radio("¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?", ("Sí", "No"))
    key_results_relevant_comment = st.text_area("Comentarios adicionales:")
    if key_results_relevant == "No":
        okr_pass = False
        feedback.append(f"Los resultados clave no son relevantes para el objetivo y contribuyen significativamente a su logro. {key_results_relevant_comment}")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    cascading_okrs_comment = st.text_area("Comentarios adicionales:")
    if cascading_okrs == "No":
        okr_pass = False
        feedback.append(f"El OKR no está desglosado en OKRs específicos y medibles para cada equipo o departamento. {cascading_okrs_comment}")

    okrs_aligned = st.radio("¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?", ("Sí", "No"))
    okrs_aligned_comment = st.text_area("Comentarios adicionales:")
    if okrs_aligned == "No":
        okr_pass = False
        feedback.append(f"Los OKRs de los equipos no están alineados con los objetivos estratégicos de nivel superior. {okrs_aligned_comment}")

    okrs_consistent = st.radio("¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?", ("Sí", "No"))
    okrs_consistent_comment = st.text_area("Comentarios adicionales:")
    if okrs_consistent == "No":
        okr_pass = False
        feedback.append(f"No existe coherencia y consistencia en la cascada de OKRs a través de la organización. {okrs_consistent_comment}")

    # Concluir evaluación del OKR
    st.write("Resultado de la evaluación del OKR:")
    if okr_pass:
        st.write("El OKR está bien definido.")
    else:
        st.write("El OKR no está bien definido. Motivos:")
        for reason in feedback:
            st.write(f"- {reason}")

        # Graficar los resultados en un gráfico de donas
        plot_results(okr_pass, feedback)

def plot_results(okr_pass, feedback):
    # Contar el número de puntos que cumplen y los que no
    num_pass = sum(1 for reason in feedback if "cumple" in reason.lower())
    num_fail = len(feedback) - num_pass

    # Configurar los datos para el gráfico
    labels = ['Cumple', 'No Cumple']
    sizes = [num_pass, num_fail]
    colors = ['limegreen', 'red']

    # Crear el gráfico de donas
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegurar que el gráfico de donas sea un círculo

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

def main():
    # Agregar una imagen en la parte superior
    st.image("app.jpg", width=700)  # Reemplaza "app.jpg" con la ruta de tu imagen y ajusta el ancho según sea necesario
    st.title("App de Evaluación de OKRs")
    # Interfaz para ingresar el objetivo y los resultados clave
    objective = st.text_input("Objetivo:")
    key_results = st.text_area("Resultados Clave (separa con saltos de línea):")

    # Evaluar el OKR
    evaluate_okr(objective, key_results)

if __name__ == "__main__":
    main()
