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

"""The "cahier" look: a page of ruled paper, written in fountain pen ink.

The colours live in .streamlit/config.toml, where streamlit can hand them to
the widgets it draws itself. What cannot be said there, the ruling of the
paper, the margin rule and the typography of the headings, is the style sheet
below.
"""

import streamlit as st

# KaTeX ships Computer Modern, the face TeX sets its documents in, and
# streamlit already loads it to render st.latex. Asking for it here costs no
# download, and the stack falls back on the usual serifs where it is missing.
SERIF = ('"KaTeX_Main", "Latin Modern Roman", "Computer Modern", '
         '"Iowan Old Style", Georgia, "Times New Roman", serif')

INK = "#1f2739"
DEEP_INK = "#16305a"
BLUE = "#1d4e89"
RED = "#b4384a"
RULE = "rgba(64, 112, 170, 0.13)"
MARGIN_RULE = "rgba(180, 56, 74, 0.5)"

STYLE = f"""
<style>
/* ----------------------------------------------------------------- the desk
   A plain warm surface, so that the ruling belongs to the sheet and not to
   what it lies on. */
[data-testid="stApp"] {{
    background-color: #efe9db;
}}
[data-testid="stHeader"] {{ background: transparent; }}

/* --------------------------------------------------------------- the sheet
   Seyes ruling, the horizontal lines of a French notebook, faint enough to
   read a form over and spaced on the line height of the page. */
[data-testid="stMainBlockContainer"] {{
    position: relative;
    max-width: 52rem;
    margin-top: 1.2rem;
    padding: 2.4rem 2.8rem 3rem 4rem;
    background-color: #fdfbf4;
    background-image:
        repeating-linear-gradient(to bottom, transparent 0 27px, {RULE} 27px 28px);
    border: 1px solid #ded2b8;
    border-radius: 3px;
    box-shadow: 0 16px 38px -22px rgba(22, 48, 90, 0.45);
}}
/* the red rule every French notebook has down its left margin */
[data-testid="stMainBlockContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 2.6rem;
    width: 1.5px;
    background: {MARGIN_RULE};
}}

/* ---------------------------------------------------------------- headings */
[data-testid="stHeading"] h1,
[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3 {{
    font-family: {SERIF};
    color: {DEEP_INK};
    font-weight: 600;
    letter-spacing: 0.005em;
}}
[data-testid="stHeading"] h1 {{
    padding-bottom: 0.35rem;
    border-bottom: 3px double {BLUE};
}}
/* section headings get the section sign a textbook would use */
[data-testid="stHeading"] h3::before {{
    content: "§ ";
    color: {RED};
    font-weight: 400;
}}

/* ----------------------------------------------------------------- widgets */
[data-testid="stWidgetLabel"] p {{
    font-family: {SERIF};
    font-size: 0.95rem;
    color: {DEEP_INK};
    letter-spacing: 0.01em;
}}
/* the type filter, as chips pinned to the page */
[data-testid="stButtonGroup"] button {{
    font-family: {SERIF};
    letter-spacing: 0.01em;
}}
/* the chosen exercises, as tags written in ink */
[data-testid="stMultiSelectTagsContainer"] span {{
    font-family: {SERIF};
}}

/* -------------------------------------------------- the frieze of formulas
   st.container(key="exo_frieze") is rendered with the class below, which is
   the supported way of reaching one's own block. */
.st-key-exo_frieze {{
    margin: -0.6rem 0 1.2rem 0;
    padding-bottom: 1rem;
    border-bottom: 1px solid {RULE};
    opacity: 0.55;
    overflow-x: auto;  /* a narrow window scrolls the frieze, never clips it */
}}
.st-key-exo_frieze .katex {{ font-size: 0.9rem; }}
@media (max-width: 640px) {{
    .st-key-exo_frieze .katex {{ font-size: 0.75rem; }}
    [data-testid="stMainBlockContainer"] {{ padding: 1.6rem 1.2rem 2rem 2.4rem; }}
    [data-testid="stMainBlockContainer"]::before {{ left: 1.4rem; }}
}}

/* the two latex boxes handed to Overleaf, as manuscript pages */
form textarea {{
    width: 100%;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 0.72rem;
    line-height: 1.45;
    color: {INK};
    background: #fffdf7;
    border: 1px solid #e3d9c2;
    border-radius: 4px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.9rem;
}}
form input[type="submit"] {{
    font-family: {SERIF};
    font-size: 1rem;
    letter-spacing: 0.02em;
    color: #fffdf7;
    background: {BLUE};
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.6rem;
    margin-bottom: 1rem;
    cursor: pointer;
}}
form input[type="submit"]:hover {{ background: {DEEP_INK}; }}
</style>
"""

# One formula per family of exercises the app can generate, so the header says
# what the page is for without a word of explanation.
FRIEZE = (r"(a+b)^2 = a^2 + 2ab + b^2 \qquad \Delta = b^2 - 4ac \qquad "
          r"\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2} \qquad "
          r"f(a) \leqslant f(x) \leqslant f(b)")


def apply_theme() -> None:
    """Send the style sheet of the cahier look to the page."""
    st.html(STYLE)


def render_frieze() -> None:
    """Draw the line of formulas that sits under the title."""
    with st.container(key="exo_frieze"):
        st.latex(FRIEZE)
