
import re

def pretty_print_eq(eq: str):
    eq_cln_exp = str(eq).replace("**", "^").replace("*", "")
    pattern = r'\bsqrt\((.*?)\)'

    # Replace 'sqrt( )' with the LaTeX form \sqrt{ }
    eq_cln_exp = re.sub(pattern, r'\\sqrt{\1}', eq_cln_exp)

    if eq_cln_exp.startswith("$"):
        return eq_cln_exp
    return "$" + eq_cln_exp + "$"
