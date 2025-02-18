from abc import abstractmethod
from random import randrange
from typing import List, Tuple

from sympy import Expr, Symbol, diff, latex
from sympy import expand, factor, rootof, GeneratorsNeeded

from math_exo.utils import pretty_print_eq

from math_exo.internationalization import *


def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)


class CalculusProblem():
    """Abstract calculus problem"""
    header: List[Mapping] = [equation_, solutions_]
    exercise:Mapping[str, str] = solve_
    expr=""
    degree = 1
    x = Symbol("x", real=True)
    y = Symbol("y", real=True)

    def __init__(self, min_coeff: int = -12, max_coeff: int = 12):
        self.min_coeff: int = min_coeff
        self.max_coeff: int = max_coeff

    @abstractmethod
    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        return

    def generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        """
        Expand expression, handle random errors
        Computes the roots
        returns the expanded expression, its factorization, its roots
        """
        err = True
        while err:
            try:
                out = self._generate()
                err = False
            except GeneratorsNeeded:
                err = True
        return out

    def pretty_print_eqs(self, equations=None):
        if equations is None:
            equations=self.generate()
        return [pretty_print_eq(exp) for exp in equations]


class ExpandFactorFindRoots(CalculusProblem):
    """Abstract expand find roots"""
    header: List[str] = [equation_, factorization_, solutions_]
    expand_expr: bool = True
    """Weather to expand or factorize the generated expression"""

    @abstractmethod
    def _get_one_expr(self) -> Expr:
        return

    def get_roots(self, expr, as_tex=True):
        roots = []
        for i in range(self.degree):
            try:
                root = rootof(expr, i)
                roots.append(root)
            except:
                pass
        if as_tex:
            return str(roots).replace("[", r"\{").replace("]", r"\}")
        return roots

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        if self.expand_expr:
            exp = expand(expression)
            fact = expression
        else:
            exp = expression
            fact = factor(exp)

        exp= latex(exp)+" = 0"
        roots = self.get_roots(fact)
        return exp, fact, roots


class DifferentiationProblem(CalculusProblem):
    """Abstract differenciation"""

    exercise = derivation_
    header: List[str] = [function_, derivative_]
    @abstractmethod
    def _get_one_expr(self) -> Expr:
        return

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        return expression, diff(expression, self.x)
