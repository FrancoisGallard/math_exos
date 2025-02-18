from sympy import latex, Expr


def pretty_print_eq(eq: Expr | str):
    if isinstance(eq, Expr):
        pretty = "$" + latex(eq) + "$"
    else:
        pretty=str(eq)

    if r"\frac{"  in pretty:
        pretty= r"\begin{LARGE}" + pretty + r"\end{LARGE}"
    return pretty