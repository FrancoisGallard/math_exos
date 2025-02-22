from abc import abstractmethod
from random import randrange
from typing import List, Tuple

from sympy import Expr, Symbol, diff, latex
from sympy import expand, factor, rootof, GeneratorsNeeded
from sympy import oo
from math_exo.utils import pretty_print_eq, get_roots, variation_table

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

    def _generate(self) -> Tuple[Expr, Expr, List[Expr]]:
        expression = self._get_one_expr()
        if self.expand_expr:
            exp = expand(expression)
            fact = expression
        else:
            exp = expression
            fact = factor(exp)

        exp= latex(exp)+" = 0"
        roots = get_roots(fact, self.degree)
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

class FuncVariations(CalculusProblem):
    """Abstract functions variations"""
    degree = 1
    exercise = variations_
    header: List[str] = [function_, variations_]

    @abstractmethod
    def _get_one_expr(self) -> Expr:
        return

    def _generate(self) -> Tuple[Expr, str]:
        expression = self._get_one_expr()
        der = diff(expression, self.x)
        roots = get_roots(der, degree=self.degree-1, as_tex=False)

        def sign_of_der(x_val):
            val= der.evalf(subs={self.x: x_val})
            if val==0.:
                return "0"
            elif val>0:
                return "+"
            return "-"
        df_values=[latex(der.limit(self.x, -oo))]
        for i, r in enumerate(roots):
            if i==0:
                df_values.append(sign_of_der(roots[0] - 1.))

            df_values.append("0")

            if i==len(roots)-1:
                df_values.append(sign_of_der(roots[-1] + 1.))
        df_values .append(latex(der.limit(self.x, oo)))

        f_variations =[]
        for df in df_values:
            if df=="+":
                f_variations.append(r"\nearrow")
            elif df=="-":
                f_variations.append(r"\searrow")
            else:
                f_variations.append(" ")
        x_values=[r"-\infty"]
        max_values=[]
        for r in roots:
            max_values+=[" ", " "]
            max_values.append(latex(expression.subs(self.x, r)))
            x_values += [" ", latex(r)]
        max_values += [" ", " "]
        x_values += [" ", r"+\infty"]

        min_values=[latex(expression.limit(self.x, -oo))]
        min_values+=[" "]*(len(df_values)-2)
        min_values.append(latex(expression.limit(self.x, oo)))




        print("x_values", x_values, len(x_values))
        print("df_values", df_values, len(df_values))
        print("max_values", max_values, len(max_values))
        print("f_variations", f_variations, len(f_variations))
        print("min_values", min_values, len(min_values))
        variations = variation_table(x_values, df_values, max_values, f_variations, min_values)

        return expression, variations

    def pretty_print_eqs(self, equations=None):
        if equations is None:
            equations=self.generate()
        return [pretty_print_eq(equations[0]), equations[1]]

# print(variation_table(x_values=[r"-\infty", " ", "0", " ", r"+\infty"],
#                       df_values=["5", "+", "0", "-", "-10"],
#                       max_values=[" ", " ", "10", " ", " "],
#                       f_variations=[" ", r"\nearrow", " ", r"\searrow", " "],
#                       min_values=[r"-\infty", " ", " ", " ", r"+\infty"]))