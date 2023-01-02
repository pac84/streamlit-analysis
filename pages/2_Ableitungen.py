import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *

st.set_page_config(page_title="Ableitungsfunktionen", page_icon="⚖️")

st.header("Bilden von Ableitungsfunktionen")
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

col1, col2 = st.columns([1,10])

anzahl = st.slider('Anzahl der Ableitungen', min_value=1, max_value=4, value=1)
with col1:
    st.latex('f(x) = ')
with col2:
    eingabe = st.text_input("Rechte Seite der Funktion eingeben", label_visibility='collapsed')
eingabe= eingabe.replace("^", "**")

x = sp.Symbol('x')
f = sp.Function('f')


try:
    f = sp.parse_expr(eingabe)
    ableitungen = [f]
    for i in range(1,anzahl+1):
        ableitungen.append(sp.diff(ableitungen[i-1],x))
    st.write('Die Funktion und ihre Ableitung(en):')
    ausgabe = r'\begin{align*}'+'\n'
    for i in range(len(ableitungen)):
        ausgabe += 'f' + i*"'" + '(x) &= ' + sp.latex(sp.simplify(ableitungen[i])).replace('log', 'ln') + r'\\' + '\n'
    ausgabe += r'\end{align*}'
    st.latex(ausgabe)
    zeichnen = st.checkbox('Zeichnen der Funktionsgraphen?')
    if zeichnen:
        st.write('Einstellungen ändern')    
        xmin = st.slider(r'$x_{\text{min}}$', min_value=-10, max_value=-1, value=-5)
        xmax = st.slider(r'$x_{\text{max}}$', min_value=1, max_value=10, value=5)
        ymin = st.slider(r'$y_{\text{min}}$', min_value=-10, max_value=-1, value=-5)
        ymax = st.slider(r'$y_{\text{max}}$', min_value=1, max_value=10, value=5)
        textgroesse = st.slider('Textgröße', min_value=10, max_value=18, value=14)
        #skalierung_x = st.slider('Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #skalierung_y = st.slider('Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        #ticks_x = st.slider('Abstand Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #ticks_y = st.slider('Abstand Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        gitter = st.checkbox('Gitter zeichnen', value=True)
        skala = st.checkbox('Achsen skalieren', value=True)
        legend = st.checkbox('Legende hinzufügen', value=True)
        st.pyplot(plotten(ableitungen, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-ableitung', textgroesse=textgroesse))
        try:
            with open("images/graph-ableitung.pdf", "rb") as file:
                    btn = st.download_button(
                    label="Graph speichern",
                    data=file,
                    file_name="images/graph-ableitung.pdf",
                    mime="image/pdf"
                )
        except:
            pass
except:
    st.write('Bitte korrekten Funktionsterm eingeben.')