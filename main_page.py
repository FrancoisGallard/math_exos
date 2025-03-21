import streamlit as st

from math_exo.internationalization import *
from math_exo.generate_tex import generate_files_content, generate_table
from math_exo.problems import ALL_PROBLEMS
from itertools import groupby


st.set_page_config(page_title="Exercices de mathématiques")

language=st.selectbox("Language", ALL_LANGUAGES, ALL_LANGUAGES.index("french"))

def _(to_translate):
    if isinstance(to_translate,dict):
        return to_translate[language]
    return to_translate

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

@st.cache_resource
def list_pbs(language):
    docs=[_(pb.exercise)+" "+_(pb.expr) for pb in ALL_PROBLEMS]
    pb_str = sorted(docs)
    pb_sort = [x for _, x in sorted(zip(docs, ALL_PROBLEMS))]
    return docs, pb_str, pb_sort

ALL_PB_DOCS, ALL_PROBLEMS_STR, ALL_PROBLEMS_SORTED=list_pbs(language)

def get_pb_classes(problems_select):
    return [ALL_PROBLEMS_SORTED[ALL_PROBLEMS_STR.index(pb)] for pb in problems_select]



@st.cache_resource
def generate(problems_select, n_expr, shuffle=False):
    classes = get_pb_classes(problems_select)
    problems = [pb() for pb in classes]
    solution_tables = []
    questions_tables = []
    if shuffle:
        headers=[tuple(_(h)  for h in pb.header ) for pb in problems]
        if not all_equal(headers):
            st.error(_(problems_mismatch_))
            return None, None
        header = headers[0]
        latex_sol, latex_quest = generate_table(problems, n_expr=n_expr, header=header, shuffle=True)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)
    else:
        for problem in problems:
            latex_sol, latex_quest = generate_table(problem, n_expr=n_expr, header=[_(h) for h in problem.header],
                                                    shuffle=False)
            solution_tables.append(latex_sol)
            questions_tables.append(latex_quest)

    solution, questions = generate_files_content(solution_tables, questions_tables, _(calculus_exercises_))
    solution.seek(0)
    questions.seek(0)

    return solution.read(), questions.read()


st.title(_(math_exercises_))

st.subheader(_(select_exercises_))

pb_selects = tuple(st.multiselect(_(exercises_list_), ALL_PROBLEMS_STR))
nb_eqs = st.slider(label=_(num_eqs_per_table_), min_value=1, max_value=20, value=10, step=1)

shuffle = st.checkbox( _(shuffle_problems_) )
if pb_selects:
    solution, questions = generate(pb_selects, nb_eqs, shuffle)
    if solution is not None:

        st.subheader(_(generate_code_))
        body = fr"""<form action="https://www.overleaf.com/docs" method="post" target="_blank">
        <div align="center">
    <input type="submit" value="{_(open_overleaf_)}">
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

