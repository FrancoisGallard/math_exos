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

import re

from sympy import Expr, factor, fraction, latex, oo, rootof, together


def to_single_fraction(expr: Expr) -> Expr:
    """Rewrite a sum of rational fractions as a single fraction.

    Differentiating a quotient leaves sympy with the derivative spread over
    several fractions, one per term of the rule. Putting them back over a
    common denominator gives the form the exercise expects. The numerator is
    factored, the denominator comes out of ``together`` already factored.

    Args:
        expr: The expression to rewrite.

    Returns:
        The expression as a single fraction, unchanged if it has no denominator.
    """
    numerator, denominator = fraction(together(expr))
    if denominator == 1:  # Not a quotient, leave the expression alone
        return expr
    if not expr.is_Add and fraction(together(fraction(expr)[0]))[1] == 1:
        # Already a single fraction whose numerator carries no fraction of its
        # own. together would only pull the numeric part out of its radicals,
        # turning 5 / (-10x-10)**(3/2) into sqrt(10) / (20 (-x-1)**(3/2)).
        return expr
    return factor(numerator) / denominator


MATH_SEGMENT = re.compile(r"\$(.+?)\$", re.DOTALL)
RELATION = re.compile(r"(\\leq|\\geq|\\neq|=|<|>)")


def enlarge_fractions(pretty: str) -> str:
    r"""Enlarge the operands holding a fraction, leave the relations at their size.

    A whole relation set in LARGE blows up its comparison sign and its right
    hand side along with the fraction, so each operand is sized on its own:
    ``\begin{LARGE}$\frac{a}{b}$\end{LARGE} $\geq -9$``.

    Args:
        pretty: A latex string, with its math mode delimiters.

    Returns:
        The same string with the fractions, and only them, enlarged.
    """

    def _segment(match):
        content = match.group(1)
        # \systeme and the variation tables hold relations of their own
        if r"\frac{" not in content or r"\systeme" in content or r"\begin{" in content:
            return match.group(0)

        pieces = []
        for i, part in enumerate(RELATION.split(content)):  # operand, relation, ...
            if not part.strip():
                continue
            if i % 2:
                # A relation, left at the surrounding size. The empty groups give
                # it back the spacing it would get inside a whole expression.
                pieces.append("${}" + part + "{}$")
            elif r"\frac{" in part:
                pieces.append(r"\begin{LARGE}$" + part + r"$\end{LARGE}")
            else:
                pieces.append("$" + part + "$")
        return "".join(pieces)

    return MATH_SEGMENT.sub(_segment, pretty)


def pretty_print_eq(eq: Expr | str):
    if isinstance(eq, Expr):
        pretty = latex(eq)
    else:
        pretty = str(eq)

    if "$" not in pretty:
        pretty = "$" + pretty + "$"
    if r"\frac{" in pretty and r"\begin{LARGE}" not in pretty:
        pretty = enlarge_fractions(pretty)
    return pretty


def get_roots(expr, degree, as_tex=True, l_b=-oo, u_b=oo):
    roots = []
    for i in range(degree):
        try:
            root = rootof(expr, i)
            # rootof walks the roots with their multiplicity, so a double root
            # comes back twice and would be printed twice in the solution set
            if root.is_real and root > l_b and root < u_b and root not in roots:
                roots.append(root)
        except Exception:
            pass
    if as_tex:
        return str(roots).replace("[", r"\{").replace("]", r"\}")
    return roots


def variation_table(x_values, df_values, max_values, f_variations, min_values):
    cols = "c" * (len(df_values) - 1) + "r"
    out = "\n$" + r"\begin{array}{|c|" + cols + r"|}" + "\n"
    out += fr"""\hline 
x     & {"&".join(x_values)} \\ \hline 
f'(x) & {"&".join(df_values)}  \\ \hline 
      & {"&".join(max_values)}  \\ 
f(x) & {"&".join(f_variations)} \\ 
     & {"&".join(min_values)}     \\ 
\hline 
"""
    out += r"\end{array}" + "\n$"
    return out
