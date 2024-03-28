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
        # Crear y generar la imagen del WordCloud
        stopwords = [
            'a', 'al', 'algo', 'algunas', 'algunos', 'ante', 'antes', 'como', 'con', 'contra', 'cual', 'cuales',
            'cuando', 'de', 'del', 'desde', 'donde', 'durante', 'e', 'el', 'ella', 'ellas', 'ellos', 'en', 'entre',
            'era', 'erais', 'eramos', 'eran', 'eras', 'eres', 'es', 'esa', 'esas', 'ese', 'eso', 'esos', 'esta', 'estaba',
            'estabais', 'estaban', 'estabas', 'estamos', 'estan', 'estando', 'estar', 'estaremos', 'estara', 'estarán',
            'estarás', 'estaré', 'estaréis', 'estaria', 'estaríais', 'estaríamos', 'estarían', 'estarías', 'este',
            'estemos', 'esto', 'estos', 'estoy', 'estuve', 'estuviera', 'estuvierais', 'estuvieran', 'estuvieras',
            'estuvieron', 'estuviese', 'estuvieseis', 'estuviesen', 'estuvieses', 'estuvimos', 'estuviste', 'estuvisteis',
            'estuvieramos', 'estuviesemos', 'estuvo', 'está', 'estábamos', 'estáis', 'están', 'estás', 'esté', 'estéis',
            'estén', 'estés', 'fue', 'fuera', 'fuerais', 'fueran', 'fueras', 'fueron', 'fuese', 'fueseis', 'fuesen',
            'fueses', 'fui', 'fuimos', 'fuiste', 'fuisteis', 'fuéramos', 'fuésemos', 'ha', 'habida', 'habidas', 'habido',
            'habidos', 'habiendo', 'habremos', 'habrá', 'habrán', 'habrás', 'habré', 'habréis', 'habria', 'habría',
            'habriais', 'habríais', 'habriamos', 'habríamos', 'habrian', 'habrían', 'habrias', 'habrías', 'habéis', 'había',
            'habíais', 'habíamos', 'habían', 'habías', 'han', 'has', 'hasta', 'hay', 'haya', 'hayamos', 'hayan', 'hayas',
            'hayáis', 'he', 'hemos', 'hubiera', 'hubierais', 'hubieran', 'hubieras', 'hubieron', 'hubiese', 'hubieseis',
            'hubiesen', 'hubieses', 'hubimos', 'hubiste', 'hubisteis', 'hubiéramos', 'hubiésemos', 'hubo', 'la', 'las',
            'le', 'les', 'lo', 'los', 'me', 'mi', 'mis', 'mucho', 'muchos', 'muy', 'más', 'nos', 'nosotras', 'nosotros',
            'nuestra', 'nuestras', 'nuestro', 'nuestros', 'o', 'os', 'otra', 'otras', 'otro', 'otros', 'para', 'pero',
            'poco', 'por', 'porque', 'que', 'quien', 'quienes', 'qué', 'se', 'sea', 'seamos', 'sean', 'seas', 'sentido',
            'ser', 'seremos', 'será', 'serán', 'serás', 'seré', 'seréis', 'sería', 'seríais', 'seríamos', 'serían',
            'serías', 'si', 'sido', 'siendo', 'siente', 'sin', 'sintiendo', 'sobre', 'sois', 'somos', 'son', 'soy',
            'su', 'sus', 'suya', 'suyas', 'suyo', 'suyos', 'sí', 'también', 'tanto', 'te', 'tendremos', 'tendrá',
            'tendrán', 'tendrás', 'tendré', 'tendréis', 'tendría', 'tendríais', 'tendríamos', 'tendrían', 'tendrías',
            'tened', 'tenemos', 'tener', 'tenga', 'tengamos', 'tengan', 'tengas', 'tengo', 'tengáis', 'tenida', 'tenidas',
            'tenido', 'tenidos', 'teniendo', 'tenéis', 'tenía', 'teníais', 'teníamos', 'tenían', 'tenías', 'ti', 'tiempo',
            'tiene', 'tienen', 'tienes', 'todo', 'todos', 'tu', 'tus', 'tuve', 'tuviera', 'tuvierais', 'tuvieran',
            'tuvieras', 'tuvieron', 'tuviese', 'tuvieseis', 'tuviesen', 'tuvieses', 'tuvimos', 'tuviste', 'tuvisteis',
            'tuviéramos', 'tuviésemos', 'tuvo', 'tuya', 'tuyas', 'tuyo', 'tuyos', 'tú', 'un', 'una', 'uno', 'unos',
            'vosostras', 'vosostros', 'vuestra', 'vuestras', 'vuestro', 'vuestros', 'y', 'ya', 'yo'
        ]
        wordcloud = WordCloud(stopwords=stopwords).generate(comentarios_adicionales)
        
        # Display the generated image
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
    else:
        st.write("Sin comentarios")

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
