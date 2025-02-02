from abc import abstractmethod
from random import randrange
from typing import List, Tuple

from sympy import Expr, Symbol, diff
from sympy import expand, factor, rootof, GeneratorsNeeded


def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)


class CalculusProblem():
    equation: str = "Equation"
    solutions: str = "Solutions"
    fonction: str = "Fonction"
    derivee: str = "Dérivée"
    factorisation: str = "Factorisation"
    developpement: str = "Développement"
    header: List[str] = [equation, solutions]
    degree = 1
    section_name: str = ""
    x = Symbol("x")
    y = Symbol("y")

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


class ExpandFactorFindRoots(CalculusProblem):
    header: List[str] = [CalculusProblem.equation, CalculusProblem.factorisation, CalculusProblem.solutions]

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
            return str(roots).replace("[", "\{").replace("]", "\}")
        return roots

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        if self.expand_expr:
            exp = expand(expression)
            fact = expression
        else:
            exp = expression
            fact = factor(exp)

        roots = self.get_roots(fact)
        return exp, fact, roots


class DifferentiationProblem(CalculusProblem):
    header: List[str] = [CalculusProblem.fonction, CalculusProblem.derivee]

    @abstractmethod
    def _get_one_expr(self) -> Expr:
        return

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        return expression, diff(expression, self.x)
