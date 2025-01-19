# This is a sample Python script.
from typing import List, Tuple

from sympy import Symbol, expand, factor, rootof, GeneratorsNeeded
from random import randrange
from abc import  abstractmethod
from sympy import Expr
from math_exo.utils import pretty_print_eq

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

class ExpandPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (ax)**2-b**2
    """
    degree=2
    expand_expr = False
    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff)*x)**2 - randrange(self.min_coeff,self.max_coeff)**2

class FactorPolyAX2MinB2(ExpandFactorFindRoots):
    """
    (a*x+b)**2
    """
    degree = 2
    expand_expr = False
    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        return (randrange(1, self.max_coeff)*x)**2 - randrange(self.min_coeff,self.max_coeff)**2

class FactorPolySum(ExpandFactorFindRoots):
    """
    (a*x+b)*(cx+d) + e*(fx+g)*(ax+b)
    """
    degree = 2
    expand_expr = False

    def _get_one_expr(self)->Expr:
        x = Symbol('x')
        a=randrange(1, self.max_coeff)
        b,c,d,e,f,g=[randrange(self.min_coeff, self.max_coeff) for _ in range(6)]
        a_expr=a*x+b
        return a_expr*(c*x+d)+e*(f*x+g)*a_expr


class FactorEqsTwoLin(ExpandFactorFindRoots):
    """
    a*x+b = cx+d
    """
    degree = 1
    expand_expr = False
    def _generate(self)->Tuple[Expr, Expr, List[Expr]]:
        x = Symbol('x')

        a,b,c,d=[sym_rand_int(self.max_coeff) for _ in range(4)]
        left=a*x + b
        right=c*x + d
        exp=f'{pretty_print_eq(left)} = {pretty_print_eq(right)}'
        exp_sol=left-right
        fact=factor(exp_sol)
        roots=rootof(exp_sol, 0)
        return exp, fact, roots

