import random
from random import randint
from random import randrange
from typing import List, Tuple

from sympy import Expr, expand, Integer, latex
from sympy import factor, sqrt, solve
from sympy.polys.specialpolys import random_poly

from math_exo.base_problems import CalculusProblem
from math_exo.base_problems import ExpandFactorFindRoots, sym_rand_int, DifferentiationProblem
from math_exo.utils import pretty_print_eq


class FactorPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (ax)**2-b**2
    """
    degree = 2
    expand_expr = False
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.factorisation, ExpandFactorFindRoots.solutions]

    def _get_one_expr(self) -> Expr:
        x = self.x
        return (randrange(1, self.max_coeff) * x) ** 2 - randrange(self.min_coeff, self.max_coeff) ** 2


class ExpandPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (a*x+b)**2
    """
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
    """
    (a*x+b)*(cx+d) + e*(fx+g)*(ax+b)
    """
    degree = 2
    expand_expr = False

    def _get_one_expr(self) -> Expr:
        x = self.x
        a = randrange(1, self.max_coeff)
        b, c, d, e, f, g = [randrange(self.min_coeff, self.max_coeff) for _ in range(6)]
        a_expr = a * x + b
        return a_expr * (c * x + d) + e * (f * x + g) * a_expr


class FactorEqsTwoLin(ExpandFactorFindRoots):
    """
    a*x+b = cx+d
    """
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
    """
    (ax+b)/(cx+d)=k
    ax+b=kcx+kd
    (a-kc)x=kd-b
    x=(kd-b)/(a-kc)
    """
    degree = 1
    header = [ExpandFactorFindRoots.equation, "Valeurs interdites", ExpandFactorFindRoots.solutions]

    def _generate(self) -> Tuple[Expr,Expr,Expr]:
        x = self.x
        c = Integer(randrange(1, self.max_coeff))
        a, b, d, k = [Integer(sym_rand_int(self.max_coeff)) for _ in range(4)]
        left = a * x + b
        right = c * x + d
        exp_sol = pretty_print_eq(left / right) +" = "+str(k)
        forbidden = -d/c
        root = (k*d-b)/(a-k*c)
        return exp_sol, forbidden, root

class ProdTwoLins(ExpandFactorFindRoots):
    """
    (a*x+b) * (cx+d)=0
    """
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
    """d/dx(ax**4 + bx**3 + cx**2 + dx + e)"""

    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)


class Diff2Polys1(DifferentiationProblem):
    """d/dx(ax**2 + bx + c )*(a2x**3 + b2x**2 + c2x + d2)"""

    def _get_one_expr(self) -> Expr:
        n = randint(1, 3)
        p1 = random_poly(self.x, 2, inf=self.min_coeff, sup=self.max_coeff)
        p2 = random_poly(self.x, n, inf=self.min_coeff, sup=self.max_coeff)
        return p1 * p2


class DiffPolyExp(DifferentiationProblem):
    """d/dx(ax+b )**n"""

    def _get_one_expr(self) -> Expr:
        n = randint(2, 5)
        return random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff) ** n


class DiffPolyFracDeg1(DifferentiationProblem):
    """d/dx(ax**3 + bx**2 + cx +d )*(a2x + b )"""

    def _get_one_expr(self) -> Expr:
        num = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        return (num / den)


class DiffPolyFrac(DifferentiationProblem):
    """d/dx(ax**3 + bx**2 + cx +d )*(a2x + b )"""

    def _get_one_expr(self) -> Expr:
        n1 = randint(2, 3)
        num = random_poly(self.x, n1, inf=self.min_coeff, sup=self.max_coeff)
        den = random_poly(self.x, 1, inf=self.min_coeff, sup=self.max_coeff)

        p = randint(2, 9)
        return (num / den) ** p


class DiffPolyFracSqrt(DifferentiationProblem):
    """d/dx sqrt(ax**3 + bx**2 + cx +d ) """

    def _get_one_expr(self) -> Expr:
        n1 = randint(2, 3)
        num = random_poly(self.x, n1, inf=self.min_coeff, sup=self.max_coeff)
        return sqrt(num)


class DiffPolyFracSqrtInv(DiffPolyFracSqrt):
    """d/dx sqrt(ax**3 + bx**2 + cx +d ) **(-1 or 1)"""

    def _get_one_expr(self) -> Expr:
        expr = super(DiffPolyFracSqrtInv, self)._get_one_expr()
        pow_p = 1 if random.random() < 0.5 else -1
        return expr ** pow_p

class CanonicalPoly2(CalculusProblem):
    """a.x²+bx+c => a (x-Alpha)²+Beta"""

    header = ["Polynome", "Forme canonique"]
    def _generate(self) ->Tuple[Expr, List[Expr]]:
        a= Integer(randint(1, self.max_coeff))
        b = Integer(randint(self.min_coeff, self.max_coeff))
        c = Integer(randint(self.min_coeff, self.max_coeff))
        expr=a*self.x**2+b*self.x+c
        alpha=-b/(2*a)
        beta=c-b**2/(4*a)
        sol=a*(self.x-alpha)**2+beta
        return expr, sol

class LinearSystem2eqs(CalculusProblem):
    """
    a.x+b.y = c
    d.x+e.y = f
    """

    header = ["Equations", "Solutions"]

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        a1,a2 =  Integer(randint(1, self.max_coeff)),Integer(randint(1, self.max_coeff))
        coeffs = [Integer(randint(self.min_coeff, self.max_coeff)) for _ in range(4)]
        x, y=self.x, self.y
        equations = [a1*x+coeffs[0]*y+coeffs[1],a2*x+coeffs[2]*y+coeffs[3]]
        try:
            sol = list(solve(equations, [x, y], set=True)[1])[0]
        except:
            sol=[]

        lhs=[a1*x+coeffs[0]*y ,a2*x+coeffs[2]*y ]
        rhs=[-coeffs[1], -coeffs[3]]
        eq_str=r"$\systeme{%s = %s,%s = %s}$"%(latex(lhs[0]), rhs[0],latex(lhs[1]),rhs[1])

        if sol:
            sol_str=r"$["+ ",".join([latex(s) for s in sol])+r"]$"
        else:
            sol_str="Pas de solutions"
        return eq_str, sol_str


ALL_PROBLEMS = [FactorPolyAX2MinB2, ExpandPolyAX2MinB2]
ALL_PROBLEMS += [FactorEqsTwoLin, FactorPolySum, ProdTwoLins]
ALL_PROBLEMS += [DiffPolyFlat, Diff2Polys1, DiffPolyExp, DiffPolyFrac, DiffPolyFracSqrt]
ALL_PROBLEMS += [DiffPolyFracDeg1, DiffPolyFracSqrt, DiffPolyFracSqrtInv]
ALL_PROBLEMS+=[CanonicalPoly2, RationalFuncEq, LinearSystem2eqs]