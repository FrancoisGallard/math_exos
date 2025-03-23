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

from sympy import latex, Expr, rootof, oo


def pretty_print_eq(eq: Expr | str):
    if isinstance(eq, Expr):
        pretty =  latex(eq)
    else:
        pretty=str(eq)

    if "$" not in pretty:
        pretty = "$"+pretty+"$"
    if r"\frac{"  in pretty and r"\begin{LARGE}" not in pretty:
        pretty= r"\begin{LARGE}" + pretty + r"\end{LARGE}"
    return pretty

def get_roots(expr, degree, as_tex=True, l_b =-oo, u_b=oo):
    roots = []
    for i in range(degree):
        try:
            root = rootof(expr, i)
            if root.is_real and root>l_b and root<u_b:
                roots.append(root)
        except:
            pass
    if as_tex:
        return str(roots).replace("[", r"\{").replace("]", r"\}")
    return roots

def variation_table(x_values, df_values, max_values, f_variations, min_values):
    cols="c"*(len(df_values)-1)+"r"
    out="\n$" +r"\begin{array}{|c|"+cols+r"|}"+"\n"
    out+=fr"""\hline 
x     & {"&".join(x_values)} \\ \hline 
f'(x) & {"&".join(df_values)}  \\ \hline 
      & {"&".join(max_values)}  \\ 
f(x) & {"&".join(f_variations)} \\ 
     & {"&".join(min_values)}     \\ 
\hline 
"""
    out+=r"\end{array}"+"\n$"
    return out
