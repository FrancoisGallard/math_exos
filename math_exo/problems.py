import random
from random import randint
from random import randrange
from typing import List, Tuple

import inspect
import sys

from sympy import Expr, expand, Integer, latex
from sympy import factor, sqrt, solve
from sympy.polys.specialpolys import random_poly

from math_exo.base_problems import CalculusProblem
from math_exo.base_problems import ExpandFactorFindRoots, sym_rand_int, DifferentiationProblem
from math_exo.utils import pretty_print_eq


class IdentiteRemarquableA2_B2(ExpandFactorFindRoots):
    """Factoriser et résoudre (a.x)²-b²=0"""
    EXERCICE_TYPE = "Factoriser et résoudre"
    degree = 2
    expand_expr = False
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.factorisation, ExpandFactorFindRoots.solutions]

    def _get_one_expr(self) -> Expr:
        x = self.x
        return (randrange(1, self.max_coeff) * x) ** 2 - randrange(self.min_coeff, self.max_coeff) ** 2


class IdentiteRemarquable(ExpandFactorFindRoots):
    """Développer (a.x+b)²"""
    EXERCICE_TYPE = "Développement"
    degree = 2
    expand_expr = True
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.developpement, ExpandFactorFindRoots.solutions]

    def _get_one_expr(self) -> Expr:
        x = self.x
        return (randrange(1, self.max_coeff) * x + randrange(self.min_coeff, self.max_coeff)) ** 2

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        exp = self._get_one_expr()
        expanded = expand(exp)
        roots = self.get_roots(exp)
        return exp, expanded, roots


class FactorPolySum(ExpandFactorFindRoots):
    """Factoriser et résoudre (a.x+b)(c.x+d) + e(fx+g)(a.x+b)=0"""
    EXERCICE_TYPE = "Factoriser et résoudre"
    degree = 2
    expand_expr = False

    def _get_one_expr(self) -> Expr:
        x = self.x
        a = randrange(1, self.max_coeff)
        b, c, d, e, f, g = [randrange(self.min_coeff, self.max_coeff) for _ in range(6)]
        a_expr = a * x + b
        return a_expr * (c * x + d) + e * (f * x + g) * a_expr


class FactorEqsTwoLin(ExpandFactorFindRoots):
    """Factoriser et résoudre a.x+b = c.x+d"""
    EXERCICE_TYPE = "Factoriser et résoudre"
    NAME = "a.x+b = c.x+d"
    degree = 1
    expand_expr = False

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        x = self.x

        a, b, c, d = [sym_rand_int(self.max_coeff) for _ in range(4)]
        left = a * x + b
        right = c * x + d
        exp = f'{pretty_print_eq(left)} = {pretty_print_eq(right)}'
        exp_sol = left - right
        fact = factor(exp_sol)
        roots = self.get_roots(exp_sol)
        return exp, fact, roots


class RationalFuncEq(ExpandFactorFindRoots):
    """Factoriser et résoudre (a.x+b)/(c.x+d)=k"""
    EXERCICE_TYPE = "Factoriser et résoudre"
    degree = 1
    header = [ExpandFactorFindRoots.equation, "Valeurs interdites", ExpandFactorFindRoots.solutions]

    def _generate(self) -> Tuple[Expr, Expr, Expr]:
        x = self.x
        c = Integer(randrange(1, self.max_coeff))
        a, b, d, k = [Integer(sym_rand_int(self.max_coeff)) for _ in range(4)]
        left = a * x + b
        right = c * x + d
        exp_sol = pretty_print_eq(left / right) + " = " + str(k)
        forbidden = -d / c
        root = (k * d - b) / (a - k * c)
        return exp_sol, forbidden, root


class ProdTwoLins(ExpandFactorFindRoots):
    """Résoudre (a.x+b) * (c.x+d) = 0 """
    EXERCICE_TYPE = "Résoudre"
    degree = 2
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.solutions]

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        x = self.x
        a = randrange(1, self.max_coeff)
        b, c, d = [sym_rand_int(self.max_coeff) for _ in range(3)]
        left = a * x + b
        right = c * x + d
        exp_sol = left * right
        roots = self.get_roots(exp_sol)
        return exp_sol, roots


class DiffPolyFlat(DifferentiationProblem):
    """d/dx (a.x**4 + b.x**3 + c.x**2 + d.x + e)"""
    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)


class Diff2Polys1(DifferentiationProblem):
    """d/dx (a.x**2 + b.x + c )*(d.x**3 + e.x**2 + f.x + g)"""
    def _get_one_expr(self) -> Expr:
        n = randint(1, 3)
        p1 = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        p2 = random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)
        return p1 * p2


class DiffPolyExp(DifferentiationProblem):
    """d/dx (a.x + b)**n"""
    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff) ** n


class DiffPolyFracDeg1(DifferentiationProblem):
    """d/dx (a.x**3 + b.x**2 + c.x + d )(e.x + f )"""
    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return (num / den)


class DiffPolyFrac(DifferentiationProblem):
    """d/dx (a.x**3 + b.x**2 + c.x +d )/(e.x + f)"""
    def _get_one_expr(self) -> Expr:
        n1 = randint(2, 3)
        num = random_poly(self.x, n1, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        p = randint(2, 9)
        return (num / den) ** p


class DiffPolyFracSqrt(DifferentiationProblem):
    """d/dx sqrt(a.x**3 + b.x**2 + c.x + d )"""
    def _get_one_expr(self) -> Expr:
        n1 = randint(2, 3)
        num = random_poly(self.x, n1, inf=self.min_coeff, sup=self.max_coeff)
        return sqrt(num)


class DiffPolyFracSqrtInv(DiffPolyFracSqrt):
    """d/dx sqrt(a.x**3 + b.x**2 + c.x +d ) ** (-1 ou 1)"""

    def _get_one_expr(self) -> Expr:
        expr = super(DiffPolyFracSqrtInv, self)._get_one_expr()
        pow_p = 1 if random.random() < 0.5 else -1
        return expr ** pow_p


class CanonicalPoly2(CalculusProblem):
    """Forme canonique de a.x²+b.x+c"""
    # => a (x-Alpha)²+Beta
    EXERCICE_TYPE = "Forme canonique"
    header = ["Polynome", "Forme canonique"]

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        a = Integer(randint(1, self.max_coeff))
        b = Integer(randint(self.min_coeff, self.max_coeff))
        c = Integer(randint(self.min_coeff, self.max_coeff))
        expr = a * self.x ** 2 + b * self.x + c
        alpha = -b / (2 * a)
        beta = c - b ** 2 / (4 * a)
        sol = a * (self.x - alpha) ** 2 + beta
        return expr, sol


class LinearSystem2eqs(CalculusProblem):
    """Résoudre {a.x+b.y = c ; d.x+e.y = f}"""

    header = ["Equations", "Solutions"]
    NAME = "2 équations linéaires"

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        a1, a2 = Integer(randint(1, self.max_coeff)), Integer(randint(1, self.max_coeff))
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(4)]
        x, y = self.x, self.y
        equations = [a1 * x + coeffs[0] * y + coeffs[1], a2 * x + coeffs[2] * y + coeffs[3]]
        try:
            sol = list(solve(equations, [x, y], set=True)[1])[0]
        except:
            sol = []

        lhs = [a1 * x + coeffs[0] * y, a2 * x + coeffs[2] * y]
        rhs = [-coeffs[1], -coeffs[3]]
        eq_str = r"$\systeme{%s = %s,%s = %s}$" % (latex(lhs[0]), rhs[0], latex(lhs[1]), rhs[1])

        if sol:
            sol_str = r"$[" + ",".join([latex(s) for s in sol]) + r"]$"
        else:
            sol_str = "Pas de solutions"
        return eq_str, sol_str


predicate = lambda x: inspect.isclass(x) and issubclass(x, CalculusProblem)
ALL_PROBLEMS = [i[1] for i in inspect.getmembers(sys.modules[__name__], predicate) if not i[1].__doc__.startswith("Abstract")]
ALL_PB_DOCS=[pb.__doc__ for pb in ALL_PROBLEMS]
ALL_PB_TYPES=set(pb.EXERCICE_TYPE for pb in ALL_PROBLEMS)
ALL_PROBLEMS_STR = sorted(ALL_PB_DOCS)
ALL_PROBLEMS_SORTED = [x for _, x in sorted(zip(ALL_PB_DOCS, ALL_PROBLEMS))]