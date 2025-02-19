from typing import Mapping, Final
import glob, os
from pathlib import Path

babel_dir=Path(__file__).parent/"babel"
languages_files=glob.glob("*.txt", root_dir=babel_dir)
ALL_LANGUAGES = [l.replace(".txt",'') for l in languages_files]

def read_lang(language):
    with open(babel_dir/(language+".txt"),"r", encoding="utf8") as inf:
        lines= inf.readlines()
        for i, l in enumerate(lines):
            lines[i]=l.replace("\n","")
        return lines

TRANSLATIONS={lang:read_lang(lang) for lang in ALL_LANGUAGES}


def get_trans_map(index):
    return {lang:TRANSLATIONS[lang][index] for  lang in  ALL_LANGUAGES}

equation_: Mapping[str,str] = get_trans_map(0)
equations_: Mapping[str,str] = get_trans_map(1)
solutions_: Mapping[str,str] = get_trans_map(2)
function_: Mapping[str,str] = get_trans_map(3)
derivative_: Mapping[str,str] = get_trans_map(4)
factorization_: Mapping[str,str] =  get_trans_map(5)
expansion_: Mapping[str,str] = get_trans_map(6)
expand_: Mapping[str,str] = get_trans_map(7)

derivation_: Mapping[str,str] = get_trans_map(8)
forbidden_values_: Mapping[str,str] =  get_trans_map(9)

factor_solve_:Mapping[str,str] =  get_trans_map(10)
expand_solve_:Mapping[str,str] =  get_trans_map(11)

polynomial_: Mapping[str,str] =  get_trans_map(12)
canonical_: Mapping[str,str] =  get_trans_map(13)

solve_: Mapping[str,str] =  get_trans_map(14)

calculus_exercises_: Mapping[str,str] =  get_trans_map(15)
math_exercises_: Mapping[str,str] =  get_trans_map(16)
shuffle_problems_: Mapping[str,str] = get_trans_map(17)
problems_mismatch_: Mapping[str,str] =  get_trans_map(18)
select_exercises_: Mapping[str,str] =  get_trans_map(19)
exercises_list_: Mapping[str,str] = get_trans_map(20)
num_eqs_per_table_: Mapping[str,str] =  get_trans_map(21)
generate_code_: Mapping[str,str] =  get_trans_map(22)
open_overleaf_: Mapping[str,str] =  get_trans_map(23)


