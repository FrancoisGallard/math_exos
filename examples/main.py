# BSD Zero Clause License
# Copyright (C) Francois Gallard
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH
# THE USE OR PERFORMANCE OF THIS SOFTWARE.

from math_exo.generate_tex import generate_latex_files, generate_table
from math_exo.problems import ALL_PROBLEMS, FactorEqsTwoLin, FactorPolySum, ProdTwoLins, \
    DiffPolyFlat, Diff2Polys1, DiffPolyExp, DiffPolyFrac, DiffPolyFracSqrt, DiffPolyFracSqrtInv, CanonicalPoly2, \
    DiffPolyFracDeg1, RationalFuncEq, LinearSystem2eqs, VarSecOrderPolyDeg3, VarSecOrderPolyDeg2, InequalitiesProd2Lin, \
    Inequalities2Lin, InequalitiesProd2LinK, InequalitiesDivLinK, VarFirstOrderPolyRatioSqrt

if __name__ == '__main__':

    solution_tables = []
    questions_tables = []

    problems = [FactorEqsTwoLin(), FactorPolySum(), ProdTwoLins()]
    problems += [DiffPolyFlat(), Diff2Polys1(), DiffPolyExp(), DiffPolyFrac(), DiffPolyFracSqrt()]
    problems += [DiffPolyFracDeg1(), DiffPolyFracSqrt(), DiffPolyFracSqrtInv()]
    problems+=[CanonicalPoly2(), RationalFuncEq(), LinearSystem2eqs(), InequalitiesProd2Lin()]
    problems+=[VarSecOrderPolyDeg3(),VarSecOrderPolyDeg2(), VarFirstOrderPolyRatioSqrt()]

    problems+=[InequalitiesDivLinK(),InequalitiesProd2LinK(), InequalitiesProd2Lin(), Inequalities2Lin()]

    for problem_class  in ALL_PROBLEMS :# problems
        problem=problem_class()
        latex_sol, latex_quest = generate_table(problem, [h["french"] for h in problem.header], n_expr=5)
        solution_tables.append(latex_sol)
        questions_tables.append(latex_quest)

    title = "Exercices de calcul littéral"
    generate_latex_files(solution_tables, questions_tables, title)
