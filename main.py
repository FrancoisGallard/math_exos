# This is a sample Python script.
import latextable
from sympy import Symbol, expand, factor, rootof
from random import randrange
from texttable import  Texttable
from sympy.polys.polyerrors import GeneratorsNeeded


def expand_poly_aminbsq(min_coeff=1, max_coeff=12):
    """
    Expand expression (ax)**2-b**2
    Computes the roots
    returns the expanded expression, its factorization, its roots
    """
    x = Symbol('x')
    exp=((randrange(1, max_coeff)*x)**2 - randrange(min_coeff,max_coeff)**2)
    fact=factor(exp )
    roots=[rootof(fact, 0), rootof(fact, 1)]
    return exp, fact, roots

def expand_poly_apbsq(min_coeff=-12, max_coeff=12):
    x = Symbol('x')
    fact=(randrange(min_coeff,max_coeff)*x  + randrange(min_coeff,max_coeff))**2
    exp=expand(fact )
    roots = [rootof(fact, 0), rootof(fact, 1)]
    return exp, fact, roots

def latexify_table(lines, headers):
    table_quest = Texttable()
    align=["p{5cm}","p{9cm}"]
    if len(headers)==3:
        align.append("p{3cm}")
    table_quest.set_cols_align(align)
    table_quest.add_rows([headers] + lines)

    latex_quest = latextable.draw_latex(table_quest)
    latex_quest=latex_quest.replace(r"\begin{table}","")
    latex_quest=latex_quest.replace(r"\end{table}", "")

    return latex_quest


def pretty_print_eq(eq):
    return "$"+str(eq).replace("**","^").replace("*","")+"$"
def generate_table(gen_func, n_expr, add_roots=True):
    lines_sol = []
    lines_question=[]

    for i in range(n_expr):
        exp, fact, roots = gen_func()
        line=[pretty_print_eq(exp), pretty_print_eq(fact)]
        if add_roots:
            line.append( pretty_print_eq(roots))
        lines_sol.append(line)
        lines_question.append([pretty_print_eq(exp), "                  ", "                   "])
    headers=["Factoriser", "Solution" ]
    if add_roots:
        headers.append("Racines")

    latex_sol=latexify_table( lines_sol, headers)
    latex_quest=latexify_table(lines_question, headers)
    return latex_sol, latex_quest

def generate_latex_files(latex_1sol,latex_1_quest, latex_2sol, latex_2_quest):
    solution = open("solution.tex", 'w')
    questions = open("questions.tex", 'w')
    try:
        for outf in [solution, questions]:

            outf.write(r"\documentclass[11pt,a4paper]{article}"+"\n")
            #outf.write(r"\usepackage{booktabs,siunitx}" + "\n")
            outf.write(r"\usepackage[margin=1cm, tmargin=0cm, textheight=27cm]{geometry}" + "\n")

            outf.write(r"\begin{document}"+"\n")
            outf.write(r"\date{}" + "\n")

            outf.write(r"\title{Entrainement aux expressions remarquables}"+"\n")
            outf.write(r"\maketitle"+"\n")

            outf.write(r"{\renewcommand{\arraystretch}{2}"+"\n")
            if outf==solution:
                outf.write(latex_1sol)
                outf.write(  "\n")
                outf.write(latex_2sol)
            else:
                outf.write(latex_1_quest)
                outf.write("\n")
                outf.write(latex_2_quest)

            outf.write("}\n")
            outf.write(r"\end{document}"+"\n")
    finally:
        solution.close()
        questions.close()


if __name__ == '__main__':
    err=True
    while err:
        try:
            latex_1sol,latex_1_quest= generate_table(expand_poly_aminbsq, 10, add_roots=True)
            latex_2sol, latex_2_quest = generate_table(expand_poly_apbsq, 10, add_roots=True)
            err=False
        except GeneratorsNeeded:
            err=True
    generate_latex_files(latex_1sol, latex_1_quest, latex_2sol, latex_2_quest)

