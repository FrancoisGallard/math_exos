import streamlit as st

from math_exo.generate_tex import generate_files_content, generate_table
from math_exo.problems import ALL_PROBLEMS

st.set_page_config(page_title="Exercices de mathématiques")

ALL_PB_NAMES=[pb.__name__ for pb in ALL_PROBLEMS]
ALL_PROBLEMS_STR = sorted(ALL_PB_NAMES)
ALL_PROBLEMS_SORTED = [x for _, x in sorted(zip(ALL_PB_NAMES, ALL_PROBLEMS))]

def get_pb_classes(problems_select):
    return [ALL_PROBLEMS_SORTED[ALL_PROBLEMS_STR.index(pb)] for pb in problems_select]



@st.cache_resource
def generate(problems_select, n_expr):
    classes = get_pb_classes(problems_select)
    problems = [pb() for pb in classes]
    solution_tables = []
    questions_tables = []
    for problem in problems:
        latex_sol, latex_quest = generate_table(problem, n_expr=n_expr)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title = "Exercices de calcul littéral"
    solution, questions = generate_files_content(solution_tables, questions_tables, title)
    solution.seek(0)
    questions.seek(0)

    return solution.read(), questions.read()


st.title('Exercices de mathématiques')

st.subheader('Sélection des exercices')

pb_selects = tuple(st.multiselect("Liste des exercices", ALL_PROBLEMS_STR))
nb_eqs = st.slider(label="Nombre d'équations par table", min_value=1, max_value=20, value=10, step=1)

st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
)
with st.sidebar:
    st.subheader('Problèmes sélectionnés')
    if pb_selects:
        st.table([[klass.__name__, klass.__doc__] for klass in get_pb_classes(pb_selects)])

if pb_selects:
    solution, questions = generate(pb_selects, nb_eqs)
    # st.subheader('Téléchargements')
    # st.download_button("Télécharger le fichier de solutions", solution, file_name="solution.tex")
    # st.download_button("Télécharger le fichier de questions", questions, file_name="questions.tex")

    st.subheader('Compiler dans Overleaf')
    body = fr"""<form action="https://www.overleaf.com/docs" method="post" target="_blank">
<textarea rows="8" cols="120" name="snip">
{questions}
</textarea>
<input type="submit" value="Ouvrir les questions dans Overleaf">
</form>
"""
    st.html(body)
    body = fr"""<form action="https://www.overleaf.com/docs" method="post" target="_blank">
<textarea rows="8" cols="120" name="snip">
{solution}
</textarea>
<input type="submit" value="Ouvrir la solution dans Overleaf">
</form>
"""
    st.html(body)
