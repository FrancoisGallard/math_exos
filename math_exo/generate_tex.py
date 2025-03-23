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

import shutil
from io import StringIO
from random import choice
from typing import List

import latextable
from texttable import Texttable

from math_exo.base_problems import CalculusProblem


def latexify_table(lines, headers):
    table_quest = Texttable()

    if len(headers) == 1:
        align = ["p{17cm}"]
    elif len(headers) == 2:
        align = ["p{6.5cm}", "p{10.5cm}"]
    elif len(headers) == 3:
        align = ["p{6cm}", "p{8cm}", "p{3cm}"]
    else:
        raise ValueError("Table of size " + str(len(headers)) + " not supported.")
    table_quest.set_cols_align(align)
    table_quest.add_rows([headers] + lines)

    latex_quest = latextable.draw_latex(table_quest)
    latex_quest = latex_quest.replace(r"\begin{table}", "")
    latex_quest = latex_quest.replace(r"\end{table}", "")

    return latex_quest


def generate_table(problem: CalculusProblem | List[CalculusProblem], header, n_expr: int = 10, shuffle=False):
    lines_sol = []
    lines_question = []

    def _add_pb(pb):
        pretty_exprs = pb.pretty_print_eqs()
        lines_sol.append(pretty_exprs)
        line_quest = [pretty_exprs[0]] + [" "] * (len(header) - 1)
        lines_question.append(line_quest)

    if shuffle:
        for i in range(n_expr):
            _add_pb(choice(problem))
    else:
        for i in range(n_expr):
            _add_pb(problem)

    latex_sol = latexify_table(lines_sol, header)
    latex_quest = latexify_table(lines_question, header)
    return latex_sol, latex_quest


def generate_latex_files(solution_tables, questions_tables, title):
    solution_buf, questions_buf = generate_files_content(solution_tables, questions_tables, title)
    solution_file = open("solution.tex", 'w', encoding="utf8")
    questions_file = open("questions.tex", 'w', encoding="utf8")
    try:

        solution_buf.seek(0)
        shutil.copyfileobj(solution_buf, solution_file)
        questions_buf.seek(0)
        shutil.copyfileobj(questions_buf, questions_file)
    finally:
        solution_file.close()
        questions_file.close()


def generate_files_content(solution_tables, questions_tables, title):
    solution, questions = StringIO(), StringIO()

    for is_solution, outf in zip([True, False], [solution, questions]):

        outf.write(r"\documentclass[11pt,a4paper]{article}" + "\n")
        outf.write(r"\usepackage[margin=1cm, tmargin=1cm, textheight=20cm, vmargin=1.5cm]{geometry}" + "\n")
        outf.write(r"\usepackage[latin1, utf8]{inputenc}" + "\n")
        outf.write(r"\usepackage[french]{babel}" + "\n")
        outf.write(r"\usepackage{systeme}" + "\n")
        outf.write(r"\begin{document}" + "\n")
        outf.write(r"\date{}" + "\n")

        if is_solution:
            outf.write(r"\title{" + str(title) + " - Solution}\n")
        else:
            outf.write(r"\title{" + str(title) + "}\n")

        outf.write(r"\maketitle" + "\n")

        outf.write(r"{\renewcommand{\arraystretch}{2}" + "\n")
        if outf == solution:
            for tex_txt in solution_tables:
                outf.write(tex_txt)
                outf.write("\n")
        else:
            for tex_txt in questions_tables:
                outf.write(tex_txt)
                outf.write("\n")

        outf.write("}\n")
        outf.write(r"\end{document}" + "\n")

    return solution, questions
