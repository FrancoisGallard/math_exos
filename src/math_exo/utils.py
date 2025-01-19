def pretty_print_eq(eq: str):
    eq_cln_exp = str(eq).replace("**", "^").replace("*", "")
    if eq_cln_exp.startswith("$"):
        return eq_cln_exp
    return "$" + eq_cln_exp + "$"
