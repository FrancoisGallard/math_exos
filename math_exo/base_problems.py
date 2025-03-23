# MathExo project
# Copyright (C) 2025 Francois Gallard
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from abc import abstractmethod
from random import randrange
from typing import List, Tuple

from sympy import Expr, Symbol, diff, latex
from sympy import degree as get_degree
from sympy import expand, factor, GeneratorsNeeded
from sympy import oo
from sympy.core.mul import Mul
from sympy.logic.boolalg import BooleanTrue, BooleanFalse

from math_exo.internationalization import *
from math_exo.utils import pretty_print_eq, get_roots, variation_table


def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)


class CalculusProblem():
    """Abstract calculus problem"""
    header: List[Mapping] = [equation_, solutions_]
    exercise: Mapping[str, str] = solve_
    expr = ""
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
            equations = self.generate()
        return [pretty_print_eq(exp) for exp in equations]

    def _check_eq_sol(self, equation, solutions):
        if equation == BooleanTrue() or equation == BooleanFalse():
            raise GeneratorsNeeded()
        if solutions == BooleanTrue() or solutions == BooleanFalse():
            if solutions == BooleanTrue():
                solutions_str = r"$x \in {\rm I\!R}$"
            else:
                solutions_str = r"$x \in \O$"
        else:
            solutions_str = None
        return solutions_str


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

        exp = latex(exp) + " = 0"
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
    approx_f_root = False
    header: List[str] = [function_, variations_]

    @abstractmethod
    def _get_one_expr(self) -> Expr:
        return

    def _get_bounds_validity(self):
        return -oo, oo

    def _get_der_sign_expr(self, expr) -> Expr:
        return diff(expr, self.x)

    def _real_lim(self, expr: Expr, val: float):
        if not self.x in expr.free_symbols:
            return expr
        lim = expr.limit(self.x, val, dir="+")
        if isinstance(lim, Mul):  # -oo*I or +oo*I
            lim = expr.limit(self.x, val, dir="-")
        return lim

    def _generate(self) -> Tuple[Expr, str]:
        expression = self._get_one_expr()
        der = self._get_der_sign_expr(expression)

        l_b, u_b = self._get_bounds_validity()
        roots_m = get_roots(der, degree=get_degree(der, gen=self.x), as_tex=False, l_b=l_b, u_b=u_b)

        roots = []
        for r in roots_m:
            if r not in roots:
                roots.append(r)

        def sign_of_der(x_val):
            val = der.evalf(subs={self.x: x_val})
            if val == 0.:
                return "0"
            elif val > 0:
                return "+"
            return "-"

        df_values = [latex(self._real_lim(der, l_b))]
        for i, r in enumerate(roots):
            if i == 0:
                df_values.append(sign_of_der(roots[0] - 1.))

            df_values.append("0")

            if i == len(roots) - 1:
                df_values.append(sign_of_der(roots[-1] + 1.))
            else:
                df_values.append(sign_of_der((r + roots[i + 1]) / 2))
        if not len(roots):  # No roots, just get the constant sign of the derivative
            df_values.append(sign_of_der(0.))
        df_values.append(latex(self._real_lim(der, u_b)))

        f_variations = []
        max_values = []
        min_values = []
        f_values = [self._real_lim(expression, l_b)]
        if self.approx_f_root:
            f_values += [expression.evalf(n=3, subs={self.x: r}) for r in roots]
        else:
            f_values += [expression.subs(self.x, r) for r in roots]
        f_values += [self._real_lim(expression, u_b)]
        f_values_l = [latex(f) for f in f_values]
        p = 0
        for df in df_values:
            if df == "+":
                f_variations.append(r"\nearrow")
                min_values += [f_values_l[p], " "]
                max_values += [" ", " "]
                p += 1
            elif df == "-":
                f_variations.append(r"\searrow")
                max_values += [f_values_l[p], " "]
                min_values += [" ", " "]
                p += 1
            else:
                f_variations.append(" ")
        if df_values[-2] == "+":
            min_values.append(" ")
            max_values.append(f_values_l[p])
        else:
            max_values.append(" ")
            min_values.append(f_values_l[p])
        x_values = [latex(l_b)]
        for r in roots:
            x_values += [" ", latex(r)]
        x_values += [" ", latex(u_b)]

        variations = variation_table(x_values, df_values, max_values, f_variations, min_values)

        return expression, variations

    def pretty_print_eqs(self, equations=None):
        if equations is None:
            equations = self.generate()
        return [pretty_print_eq(equations[0]), equations[1]]
