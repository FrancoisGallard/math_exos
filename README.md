# MathExos

## Description

MathExos is a web application to generate random mathematics exercises.

Factorize polynomials, find roots, compute derivatives, compute function variation tables, solve linear systems.
The solutions are provided with beautiful analytic expressions in Latex.

It  generates editable Latex documents for the problem page for the students, and a solution document.
These documents can be compiled online to PDF in one click using Overleaf.

The application is multi language and supports currently: Arabic, Chinease, English, French, German, Italian, Polish.
It is very easy to add a new language so if you have the need please ask!

It is a full open source and web application, based on Python, streamlit, symbolic calculations.

## Getting Started

The easyest way is to use the online [streamlit application ](https://mathexos.streamlit.app/):


## Report bugs

Please create an issue on github, with a description on how to reproduce the bug
* [GitHub repository new issue](https://github.com/FrancoisGallard/math_exos/issues/new)

## Authors

Contributors names and contact info

François Gallard, gallardf@gmail.com

## Version History
 
* 0.1
    * Initial Release: 
    * about 30 types of exercises
    * derivatives, inequalities, factorization, function variation tables, linear systems, polynomial expansion

## License

This project is licensed under the GNU AGPL v3 License - see the LICENSE.txt file for details
 
## Contributing to the project

* [GitHub repository](https://github.com/FrancoisGallard/math_exos)
* You may want to add the support of new languages by adding a file in the folder math_exos/babel/new_language.txt

## Developers

To run the application locally run the main streamlit page using:

``` 
streamlit run main_page.py
```

The project can also be used from Python scripts, see the examples folder.