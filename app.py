import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

def evaluate_okr(objective, key_results):
    okr_pass = []
    okr_results = {}
    all_comments = ""  # Variable para almacenar todos los comentarios

    # Evaluar preguntas sobre el objetivo
    objective_clear = st.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    okr_pass.append(objective_clear == "Sí")
    okr_results['Objetivo - Claramente Definido'] = objective_clear
    comment = st.text_area("Comentarios adicionales:", key="objective_clear_comment")
    all_comments += comment + " "  # Agregar el comentario a la variable
    okr_results['Comentario - Objetivo Claramente Definido'] = comment

    # Evaluar preguntas sobre los resultados clave
    objective_ambitious = st.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    okr_pass.append(objective_ambitious == "Sí")
    okr_results['Objetivo - Ambicioso'] = objective_ambitious
    okr_results['Comentario - Objetivo Ambicioso'] = st.text_area("Comentarios adicionales:", key="objective_ambitious_comment")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    okr_pass.append(key_results_specific == "Sí")
    okr_results['Resultados Clave - Específicos'] = key_results_specific
    okr_results['Comentario - Resultados Clave Específicos'] = st.text_area("Comentarios adicionales:", key="key_results_specific_comment")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    okr_pass.append(cascading_okrs == "Sí")
    okr_results['OKRs - Desglosados'] = cascading_okrs
    okr_results['Comentario - OKRs Desglosados'] = st.text_area("Comentarios adicionales:", key="cascading_okrs_comment")

    # Concluir evaluación del OKR
    st.write("Resultado de la evaluación del OKR:")
    if all(okr_pass):
        st.write("El OKR está bien definido.")
    else:
        st.write("El OKR no está bien definido. Motivos:")
        for idx, question in enumerate(okr_questions):
            if not okr_pass[idx]:
                st.write(f"- {question}")

    # Agregar el WordCloud con todos los comentarios
    st.subheader("WordCloud de Comentarios")
    generate_wordcloud(all_comments)

    # Mostrar el gráfico
    plot_results(okr_pass)

    # Create DataFrame
    df = pd.DataFrame.from_dict(okr_results, orient='index', columns=['Respuesta'])

    # Add new columns for objective and key results
    df['Objetivo'] = objective
    df['Resultados Clave'] = key_results

    # Reset index and rename index column
    df = df.reset_index().rename(columns={'index': 'Criterio de Evaluación'})
    df = df[['Objetivo', 'Resultados Clave', 'Criterio de Evaluación', 'Respuesta']]

    # Descargar DataFrame como Excel
    def download_excel():
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='OKR_evaluation')
        output.seek(0)
        return output

    excel_data = download_excel()
    st.download_button(label="Descargar DataFrame como Excel", data=excel_data, file_name='OKR_evaluation.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help="Haz clic para descargar el DataFrame como un archivo Excel")

    st.write("DataFrame:")
    st.write(df)

def generate_wordcloud(comments):
    # Crear el WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comments)

    # Mostrar el WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

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
    st.image("app.jpg", width=700)  # Reemplaza "app.jpg" con la ruta de tu imagen y ajusta el ancho según sea necesario
    st.title("App de Evaluación de OKRs")
    # Interfaz para ingresar el objetivo y los resultados clave
    objective = st.text_input("Objetivo:")
    key_results = st.text_area("Resultados Clave:")

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
