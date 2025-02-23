from sympy import latex, Expr, rootof


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

def get_roots(expr,degree, as_tex=True ):
    roots = []
    for i in range(degree):
        try:
            root = rootof(expr, i)
            if root.is_real:
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
