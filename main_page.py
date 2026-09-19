# MathExo project
# Copyright (C) 2025 Francois Gallard
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from html import escape
from itertools import groupby

import streamlit as st

from math_exo.generate_tex import generate_files_content, generate_table
from math_exo.internationalization import *
from math_exo.problems import ALL_PROBLEMS
from math_exo.theme import apply_theme, render_frieze

st.set_page_config(page_title="Exercices de mathématiques")

# The names Overleaf gives the two files of the project it creates
PROBLEM_FILE = "problem.tex"
SOLUTION_FILE = "solution.tex"

apply_theme()

language = st.selectbox("Language", ALL_LANGUAGES, ALL_LANGUAGES.index("french"))


def _(to_translate):
    if isinstance(to_translate, dict):
        return to_translate[language]
    return to_translate


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


@st.cache_data
def list_pbs(language):
    docs = [_(pb.exercise) + " " + _(pb.expr) for pb in ALL_PROBLEMS]
    pb_str = sorted(docs)
    pb_sort = [pb for _, pb in sorted(zip(docs, ALL_PROBLEMS), key=lambda item: item[0])]
    return docs, pb_str, pb_sort


ALL_PB_DOCS, ALL_PROBLEMS_STR, ALL_PROBLEMS_SORTED = list_pbs(language)
ALL_PROBLEMS_TYPES = [_(pb.exercise) for pb in ALL_PROBLEMS_SORTED]
ALL_TYPES = sorted(set(ALL_PROBLEMS_TYPES))


def get_pb_classes(problems_select):
    return [ALL_PROBLEMS_SORTED[ALL_PROBLEMS_STR.index(pb)] for pb in problems_select]


@st.cache_data
def generate(problems_select, n_expr, shuffle=False):
    classes = get_pb_classes(problems_select)
    problems = [pb() for pb in classes]
    solution_tables = []
    questions_tables = []
    if shuffle:
        headers = [tuple(_(h) for h in pb.header) for pb in problems]
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
render_frieze()

st.subheader(_(select_exercises_))

types_select = st.pills(_(filter_by_type_), ALL_TYPES, selection_mode="multi")
if types_select:
    shown_problems = [pb for pb, pb_type in zip(ALL_PROBLEMS_STR, ALL_PROBLEMS_TYPES)
                      if pb_type in types_select]
else:  # No type picked, the filter is off and every exercise stays available
    shown_problems = ALL_PROBLEMS_STR

pb_selects = tuple(st.multiselect(_(exercises_list_), shown_problems))
nb_eqs = st.slider(label=_(num_eqs_per_table_), min_value=1, max_value=20, value=10, step=1)

shuffle = st.checkbox(_(shuffle_problems_))
if pb_selects:
    solution, questions = generate(pb_selects, nb_eqs, shuffle)
    if solution is not None:
        st.subheader(_(generate_code_))
        # snip[] carries the two documents and snip_name[] their names, paired
        # in the order the fields appear. Without the names Overleaf calls them
        # Untitled.tex and Untitled (1).tex. main_document opens the exercise
        # sheet rather than its solution.
        # The sources hold & and <, which have to be escaped to survive the
        # textarea; the browser hands the original text back on submit.
        body = f"""<form action="https://www.overleaf.com/docs" method="post" target="_blank">
    <div align="center">
        <input type="submit" value="{escape(_(open_overleaf_))}">
    </div>
    <input type="hidden" name="snip_name[]" value="{PROBLEM_FILE}">
    <input type="hidden" name="snip_name[]" value="{SOLUTION_FILE}">
    <input type="hidden" name="main_document" value="{PROBLEM_FILE}">
    <textarea rows="8" cols="120" name="snip[]">{escape(questions)}</textarea>
    <textarea rows="8" cols="120" name="snip[]">{escape(solution)}</textarea>
</form>
"""
        st.html(body)
