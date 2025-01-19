# This is a sample Python script.
from math_exo.generate_tex import generate_latex_files, generate_table
from math_exo.problems import FactorPolyAX2MinB2, ExpandPolyAX2MinB2, FactorEqsTwoLin, FactorPolySum, ProdTwoLins, \
    DiffPolyFlat, Diff2Polys1, DiffPolyExp, DiffPolyFrac, DiffPolyFracSqrt, DiffPolyFracSqrtInv

if __name__ == '__main__':

    solution_tables=[]
    questions_tables=[]

    problems=[FactorPolyAX2MinB2(), ExpandPolyAX2MinB2()]
    problems+=[ FactorEqsTwoLin(), FactorPolySum(), ProdTwoLins()]
    problems=[DiffPolyFlat(), Diff2Polys1(), DiffPolyExp(), DiffPolyFrac(), DiffPolyFracSqrt()]
    problems = [ DiffPolyFracSqrt(), DiffPolyFracSqrtInv()]
    for problem in problems:
        latex_sol, latex_quest=generate_table(problem,n_expr=10)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title="Exercices de calcul littéral"
    generate_latex_files(solution_tables,questions_tables,title)

