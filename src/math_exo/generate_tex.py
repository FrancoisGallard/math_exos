import latextable
from texttable import  Texttable

from math_exo.base_problems import CalculusProblem
from math_exo.utils import pretty_print_eq

def latexify_table(lines, headers):
    table_quest = Texttable()
    align=["p{6cm}","p{8cm}"]
    if len(headers)==3:
        align.append("p{3cm}")
    table_quest.set_cols_align(align)
    table_quest.add_rows([headers] + lines)

    latex_quest = latextable.draw_latex(table_quest)
    latex_quest=latex_quest.replace(r"\begin{table}","")
    latex_quest=latex_quest.replace(r"\end{table}", "")

    return latex_quest


def generate_table(problem:CalculusProblem, n_expr:int=10):
    lines_sol = []
    lines_question=[]

    for i in range(n_expr):
        out_exprs = problem.generate()
        pretty_exprs=[pretty_print_eq(exp) for exp in out_exprs]
        lines_sol.append(pretty_exprs)

        line_quest=[pretty_exprs[0]]+[" "]*(len(problem.header)-1)
        lines_question.append(line_quest)

    latex_sol=latexify_table( lines_sol, problem.header)
    latex_quest=latexify_table(lines_question, problem.header)
    return latex_sol, latex_quest

def generate_latex_files(solution_tables,questions_tables, title):
    solution = open("solution.tex", 'w')
    questions = open("questions.tex", 'w')
    try:
        for outf in [solution, questions]:

            outf.write(r"\documentclass[11pt,a4paper]{article}"+"\n")
            #outf.write(r"\usepackage{booktabs,siunitx}" + "\n")
            outf.write(r"\usepackage[margin=1cm, tmargin=0cm, textheight=27cm]{geometry}" + "\n")

            outf.write(r"\begin{document}"+"\n")
            outf.write(r"\date{}" + "\n")

            outf.write(r"\title{"+str(title)+"}"+"\n")
            outf.write(r"\maketitle"+"\n")

            outf.write(r"{\renewcommand{\arraystretch}{2}"+"\n")
            if outf==solution:
                for tex_txt in solution_tables:
                    outf.write(tex_txt)
                    outf.write(  "\n")
            else:
                for tex_txt in questions_tables:
                    outf.write(tex_txt)
                    outf.write("\n")

            outf.write("}\n")
            outf.write(r"\end{document}"+"\n")
    finally:
        solution.close()
        questions.close()




