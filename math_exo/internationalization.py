from typing import Mapping, Final

FR:Final[str]="fr"
EN:Final[str]="en"

equation_: Mapping[str,str] =  {FR:"Equation", EN:"Equation"}
equations_: Mapping[str,str] =  {FR:"Equations", EN:"Equations"}
solutions_: Mapping[str,str] = {FR:"Solutions", EN:"Solutions"}
function_: Mapping[str,str] ={FR:"Fonction", EN:"Function"}
derivative_: Mapping[str,str] = {FR:"Dérivée", EN:"Derivative"}
factorization_: Mapping[str,str] = {FR:"Factorisation", EN:"Factorization"}
expansion_: Mapping[str,str] = {FR:"Développement", EN:"Expansion"}
expand_: Mapping[str,str] = {FR:"Développer", EN:"Expand"}

derivation_: Mapping[str,str] = {FR:"Dérivation", EN:"Derivative"}
forbidden_values_: Mapping[str,str] = {FR:"Valeurs interdites", EN:"Forbidden values"}

factor_solve_:Mapping[str,str] = {FR:"Factoriser et résoudre", EN:"Factorize and solve"}
expand_solve_:Mapping[str,str] = {FR:"Développer et résoudre", EN:"Expand and solve"}

polynomial_: Mapping[str,str] = {FR:"Polynome", EN:"Polynomial"}
canonical_: Mapping[str,str] = {FR:"Forme canonique", EN:"Canonical form"}

solve_: Mapping[str,str] = {FR:"Résoudre", EN:"Solve"}

calculus_exercises_: Mapping[str,str] = {FR:"Exercices de calcul littéral", EN:"Calculus exercises"}
math_exercises_: Mapping[str,str] = {FR:'Exercices de mathématiques', EN:"Mathematics exercises"}
select_exercises_: Mapping[str,str] = {FR:'Sélection des exercices' , EN:"Select exercises"}
exercises_list_: Mapping[str,str] = {FR:"Liste des exercices" , EN:"Exercises list"}
num_eqs_per_table_: Mapping[str,str] = {FR:"Nombre d'équations par table", EN:"Number of equations per table"}
generate_code_: Mapping[str,str] = {FR:'Générer le code LateX et le compiler' , EN:"Generate LateX code and compile"}
open_overleaf_: Mapping[str,str] = {FR:"Ouvrir dans Overleaf pour compiler" , EN:"Open Overleaf to compile"}