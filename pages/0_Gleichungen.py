import streamlit as st
import sympy as sp
import numpy as np
import matplotlib as plt

st.set_page_config(page_title="Gleichungen lösen", page_icon="⚖️")

st.header("Lösen von Gleichungen")
expander = st.expander('Hinweise zur Eingabe')
expander.write("""
Gib eine Gleichung in das Textfeld ein, achte auf folgende Hinweise:
- Nutze 'x' als Variable.
- Dezimalzahlen müssen mit einem '.' statt mit einem ',' eingegeben werden, also '2.3' für $2,3$.
- Potenzen werden mit '\*\*' oder '^' eingegeben, also z.B. x\*\*2 oder x^2 für $x^2$.
- Zwischen Faktoren und der Variablen muss ein '\*' stehen, also 2\*x statt 2x.
- Die Gleichung muss auf '= 0' umgestellt sein und es wird nur eine Seite der Gleichung eingegeben, also statt 2\*x = 3 muss 2\*x - 3 eingegeben werden.
- Die natürliche Exponentialfunktion $e^x$ wird mit exp(x) eingegeben.
""")

col1, col2 = st.columns([14,1])

with col1:
    eingabe = st.text_input("Linke Seite der Gleichung eingeben", label_visibility='collapsed', )
with col2:
    st.latex(' = 0')
eingabe = eingabe.replace("^", "**")
x = sp.Symbol('x')

try:
    gleichung = sp.parse_expr(eingabe)
    st.write("Folgende Gleichung wurde eingegeben")
    gleichung2 = sp.latex(gleichung)
    st.latex(gleichung2 + " = 0")
    try:
        lsg = sp.solve(gleichung, x, rational=True)
        lsg2 = []
        for i in range(len(lsg)):
            if sp.im(lsg[i]) == 0:
                lsg2.append(lsg[i])
            
        if len(lsg2) > 0:
            st.write("Lösung der Gleichung")
            for i in range(len(lsg2)):
                lsg_string = "x_{%d} = " % ((i+1))
                lsg_string += sp.latex(sp.simplify(lsg2[i]))
                st.latex(lsg_string)
        else:
            st.write("Die Gleichung ist nicht lösbar")
    except:
        st.write("Die Gleichung ist nicht lösbar")
except:
    st.write("Bitte eine korrekte Gleichung eingeben")