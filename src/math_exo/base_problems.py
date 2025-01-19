
from typing import List, Tuple

from sympy import  expand, factor, rootof, GeneratorsNeeded
from random import randrange
from abc import  abstractmethod
from sympy import Expr

def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)

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
    def _generate(self)->Tuple[Expr, Expr, List[Expr]]:
        return

    def generate(self)->Tuple[Expr, Expr, List[Expr]]:
        """
        Expand expression, handle random errors
        Computes the roots
        returns the expanded expression, its factorization, its roots
        """
        err = True
        while err:
            try:
                out=self._generate()
                err = False
            except GeneratorsNeeded:
                err = True
        return out

class ExpandFactorFindRoots(CalculusProblem):
    header: List[str] = [CalculusProblem.equation, CalculusProblem.factorisation, CalculusProblem.racines]

    expand_expr:bool=True
    """Weather to expand or factorize the generated expression"""

    @abstractmethod
    def _get_one_expr(self)->Expr:
        return

    def _generate(self)->Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        if self.expand_expr:
            exp=expand(expression)
            fact=expression
        else:
            exp=expression
            fact = factor(exp)

        roots = [rootof(fact, i) for i in range(self.degree)]
        return exp, fact, roots



