from sympy import latex, Expr

def pretty_print_eq(eq: Expr|str):
    if isinstance(eq, Expr):
        eq_str="$"+latex(eq)+"$"
        return eq_str
    else:
        return eq
