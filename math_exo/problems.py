from random import randint
from random import randrange
from typing import List, Tuple

import inspect
import sys

from sympy import Expr, expand, Integer, latex, diff
from sympy import factor, sqrt, solve, exp, oo
from sympy.polys.specialpolys import random_poly
from sympy.solvers.inequalities import reduce_rational_inequalities

from math_exo.base_problems import CalculusProblem, FuncVariations
from math_exo.base_problems import ExpandFactorFindRoots, sym_rand_int, DifferentiationProblem
from math_exo.utils import pretty_print_eq, get_roots

from math_exo.internationalization import *

class IdentiteRemarquableA2_B2(ExpandFactorFindRoots):

    expr = "(a.x)²-b²=0"
    exercise=factor_solve_

    degree = 2
    expand_expr = False

    def _get_one_expr(self) -> Expr:
        x = self.x
        return (randrange(1, self.max_coeff) * x) ** 2 - randrange(self.min_coeff, self.max_coeff) ** 2


class IdentiteRemarquable(ExpandFactorFindRoots):
    expr = "(a.x+b)²"
    exercise = expand_
    degree = 2
    expand_expr = True
    header = [equation_, expansion_, solutions_]

    def _get_one_expr(self) -> Expr:
        x = self.x
        return (randrange(1, self.max_coeff) * x + randrange(self.min_coeff, self.max_coeff)) ** 2

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        exp = self._get_one_expr()
        expanded = expand(exp)
        roots = get_roots(exp, self.degree)
        return exp, expanded, roots


class FactorPolySum(ExpandFactorFindRoots):
    expr = "(a.x+b)(c.x+d) + e(fx+g)(a.x+b)=0"
    exercise = factor_solve_
    degree = 2
    expand_expr = False

    def _get_one_expr(self) -> Expr:
        x = self.x
        a = randrange(1, self.max_coeff)
        b, c, d, e, f, g = [randrange(self.min_coeff, self.max_coeff) for _ in range(6)]
        a_expr = a * x + b
        return a_expr * (c * x + d) + e * (f * x + g) * a_expr


class FactorEqsTwoLin(ExpandFactorFindRoots):
    expr = "a.x+b = c.x+d"
    exercise = factor_solve_
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
        roots = get_roots(exp_sol, self.degree)
        return exp, fact, roots


class RationalFuncEq(ExpandFactorFindRoots):
    expr = "(a.x+b)/(c.x+d)=k"
    exercise = factor_solve_
    degree = 1
    header = [equation_, forbidden_values_,  solutions_]
    

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
    expr = "(a.x+b) * (c.x+d) = 0 "
    exercise = expand_solve_
    degree = 2
    header = [equation_, solutions_]

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        x = self.x
        a = randrange(1, self.max_coeff)
        b, c, d = [sym_rand_int(self.max_coeff) for _ in range(3)]
        left = a * x + b
        right = c * x + d
        exp_sol = left * right
        roots = get_roots(exp_sol, self.degree)
        exp_txt=latex(exp_sol)+" = 0"
        return exp_txt, roots


class DiffPolyFlat(DifferentiationProblem):
    expr= "(a.x**4 + b.x**3 + c.x**2 + d.x + e)"
    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)


class Diff2Polys1(DifferentiationProblem):
    expr="(a.x**2 + b.x + c )*(d.x**3 + e.x**2 + f.x + g)"
    def _get_one_expr(self) -> Expr:
        n = randint(1, 3)
        p1 = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        p2 = random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)
        return p1 * p2


class DiffPolyExp(DifferentiationProblem):
    expr="(a.x + b)**n"
    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff) ** n


class DiffPolyFracDeg1(DifferentiationProblem):
    expr="(a.x**3 + b.x**2 + c.x + d )(e.x + f )"
    

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 3, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return (num / den)

class DiffPolyFrac(DifferentiationProblem):
    expr="(a.x**2 + b.x + c )/(e.x + f)**p"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        p = randint(2, 9)

        return num / (den**p)

class DiffPolyFrac2(DifferentiationProblem):
    expr="(a.x + b )**p/(c.x**2+ d.x + e)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)

        p = randint(2, 9)
        return num**p / den

class DiffPolyFracSqrt(DifferentiationProblem):
    expr="sqrt(a.x**3 + b.x**2 + c.x + d )"

    def _get_one_expr(self) -> Expr:
        n1 = randint(2, 3)
        num = random_poly(self.x, n1, inf=self.min_coeff, sup=self.max_coeff)
        return sqrt(num)

class DiffPolyFracSqrtInv(DifferentiationProblem):
    expr="1/sqrt(a.x + b)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)
        return 1/sqrt(num)


class DiffPolySqrt(DifferentiationProblem):
    expr="sqrt(x)*(a.x**2+ b.x + c)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)

        return sqrt(self.x)*num

class DiffPolySqrtPoly(DifferentiationProblem):
    expr="sqrt(a.x+b)*(c.x**2+ d.x + e)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        sqp = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return sqrt(sqp)*num

class DiffPolySqrtPoly3(DifferentiationProblem):
    expr="sqrt(a.x+b)*(c.x**3+ d.x**2 + e.x + f)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 3, inf=self.min_coeff, sup=self.max_coeff)
        sqp = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return sqrt(sqp)*num


class DiffPolyExpPoly(DifferentiationProblem):
    expr = "exp(a.x+b)*(c.x**2+ d.x + e)"

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        sqp = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return exp(sqp) * num

class CanonicalPoly2(CalculusProblem):
    expr="a.x²+b.x+c"
    exercise=canonical_
    header = [polynomial_, canonical_]

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
    expr="{a.x+b.y = c ; d.x+e.y = f}"
    exercise=solve_

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

class Inequalities2Lin(CalculusProblem):
    expr = "a.x + b <= c.x + d"
    exercise = solve_

    def _generate(self) -> Tuple[str, str]:
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(4)]
        if coeffs[0]==coeffs[2]:
            coeffs[0]+=1
        left = coeffs[0]*self.x + coeffs[1]
        right = coeffs[2]*self.x + coeffs[3]
        equation= left <= right
        solutions=reduce_rational_inequalities([[equation]], self.x)
        solutions_str = self._check_eq_sol(equation, solutions)
        if solutions_str is None:
            solutions_str="$ "+latex(solutions)+" $"
            equation_str = "$ "+latex(left)+r" \leq "+latex(right)+" $"
        return equation_str, solutions_str

class InequalitiesProd2Lin(CalculusProblem):
    expr = "(a.x + b)(c.x + d) <= | >= 0"
    exercise = solve_

    def _generate(self) -> Tuple[str, str]:
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(4)]
        if coeffs[0]==coeffs[2]==0:
            coeffs[0]+=1
        left = coeffs[0]*self.x + coeffs[1]
        right = coeffs[2]*self.x + coeffs[3]
        sign = randint(0, 1)
        if sign:
            equation = left * right <= 0
        else:
            equation = left * right >= 0

        solutions = reduce_rational_inequalities([[equation]], self.x)

        solutions_str= self._check_eq_sol(equation, solutions)
        if solutions_str is None:
            solutions_str ="$ "+latex(solutions)+" $"
            solutions_str=solutions_str.replace(r"\wedge", "$ et $").replace(r"\vee", "$ ou $")
        equation_str = "$ "+latex(equation)+r" $"

        return equation_str, solutions_str

class InequalitiesProd2LinK(CalculusProblem):
    expr = "(a.x + b)(c.x + d) <= | >= k"
    exercise = solve_

    def _generate(self) -> Tuple[str, str]:
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(5)]
        if coeffs[0]==coeffs[2]==0:
            coeffs[0]+=1

        left = coeffs[0]*self.x + coeffs[1]
        right = coeffs[2]*self.x + coeffs[3]
        sign = randint(0, 1)
        if sign:
            equation= left * right <= coeffs[4]
        else:
            equation = left * right >= coeffs[4]

        solutions = reduce_rational_inequalities([[equation]], self.x)
        solutions_str = self._check_eq_sol(equation, solutions)
        equation_str = "$ " + latex(equation) + r" $"
        if solutions_str is None:
            solutions_str ="$ "+latex(solutions)+" $"
            solutions_str=solutions_str.replace(r"\wedge", "$ et $").replace(r"\vee", "$ ou $")

        return equation_str, solutions_str

class InequalitiesDivLinK(CalculusProblem):
    expr = "(a.x + b)/(c.x + d) <= | >= k"
    exercise = solve_

    def _generate(self) -> Tuple[str, str]:
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(5)]
        if coeffs[0]==coeffs[2]==0:
            coeffs[0]+=1

        left = coeffs[0]*self.x + coeffs[1]
        right = coeffs[2]*self.x + coeffs[3]
        sign = randint(0, 1)
        if sign:
            equation= left / right <= coeffs[4]
        else:
            equation = left / right >= coeffs[4]
        solutions=reduce_rational_inequalities([[equation]], self.x)

        solutions_str = self._check_eq_sol(equation, solutions)
        if solutions_str is None:
            solutions_str ="$ "+latex(solutions)+" $"
            solutions_str=solutions_str.replace(r"\wedge", "$ et $").replace(r"\vee", "$ ou $")
        equation_str = "$ "+latex(equation)+r" $"

        return equation_str, solutions_str

class VarSecOrderPolyDeg2(FuncVariations):
    expr = "(a.x² + bx + c)"
    degree = 2
    approx_f_root = False
    def _get_one_expr(self):
        return random_poly(self.x, self.degree, inf=self.min_coeff, sup=self.max_coeff)

class VarSecOrderPolyDeg3(FuncVariations):
    expr = "(a.x**3 + bx² + c.x +d)"
    degree = 3
    approx_f_root = True
    def _get_one_expr(self):
        return random_poly(self.x, self.degree, inf=self.min_coeff, sup=self.max_coeff)

class VarFirstOrderPolyRatioSqrt(FuncVariations):
    expr = "(a.x + b)/sqrt(c.x + d)"
    degree = 1
    approx_f_root = True

    def _get_bounds_validity(self):
        if self.c>0:
            return -self.d/self.c, oo
        return -oo, -self.d / self.c

    def _get_der_sign_expr(self, expr)->Expr:
        # d/dx = (a.c.x+2 a. d - b.c) / 2(c.x+d)**2/3
        return self.a*self.c*self.x+2*self.a*self.d-self.b*self.c

    def _get_one_expr(self):
        self.a, self.b, self.c, self.d = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(4)]
        if self.a ==0:
            self.a=2
        if self.c ==0:
            self.c=5
        if self.a/self.c == self.b/self.d :# Expr degenerates in sqrt(a/c.x+b/d)
            self.b+=1
        self.num = self.a*self.x + self.b
        self.den = self.c*self.x + self.d
        return self.num/sqrt(self.den)

predicate = lambda x: inspect.isclass(x) and issubclass(x, CalculusProblem)
ALL_PROBLEMS = [i[1] for i in inspect.getmembers(sys.modules[__name__], predicate) if i[1].expr]
