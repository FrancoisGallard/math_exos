from random import randrange
from typing import List, Tuple

from sympy import Expr, expand
from sympy import Symbol, factor, rootof

from math_exo.base_problems import ExpandFactorFindRoots, sym_rand_int
from math_exo.utils import pretty_print_eq


class FactorPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (ax)**2-b**2
    """
    degree = 2
    expand_expr = False
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.factorisation, ExpandFactorFindRoots.racines]

    def _get_one_expr(self) -> Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff) * x) ** 2 - randrange(self.min_coeff, self.max_coeff) ** 2


class ExpandPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (a*x+b)**2
    """
    degree = 2
    expand_expr = True
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.developpement, ExpandFactorFindRoots.racines]

    def _get_one_expr(self) -> Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff) * x+ randrange(self.min_coeff, self.max_coeff)) ** 2

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        exp = self._get_one_expr()
        expanded=expand(exp)
        roots = self.get_roots(exp)
        return exp, expanded, roots

class FactorPolySum(ExpandFactorFindRoots):
    """
    (a*x+b)*(cx+d) + e*(fx+g)*(ax+b)
    """
    degree = 2
    expand_expr = False

    def _get_one_expr(self) -> Expr:
        x = Symbol('x')
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
        x = Symbol('x')

        a, b, c, d = [sym_rand_int(self.max_coeff) for _ in range(4)]
        left = a * x + b
        right = c * x + d
        exp = f'{pretty_print_eq(left)} = {pretty_print_eq(right)}'
        exp_sol = left - right
        fact = factor(exp_sol)
        roots = self.get_roots( exp_sol)
        return exp, fact, roots


class ProdTwoLins(ExpandFactorFindRoots):
    """
    (a*x+b) * (cx+d)=0
    """
    degree = 2
    header = [ExpandFactorFindRoots.equation, ExpandFactorFindRoots.racines]

    def _generate(self) -> Tuple[Expr, List[Expr]]:
        x = Symbol('x')
        a = randrange(1, self.max_coeff)
        b, c, d = [sym_rand_int(self.max_coeff) for _ in range(3)]
        left = a * x + b
        right = c * x + d
        exp_sol = left * right
        exp = f'{exp_sol} = 0'
        roots = self.get_roots(exp_sol)
        return exp, roots
