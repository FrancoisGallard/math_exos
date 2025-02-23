from sympy import latex, Expr, rootof


def pretty_print_eq(eq: Expr | str):
    if isinstance(eq, Expr):
        pretty = "$" + latex(eq) + "$"
    else:
        pretty=str(eq)

    if r"\frac{"  in pretty:
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
    print("out", out)
    return out

# print(variation_table(x_values=[r"-\infty", " ", "0", " ", r"+\infty"],
#                       df_values=["5", "+", "0", "-", "-10"],
#                       max_values=[" ", " ", "10", " ", " "],
#                       f_variations=[" ", r"\nearrow", " ", r"\searrow", " "],
#                       min_values=[r"-\infty", " ", " ", " ", r"+\infty"]))