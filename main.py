# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sympy as sp
from sympy import Symbol, expand, factor, rootof
from random import randrange
import tabulate

import random

def expand_poly_aminbsq(min_coeff=1, max_coeff=12):

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

def generate_table(gen_func, n_expr, add_roots=True):
    table_sol = []
    table_question=[]
    for i in range(n_expr):
        exp, fact, roots = gen_func()
        line=[str(exp), str(fact)]
        if add_roots:
            line.append( str(roots))
        table_sol.append(line)
        table_question.append([str(exp), "                  ", "                   "])
    headers=["Factoriser", "Solution" ]
    if add_roots:
        headers.append("Racines")
    latex_sol=tabulate.tabulate(table_sol, headers=headers, tablefmt="latex_longtable",)
    latex_quest = tabulate.tabulate(table_question, headers=headers, tablefmt="latex_longtable")
    return latex_sol, latex_quest

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    latex_1sol,latex_1_quest= generate_table(expand_poly_aminbsq, 10, add_roots=True)
    latex_2sol, latex_2_quest = generate_table(expand_poly_apbsq, 10, add_roots=True)
    solution= open("solution.tex",'w')
    questions=open("questions.tex",'w')
    try:
        for outf in [solution, questions]:

            outf.write(r"\documentclass[11pt,twoside,a4paper]{article}"+"\n")
            outf.write(r"\usepackage{booktabs,siunitx}" + "\n")
            outf.write(r"\begin{document}"+"\n")
            outf.write(r"\title{Entrainement aux expressions remarquables}"+"\n")
            outf.write(r"\maketitle"+"\n")
            if outf==solution:
                outf.write(latex_1sol)
                outf.write(  "\n\n")
                outf.write(latex_2sol)
            else:
                outf.write(latex_1_quest)
                outf.write("\n\n")
                outf.write(latex_2_quest)
            outf.write(r"\end{document}"+"\n")
    finally:
        solution.close()
        questions.close()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
