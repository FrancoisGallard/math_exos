from typing import List, Tuple

from sympy import Symbol,  factor, rootof
from random import randrange
from sympy import Expr

from math_exo.base_problems import ExpandFactorFindRoots, sym_rand_int
from math_exo.utils import pretty_print_eq


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

