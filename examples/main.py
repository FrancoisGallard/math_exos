# This is a sample Python script.
from math_exo.generate_tex import generate_latex_files, generate_table
from math_exo.problems import FactorEqsTwoLin, FactorPolySum, ProdTwoLins, \
    DiffPolyFlat, Diff2Polys1, DiffPolyExp, DiffPolyFrac, DiffPolyFracSqrt, DiffPolyFracSqrtInv, CanonicalPoly2, \
    DiffPolyFracDeg1, RationalFuncEq, LinearSystem2eqs, ExpandFactorFindRoots, VarSecOrderPolyDeg3, VarSecOrderPolyDeg2

if __name__ == '__main__':

    solution_tables = []
    questions_tables = []

    problems = [ExpandFactorFindRoots() ]
    problems += [FactorEqsTwoLin(), FactorPolySum(), ProdTwoLins()]
    problems += [DiffPolyFlat(), Diff2Polys1(), DiffPolyExp(), DiffPolyFrac(), DiffPolyFracSqrt()]
    problems += [DiffPolyFracDeg1(), DiffPolyFracSqrt(), DiffPolyFracSqrtInv()]
    problems+=[CanonicalPoly2(), RationalFuncEq(), LinearSystem2eqs(), VarSecOrderPolyDeg3(),VarSecOrderPolyDeg2()]
    problems=[VarSecOrderPolyDeg2()]
    for problem in problems:
        latex_sol, latex_quest = generate_table(problem, [h["french"] for h in problem.header], n_expr=5)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title = "Exercices de calcul littéral"
    generate_latex_files(solution_tables, questions_tables, title)
