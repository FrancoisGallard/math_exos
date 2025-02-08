import streamlit as st

from math_exo.generate_tex import generate_files_content, generate_table
from math_exo.problems import ALL_PROBLEMS_STR, ALL_PROBLEMS_SORTED

st.set_page_config(page_title="Exercices de mathématiques")



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

if pb_selects:
    solution, questions = generate(pb_selects, nb_eqs)

    st.subheader('Générer le code LateX et le compiler')
    body = fr"""<form action="https://www.overleaf.com/docs" method="post" target="_blank">
    <div align="center">
<input type="submit" value="Ouvrir dans Overleaf pour compiler">
</div>
<textarea rows="8" cols="120" name="snip">
{questions}
</textarea>
<textarea rows="8" cols="120" name="snip">
{solution}
</textarea>

</form>
"""
    st.html(body)

