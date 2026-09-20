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
from math_exo.utils import pretty_print_eq, get_roots, to_single_fraction, variation_table


def sym_rand_int(max_coeff):
    return randrange(-max_coeff, max_coeff)


MAX_DRAWS = 200
"""How many times a problem redraws its coefficients before giving up"""


class CalculusProblem():
    """Abstract calculus problem"""
    header: List[Mapping] = [equation_, solutions_]
    col_widths: List[str] = []
    """Table column widths, empty to let latexify_table pick them from the header"""
    exercise: Mapping[str, str] = solve_
    expr = ""
    degree = 1
    x = Symbol("x", real=True)
    y = Symbol("y", real=True)

    def __init__(self, min_coeff: int = -12, max_coeff: int = 12,
                 language: str = "french"):
        # Several problems draw a leading coefficient from randrange(1, max_coeff)
        # and redraw until their constraints hold. Below 2 that range is empty,
        # and a range barely wider makes constraints such as "this coefficient
        # must be neither 0 nor the opposite of that one" impossible to satisfy,
        # which would spin for ever. Say so here rather than there.
        if max_coeff < 2 or min_coeff >= max_coeff:
            raise ValueError(
                "coefficients need room: max_coeff must be 2 or more and above "
                f"min_coeff, got min_coeff={min_coeff}, max_coeff={max_coeff}"
            )
        self.min_coeff: int = min_coeff
        self.max_coeff: int = max_coeff
        self.language: str = language

    def _translate(self, to_translate: Mapping[str, str]) -> str:
        """Pick the wording of the language this problem was built for.

        The header and the title are translated by the page, but a few answers
        carry words of their own, and those are built here.

        Args:
            to_translate: The mapping of a term over the languages.

        Returns:
            The term in the language of this problem.
        """
        return to_translate[self.language]

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
                solutions_str = r"$x \in \mathbb{R}$"
            else:
                # \O is the Danish letter and is invalid in math mode
                solutions_str = r"$x \in \emptyset$"
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

    def _generate(self) -> Tuple[Expr, Expr]:
        expression = self._get_one_expr()
        return expression, to_single_fraction(diff(expression, self.x))


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
        roots = get_roots(der, degree=get_degree(der, gen=self.x), as_tex=False,
                          l_b=l_b, u_b=u_b)

        def sign_of_der(x_val):
            val = der.evalf(subs={self.x: x_val})
            if val == 0.:
                return "0"
            elif val > 0:
                return "+"
            return "-"

        def sign_between(low, high):
            """The sign of the derivative strictly between two bounds.

            The bounds are those of the interval the function is defined on, so
            the point sampled has to lie inside it. Sampling a fixed abscissa
            instead, x = 0 or a root plus one, reads the derivative where the
            function does not live and reverses the arrows of the table.

            Args:
                low: The lower bound, possibly -oo.
                high: The upper bound, possibly oo.

            Returns:
                "+", "-" or "0".
            """
            if low == -oo and high == oo:
                sample = 0.
            elif low == -oo:
                sample = high - 1
            elif high == oo:
                sample = low + 1
            else:
                sample = (low + high) / 2
            return sign_of_der(sample)

        df_values = [latex(self._real_lim(der, l_b))]
        for i, r in enumerate(roots):
            if i == 0:
                df_values.append(sign_between(l_b, r))

            df_values.append("0")

            if i == len(roots) - 1:
                df_values.append(sign_between(r, u_b))
            else:
                df_values.append(sign_between(r, roots[i + 1]))
        if not len(roots):  # No roots, just get the constant sign of the derivative
            df_values.append(sign_between(l_b, u_b))
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
