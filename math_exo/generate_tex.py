import shutil
from io import StringIO

import latextable
from texttable import Texttable

from math_exo.base_problems import CalculusProblem
from math_exo.utils import pretty_print_eq


def latexify_table(lines, headers):
    table_quest = Texttable()

    if len(headers) == 1:
        align = ["p{17cm}"]
    elif len(headers) == 2:
        align = ["p{8cm}", "p{9cm}"]
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


def generate_table(problem: CalculusProblem, n_expr: int = 10):
    lines_sol = []
    lines_question = []

    for i in range(n_expr):
        out_exprs = problem.generate()
        pretty_exprs = [pretty_print_eq(exp) for exp in out_exprs]
        lines_sol.append(pretty_exprs)

        line_quest = [pretty_exprs[0]] + [" "] * (len(problem.header) - 1)
        lines_question.append(line_quest)

    latex_sol = latexify_table(lines_sol, problem.header)
    latex_quest = latexify_table(lines_question, problem.header)
    return latex_sol, latex_quest


def generate_latex_files(solution_tables, questions_tables, title):
    solution_buf, questions_buf = generate_files_content(solution_tables, questions_tables, title)
    solution_file = open("solution.tex", 'w')
    questions_file = open("questions.tex", 'w')
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

    for is_solution, outf in zip([True, False],[solution, questions]):

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
