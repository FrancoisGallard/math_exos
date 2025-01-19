# This is a sample Python script.
from typing import List, Tuple

import latextable
from sympy import Symbol, expand, factor, rootof
from random import randrange
from texttable import  Texttable
from sympy.polys.polyerrors import GeneratorsNeeded
from abc import  abstractmethod
from sympy import Expr

class CalculusProblem():
    equation:str="Equation"
    solution:str="Solution"
    racines:str="Racines"
    racine: str = "Racine"
    derivee:str="Dérivée"
    factorisation:str="Factorisation"
    header:List[str]=[equation, solution]
    degree=1
    section_name:str=""
    def __init__(self, min_coeff:int=-12, max_coeff:int=12):
        self.min_coeff:int=min_coeff
        self.max_coeff:int=max_coeff

    @abstractmethod
    def generate(self)->Tuple[Expr, Expr, List[Expr]]:
        """
        Expand expression
        Computes the roots
        returns the expanded expression, its factorization, its roots
        """
        return

class ExpandFactorFindRoots(CalculusProblem):
    header: List[str] = [CalculusProblem.equation, CalculusProblem.factorisation, CalculusProblem.racines]

    expand_expr:bool=True
    """Weather to expand or factorize the generated expression"""

    @abstractmethod
    def _get_one_expr(self)->Expr:
        return

    def generate(self)->Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        if self.expand_expr:
            exp=expand(expression)
            fact=expression
        else:
            exp=expression
            fact = factor(exp)

        roots = [rootof(fact, i) for i in range(self.degree)]
        return exp, fact, roots

class ExpandPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (ax)**2-b**2
    """
    degree=2
    expand_expr = False
    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff)*x)**2 - randrange(self.min_coeff,self.max_coeff)**2

class FactorPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (a*x+b)**2
    """
    degree = 2
    expand_expr = False
    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff)*x)**2 - randrange(self.min_coeff,self.max_coeff)**2

class FactorPolySum(ExpandFactorFindRoots):
    """
    (a*x+b)*(cx+d) + e*(fx+g)*(ax+b)
    """
    degree = 2
    expand_expr = False

    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        a=randrange(1, self.max_coeff)
        b,c,d,e,f,g=[randrange(self.min_coeff, self.max_coeff) for _ in range(6)]
        a_expr=a*x+b
        return a_expr*(c*x+d)+e*(f*x+g)*a_expr


def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)

class FactorEqsTwoLin(ExpandFactorFindRoots):
    """
    a*x+b = cx+d
    """
    degree = 1
    expand_expr = False
    def generate(self)->Tuple[Expr, Expr, List[Expr]]:
        x = Symbol('x')

        a,b,c,d=[sym_rand_int(self.max_coeff) for _ in range(4)]
        left=a*x + b
        right=c*x + d
        exp=f'{pretty_print_eq(left)} = {pretty_print_eq(right)}'
        exp_sol=left-right
        fact=factor(exp_sol)
        roots=rootof(exp_sol, 0)
        return exp, fact, roots


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


def pretty_print_eq(eq:str):
    eq_cln_exp=str(eq).replace("**","^").replace("*","")
    if eq_cln_exp.startswith("$"):
        return eq_cln_exp
    return "$"+eq_cln_exp+"$"

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

def retry_generate_tables(gen_func, n_expr):
    err = True
    while err:
        try:
            latex_sol, latex_quest = generate_table(gen_func, n_expr)
            err = False
        except GeneratorsNeeded:
            err = True
    return latex_sol, latex_quest

if __name__ == '__main__':

    solution_tables=[]
    questions_tables=[]

    problems=[ExpandPolyAX2MinB2(), FactorPolyAX2MinB2()]
    problems+=[ FactorEqsTwoLin(), FactorPolySum()]
    for problem in problems:
        latex_sol, latex_quest=retry_generate_tables(problem,n_expr=10)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title="Entrainement aux expressions remarquables"
    generate_latex_files(solution_tables,questions_tables,title)

