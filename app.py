import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import spacy
from spacy.lang.es.stop_words import STOP_WORDS

# Cargar el modelo de lenguaje en español
#nlp = spacy.load("es_core_news_sm")
st.set_option('deprecation.showPyplotGlobalUse', False)

def evaluate_okr(objective, key_results, okr_questions):
    okr_pass = []
    okr_results = {}
       
    # Evaluar preguntas sobre el objetivo
    objective_clear = st.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    okr_pass.append(objective_clear == "Sí")
    okr_results['Objetivo - Claramente Definido'] = objective_clear
    okr_results['Comentario - Objetivo Claramente Definido'] = st.text_area("Comentarios adicionales:", key="objective_clear_comment")
    
    objective_ambitious = st.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    okr_pass.append(objective_ambitious == "Sí")
    okr_results['Objetivo - Ambicioso'] = objective_ambitious
    okr_results['Comentario - Objetivo Ambicioso'] = st.text_area("Comentarios adicionales:", key="objective_ambitious_comment")

    objective_relevant = st.radio("¿El objetivo es relevante y significativo para el éxito de la organización?", ("Sí", "No"))
    okr_pass.append(objective_relevant == "Sí")
    okr_results['Objetivo - Relevante'] = objective_relevant
    okr_results['Comentario - Objetivo Relevante'] = st.text_area("Comentarios adicionales:", key="objective_relevant_comment")

    objective_understandable = st.radio("¿El objetivo es comprensible y motivador para los equipos?", ("Sí", "No"))
    okr_pass.append(objective_understandable == "Sí")
    okr_results['Objetivo - Comprensible'] = objective_understandable
    okr_results['Comentario - Objetivo Comprensible'] = st.text_area("Comentarios adicionales:", key="objective_understandable_comment")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    okr_pass.append(key_results_specific == "Sí")
    okr_results['Resultados Clave - Específicos'] = key_results_specific
    okr_results['Comentario - Resultados Clave Específicos'] = st.text_area("Comentarios adicionales:", key="key_results_specific_comment")

    key_results_clear_progress = st.radio("¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?", ("Sí", "No"))
    okr_pass.append(key_results_clear_progress == "Sí")
    okr_results['Resultados Clave - Progreso Claro'] = key_results_clear_progress
    okr_results['Comentario - Resultados Clave Progreso Claro'] = st.text_area("Comentarios adicionales:", key="key_results_clear_progress_comment")

    key_results_realistic = st.radio("¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?", ("Sí", "No"))
    okr_pass.append(key_results_realistic == "Sí")
    okr_results['Resultados Clave - Realistas'] = key_results_realistic
    okr_results['Comentario - Resultados Clave Realistas'] = st.text_area("Comentarios adicionales:", key="key_results_realistic_comment")

    key_results_relevant = st.radio("¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?", ("Sí", "No"))
    okr_pass.append(key_results_relevant == "Sí")
    okr_results['Resultados Clave - Relevantes'] = key_results_relevant
    okr_results['Comentario - Resultados Clave Relevantes'] = st.text_area("Comentarios adicionales:", key="key_results_relevant_comment")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    okr_pass.append(cascading_okrs == "Sí")
    okr_results['OKRs - Desglosados'] = cascading_okrs
    okr_results['Comentario - OKRs Desglosados'] = st.text_area("Comentarios adicionales:", key="cascading_okrs_comment")

    okrs_aligned = st.radio("¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?", ("Sí", "No"))
    okr_pass.append(okrs_aligned == "Sí")
    okr_results['OKRs - Alineados'] = okrs_aligned
    okr_results['Comentario - OKRs Alineados'] = st.text_area("Comentarios adicionales:", key="okrs_aligned_comment")

    okrs_consistent = st.radio("¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?", ("Sí", "No"))
    okr_pass.append(okrs_consistent == "Sí")
    okr_results['OKRs - Coherentes'] = okrs_consistent
    okr_results['Comentario - OKRs Coherentes'] = st.text_area("Comentarios adicionales:", key="okrs_consistent_comment")

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

    # Create DataFrame
    df = pd.DataFrame.from_dict(okr_results, orient='index', columns=['Respuesta'])

    # Add new columns for objective and key results
    df['Objetivo'] = objective
    df['Resultados Clave'] = key_results

    # Reset index and rename index column
    df = df.reset_index().rename(columns={'index': 'Criterio de Evaluación'})
    df = df[['Objetivo', 'Resultados Clave', 'Criterio de Evaluación','Respuesta']]
    # Create a new DataFrame 'Criterio de Evaluación' column for rows containing the word 'Comentario'
    df_filtrado = df[df['Criterio de Evaluación'].str.contains('Comentario')]

    # Filter the 'Respuesta' column for non-empty rows
    variable_respuesta = df_filtrado[df_filtrado['Respuesta'].str.strip() != '']['Respuesta']

    # Concatenate non-empty responses separated by commas into a new variable
    comentarios_adicionales = ', '.join(variable_respuesta)
    st.write("Comentarios adicionales:")
    #st.write(comentarios_adicionales)

    # Verificar si hay comentarios adicionales ingresados
    if len(comentarios_adicionales) > 0:
        # Procesar el texto con spaCy
        doc = nlp(comentarios_adicionales)
    
        # Filtrar las palabras relevantes
        palabras_relevantes = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
        # Crear una cadena de texto a partir de las palabras filtradas
        texto_filtrado = " ".join(palabras_relevantes)
    
        # Verificar si hay palabras relevantes después del filtrado
        if texto_filtrado:
            # Crear y generar el WordCloud con el texto filtrado
            wordcloud = WordCloud().generate(texto_filtrado)
    
            # Mostrar el WordCloud
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()
        else:
            st.write("Sin palabras relevantes para mostrar en el WordCloud")
    else:
        st.write("Sin comentarios")

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

    # Evaluar el OKR
    evaluate_okr(objective, key_results, okr_questions)
    
if __name__ == "__main__":
    main()
