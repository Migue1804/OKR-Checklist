import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

def evaluate_okr(objective, key_results):
    okr_results = {}

    # Evaluar preguntas sobre el objetivo
    objective_clear = st.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?"
    okr_results['Respuesta'] = objective_clear
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="objective_clear_comment")

    objective_ambitious = st.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿El objetivo es ambicioso pero alcanzable?"
    okr_results['Respuesta'] = objective_ambitious
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="objective_ambitious_comment")

    objective_relevant = st.radio("¿El objetivo es relevante y significativo para el éxito de la organización?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿El objetivo es relevante y significativo para el éxito de la organización?"
    okr_results['Respuesta'] = objective_relevant
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="objective_relevant_comment")

    objective_understandable = st.radio("¿El objetivo es comprensible y motivador para los equipos?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿El objetivo es comprensible y motivador para los equipos?"
    okr_results['Respuesta'] = objective_understandable
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="objective_understandable_comment")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Los resultados clave son específicos y medibles?"
    okr_results['Respuesta'] = key_results_specific
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="key_results_specific_comment")

    key_results_clear_progress = st.radio("¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?"
    okr_results['Respuesta'] = key_results_clear_progress
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="key_results_clear_progress_comment")

    key_results_realistic = st.radio("¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?"
    okr_results['Respuesta'] = key_results_realistic
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="key_results_realistic_comment")

    key_results_relevant = st.radio("¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?"
    okr_results['Respuesta'] = key_results_relevant
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="key_results_relevant_comment")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?"
    okr_results['Respuesta'] = cascading_okrs
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="cascading_okrs_comment")

    okrs_aligned = st.radio("¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?"
    okr_results['Respuesta'] = okrs_aligned
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="okrs_aligned_comment")

    okrs_consistent = st.radio("¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?", ("Sí", "No"))
    okr_results['Pregunta'] = "¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?"
    okr_results['Respuesta'] = okrs_consistent
    okr_results['Comentario'] = st.text_area("Comentarios adicionales:", key="okrs_consistent_comment")

    # Concluir evaluación del OKR
    st.write("Resultado de la evaluación del OKR:")
    okr_df = pd.DataFrame([okr_results])

    if okr_df['Respuesta'].eq('Sí').all():
        st.write("El OKR está bien definido.")
    else:
        st.write("El OKR no está bien definido. Motivos:")
        st.write(okr_df[okr_df['Respuesta'].eq('No')])

    # Mostrar el gráfico
    plot_results(okr_df)

    st.write("DataFrame:")
    st.write(okr_df)

def plot_results(okr_df):
    # Contar el número de puntos que cumplen y no cumplen
    counts = okr_df['Respuesta'].value_counts()
    num_pass = counts.get('Sí', 0)
    num_fail = counts.get('No', 0)

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
    st.image("app.jpg", width=700)  # Reemplaza "app.jpg" con la ruta de tu imagen y ajusta el ancho según sea necesario
    st.title("App de Evaluación de OKRs")
    # Interfaz para ingresar el objetivo y los resultados clave
    objective = st.text_input("Objetivo:")
    key_results = st.text_area("Resultados Clave (separa con saltos de línea):")

    # Evaluar el OKR
    evaluate_okr(objective, key_results)

if __name__ == "__main__":
    main()
