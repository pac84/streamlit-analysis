import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *

st.set_page_config(page_title="Funktionen zeichnen", page_icon="⚖️")

st.header("Zeichnen von Funktionsgraphen")
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

functionen = []
eingabe = []

anzahl = st.slider('Anzahl der zu zeichnenden Funktionsgraphen', min_value=1, max_value=5, value=1)

col1, col2 = st.columns([1,6])
with col1:
    for i in range(anzahl):
        st.latex(r'f_{%d}(x) = ' % (i+1))
with col2:
    for i in range(anzahl):
        labelEingabe = "Rechte Seite der Funktion %d eingeben" % (i+1)
        eingabeFunk = st.text_input(labelEingabe, label_visibility='collapsed')
        eingabeFunk = eingabeFunk.replace("^", "**")
        #eingabeFunk = eingabeFunk + "0*x"
        eingabe.append(eingabeFunk)

x = sp.Symbol('x')
#f = sp.Function('f')

try:
    funktionen = []
    if anzahl > 1:
        st.write('Die eingebenen Funktionen:')
    else:
        st.write('Die eingebene Funktion:')

    for eingabeFunk in eingabe:
        funktionen.append(sp.parse_expr(eingabeFunk))

    ausgabe = r'\begin{align*}'+'\n'
    legende = []
    for i in range(len(funktionen)):
        ausgabe += r'f_{' + str(i+1) + r'}(x) &= ' + sp.latex(sp.simplify(funktionen[i])) + r'\\' + '\n'
        legende.append(r'$f_{' + str(i+1) + r'}(x)$')
    ausgabe += r'\end{align*}'
    st.latex(ausgabe)
    
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
        st.pyplot(plotten(funktionen, name_funktion=legende, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-funktionen', textgroesse=textgroesse))
        try:
            with open("images/graph-funktionen.pdf", "rb") as file:
                    btn = st.download_button(
                    label="Graph speichern",
                    data=file,
                    file_name="images/graph-funktionen.pdf",
                    mime="image/pdf"
                )
        except:
            pass
except:
    st.write('Bitte korrekten Funktionsterm eingeben.')