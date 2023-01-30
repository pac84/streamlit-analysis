import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *

st.set_page_config(page_title="Exponentialfunktionen", page_icon="⚖️")

st.header("Exponentialfunktionen")
expander = st.expander('Hinweise zur Eingabe')
expander.write("""
Gib eine Funktion in das Textfeld ein, achte auf folgende Hinweise:
- Nutze 'x' als Variable.
- Dezimalzahlen müssen mit einem '.' statt mit einem ',' eingegeben werden, also '2.3' für $2,3$.
- Potenzen werden mit '\*\*' oder '^' eingegeben, also z.B. x\*\*2 oder x^2 für $x^2$.
- Zwischen Faktoren und der Variablen muss ein '\*' stehen, also 2\*x statt 2x.
- Gib nur den Teil rechts vom '='-Zeichen ein, also 'x**2' für $f(x) = x^2$
- Die natürliche Exponentialfunktion $e^x$ wird mit exp(x) eingegeben.
- Wurzeln werden mit 'sqrt(x)' eingegeben.
""")

col_ab, col_cd = st.columns(2)

with col_ab:
    a = st.slider('Parameter a', min_value=-8.0, max_value=8.0, value=1.0, step=0.1)
    b = st.slider('Parameter b', min_value=-8.0, max_value=8.0, value=1.0, step=0.1)
with col_cd:    
    c = st.slider('Parameter c', min_value=-8.0, max_value=8.0, value=0.0, step=0.1)
    d = st.slider('Parameter d', min_value=-8.0, max_value=8.0, value=0.0, step=0.1)

x = sp.Symbol('x')
f = sp.Function('f')
f = sp.nsimplify(a) * sp.exp(sp.factor(sp.nsimplify(b)*(x-sp.nsimplify(c))))+sp.nsimplify(d)


st.write('Die eingegebne Funktion:')
legende = ['f(x)']
ausgabe = r'\begin{align*}'+'\n'
ausgabe += 'f(x) = ' + sp.latex(f)
ausgabe += r'\end{align*}'
st.latex(ausgabe)
st.markdown(r'''Der Graph hat folgende Parameter
- Streckung in y-Richtung $%.1f$
- Streckung in x-Richtung $%.1f$
- Verschiebung in x-Richtung um $%s$
- Verschiebung in y-Richtung um $%s$
''' % (a, b, sp.latex(sp.nsimplify(c)), sp.latex(sp.nsimplify(d))))

zeichnen = st.checkbox('Zeichnen der Funktionsgraphen?')
if zeichnen:
    st.write('Einstellungen ändern')
    col_x, col_y = st.columns(2)
    with col_x:    
        xmin = st.slider(r'$x_{\text{min}}$', min_value=-20, max_value=-1, value=-5)
        xmax = st.slider(r'$x_{\text{max}}$', min_value=1, max_value=20, value=5)
    with col_y:
        ymin = st.slider(r'$y_{\text{min}}$', min_value=-20, max_value=-1, value=-5)
        ymax = st.slider(r'$y_{\text{max}}$', min_value=1, max_value=20, value=5)
    colAuswahl1, colAuswahl2, colAuswahl3, colAuswahl4 = st.columns(4)
    with colAuswahl1:
        gitter = st.checkbox('Gitter zeichnen', value=True)
    with colAuswahl2:    
        skala = st.checkbox('Achsen skalieren', value=True)
    with colAuswahl3:    
        legend = st.checkbox('Legende hinzufügen', value=True)
    with colAuswahl4:
        textgroesse = int(st.selectbox('Schriftgröße', ('12', '13', '14', '15', '16', '17', '18'), index=2))
    st.pyplot(plotten([f], name_funktion=legende, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-Exponentialfunktion', textgroesse=textgroesse))
    try:
        with open("images/graph-Exponentialfunktion.pdf", "rb") as file:
                btn = st.download_button(
                label="Graph speichern",
                data=file,
                file_name="images/graph-Exponentialfunktion.pdf",
                mime="image/pdf"
            )
    except:
        pass
