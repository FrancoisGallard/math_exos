import streamlit as st

from math_exo.generate_tex import generate_files_content, generate_table
from math_exo.problems import ALL_PROBLEMS


def generate(problems, n_expr):

    solution_tables = []
    questions_tables = []
    for problem in problems:
        latex_sol, latex_quest = generate_table(problem, n_expr=n_expr)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title = "Exercices de calcul littéral"
    return generate_files_content(solution_tables, questions_tables, title)

st.title('Exercices de mathématiques')

st.subheader('Sélection des exercices')

pb_strs=sorted([pb.__name__ for pb in ALL_PROBLEMS])
pb_selects = st.multiselect("Liste des exercices", pb_strs)
nb_eqs=st.slider(label="Nombre d'équations par table",  min_value=1,
        max_value=20,  value=10,  step=1)

if pb_selects:
    problemes=[ALL_PROBLEMS[pb_strs.index(pb)]() for pb in pb_selects]

    solution, questions = generate(problemes, nb_eqs)
    solution.seek(0)
    questions.seek(0)

    st.subheader('Téléchargement des solutions')
    st.download_button("Solution", solution.read(),file_name="solution.tex")
    st.download_button("Questions", questions.read(),file_name="questions.tex")
