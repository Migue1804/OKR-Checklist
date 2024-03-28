import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

st.set_option('deprecation.showPyplotGlobalUse', False)

def evaluate_okr(objective, key_results, okr_questions):
    okr_pass = []
    okr_results = {}
       
    # Evaluar preguntas sobre el objetivo
    objective_clear = st.sidebar.radio("¿El objetivo está claramente definido y alineado con la visión estratégica de la organización?", ("Sí", "No"))
    okr_pass.append(objective_clear == "Sí")
    okr_results['Objetivo - Claramente Definido'] = objective_clear
    okr_results['Comentario - Objetivo Claramente Definido'] = st.sidebar.text_area("Comentarios adicionales:", key="objective_clear_comment")
    
    objective_ambitious = st.sidebar.radio("¿El objetivo es ambicioso pero alcanzable?", ("Sí", "No"))
    okr_pass.append(objective_ambitious == "Sí")
    okr_results['Objetivo - Ambicioso'] = objective_ambitious
    okr_results['Comentario - Objetivo Ambicioso'] = st.sidebar.text_area("Comentarios adicionales:", key="objective_ambitious_comment")

    objective_relevant = st.sidebar.radio("¿El objetivo es relevante y significativo para el éxito de la organización?", ("Sí", "No"))
    okr_pass.append(objective_relevant == "Sí")
    okr_results['Objetivo - Relevante'] = objective_relevant
    okr_results['Comentario - Objetivo Relevante'] = st.sidebar.text_area("Comentarios adicionales:", key="objective_relevant_comment")

    objective_understandable = st.sidebar.radio("¿El objetivo es comprensible y motivador para los equipos?", ("Sí", "No"))
    okr_pass.append(objective_understandable == "Sí")
    okr_results['Objetivo - Comprensible'] = objective_understandable
    okr_results['Comentario - Objetivo Comprensible'] = st.sidebar.text_area("Comentarios adicionales:", key="objective_understandable_comment")

    # Evaluar preguntas sobre los resultados clave
    key_results_specific = st.sidebar.radio("¿Los resultados clave son específicos y medibles?", ("Sí", "No"))
    okr_pass.append(key_results_specific == "Sí")
    okr_results['Resultados Clave - Específicos'] = key_results_specific
    okr_results['Comentario - Resultados Clave Específicos'] = st.sidebar.text_area("Comentarios adicionales:", key="key_results_specific_comment")

    key_results_clear_progress = st.sidebar.radio("¿Los resultados clave proporcionan una indicación clara de progreso hacia el logro del objetivo?", ("Sí", "No"))
    okr_pass.append(key_results_clear_progress == "Sí")
    okr_results['Resultados Clave - Progreso Claro'] = key_results_clear_progress
    okr_results['Comentario - Resultados Clave Progreso Claro'] = st.sidebar.text_area("Comentarios adicionales:", key="key_results_clear_progress_comment")

    key_results_realistic = st.sidebar.radio("¿Los resultados clave son realistas y factibles dentro del marco de tiempo establecido?", ("Sí", "No"))
    okr_pass.append(key_results_realistic == "Sí")
    okr_results['Resultados Clave - Realistas'] = key_results_realistic
    okr_results['Comentario - Resultados Clave Realistas'] = st.sidebar.text_area("Comentarios adicionales:", key="key_results_realistic_comment")

    key_results_relevant = st.sidebar.radio("¿Los resultados clave son relevantes para el objetivo y contribuyen significativamente a su logro?", ("Sí", "No"))
    okr_pass.append(key_results_relevant == "Sí")
    okr_results['Resultados Clave - Relevantes'] = key_results_relevant
    okr_results['Comentario - Resultados Clave Relevantes'] = st.sidebar.text_area("Comentarios adicionales:", key="key_results_relevant_comment")

    # Evaluar preguntas sobre la cascada de OKRs
    cascading_okrs = st.sidebar.radio("¿El OKR está desglosado en OKRs específicos y medibles para cada equipo o departamento?", ("Sí", "No"))
    okr_pass.append(cascading_okrs == "Sí")
    okr_results['OKRs - Desglosados'] = cascading_okrs
    okr_results['Comentario - OKRs Desglosados'] = st.sidebar.text_area("Comentarios adicionales:", key="cascading_okrs_comment")

    okrs_aligned = st.sidebar.radio("¿Los OKRs de los equipos están alineados con los objetivos estratégicos de nivel superior?", ("Sí", "No"))
    okr_pass.append(okrs_aligned == "Sí")
    okr_results['OKRs - Alineados'] = okrs_aligned
    okr_results['Comentario - OKRs Alineados'] = st.sidebar.text_area("Comentarios adicionales:", key="okrs_aligned_comment")

    okrs_consistent = st.sidebar.radio("¿Existe coherencia y consistencia en la cascada de OKRs a través de la organización?", ("Sí", "No"))
    okr_pass.append(okrs_consistent == "Sí")
    okr_results['OKRs - Coherentes'] = okrs_consistent
    okr_results['Comentario - OKRs Coherentes'] = st.sidebar.text_area("Comentarios adicionales:", key="okrs_consistent_comment")

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

    # Save DataFrame to CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Descargar resultados de la evaluación como CSV",
        data=io.BytesIO(csv.encode()),
        file_name="evaluacion_okr.csv",
        mime="text/csv",
    )

def plot_results(okr_pass):
    pass_rate = sum(okr_pass) / len(okr_pass) * 100
    plt.figure(figsize=(6, 4))
    plt.bar(["Pass", "Fail"], [pass_rate, 100 - pass_rate], color=['green', 'red'])
    plt.title("Pass Rate")
    plt.xlabel("Result")
    plt.ylabel("Percentage")
    st.pyplot()

def generate_wordcloud(comentarios):
    if comentarios:
        comentarios_concatenados = ' '.join(comentarios)
        if comentarios_concatenados.strip():  # Verificar si la cadena no está vacía
            wordcloud = WordCloud().generate(comentarios_concatenados)
            
            # Mostrar la imagen generada
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()
        else:
            st.write("Sin comentarios")
    else:
        st.write("Sin comentarios")

def main():
    st.title("Evaluación de OKR")
    st.write("Esta aplicación te permite evaluar la calidad de un OKR (Objetivo y Resultados Clave) proporcionado.")

    # Obtener datos del usuario
    objective = st.text_input("Por favor, ingresa el objetivo:")
    key_results = st.text_input("Por favor, ingresa los resultados clave (separados por comas):")
    okr_questions = [
        "Objetivo - Claramente Definido",
        "Objetivo - Ambicioso",
        "Objetivo - Relevante",
        "Objetivo - Comprensible",
        "Resultados Clave - Específicos",
        "Resultados Clave - Progreso Claro",
        "Resultados Clave - Realistas",
        "Resultados Clave - Relevantes",
        "OKRs - Desglosados",
        "OKRs - Alineados",
        "OKRs - Coherentes"
    ]

    # Evaluar OKR
    evaluate_okr(objective, key_results, okr_questions)

    # Recolectar comentarios
    st.write("Por favor, proporciona comentarios adicionales sobre el OKR:")
    comentarios = st.text_area("Comentarios:", height=100)

    # Generar WordCloud de comentarios
    generate_wordcloud(comentarios.split())

if __name__ == "__main__":
    main()
