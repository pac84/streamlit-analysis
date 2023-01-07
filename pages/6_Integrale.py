import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *

st.set_page_config(page_title="Integrale", page_icon="")

st.header("Berechnen von Integralen")
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
- Die untere Grenze muss kleiner als die obere Grenze sein.
""")

col1, col2 = st.columns([1,10])

untere_Grenze = sp.nsimplify(st.slider('untere Grenze', min_value=-20.0, max_value=19.0, value=-1.0, step=0.1),rational=True)
obere_Grenze = sp.nsimplify(st.slider('obere Grenze', min_value=-19.0, max_value=20.0, value=1.0, step=0.1),rational=True)
with col1:
    st.latex('f(x) = ')
with col2:
    eingabe = st.text_input("Rechte Seite der Funktion eingeben", label_visibility='collapsed')
eingabe= eingabe.replace("^", "**")

x = sp.Symbol('x')
f = sp.Function('f')
F = sp.Function('F')

try:
    f = sp.parse_expr(eingabe)
    F = sp.integrate(f,x)

    st.write('Die eingegeben Funktion und ihre Stammfunktion:')
    ausgabe = r'\begin{align*}'+'\n'
    ausgabe += 'f(x) &= ' + sp.latex(sp.simplify(f)) + r'\\' + '\n'
    ausgabe += 'F(x) &= ' + sp.latex(sp.simplify(F)) + r'\\' + '\n'
    ausgabe += r'\end{align*}'
    st.latex(ausgabe)

    if untere_Grenze < obere_Grenze:
        st.markdown("Berechnung des Integrals")
        ausgabe = r'\begin{align*}'+'\n'
        ausgabe += r'\int_{%s}^{%s}f(x)\,dx &= \int_{%s}^{%s}%s\,dx' % (sp.latex(untere_Grenze), sp.latex(obere_Grenze), sp.latex(untere_Grenze), sp.latex(obere_Grenze), sp.latex(f))
        ausgabe += r'\\' + '\n'
        ausgabe += r'&= \left[ %s \right]_{%s}^{%s}' % (sp.latex(F), sp.latex(untere_Grenze), sp.latex(obere_Grenze))
        ausgabe += r'\\' + '\n'
        ausgabe += r'&= \left( %s \right) - \left( %s \right)' % (sp.latex(F.subs(x,sp.UnevaluatedExpr(obere_Grenze))), sp.latex(F.subs(x,sp.UnevaluatedExpr(untere_Grenze))))
        ausgabe += r'\\' + '\n'
        ausgabe += r'&= \left( %s \right) - \left( %s \right)' % (sp.latex(F.subs(x,obere_Grenze)), sp.latex(F.subs(x,untere_Grenze)))
        ausgabe += r'\\' + '\n'
        ausgabe += r'&= %s' % (sp.latex(F.subs(x,obere_Grenze)-F.subs(x,untere_Grenze)))
        ausgabe += r'\\' + '\n'
        ausgabe += r'\end{align*}'
        print(untere_Grenze)
        st.latex(ausgabe)
    else:
        st.write("Die untere Grenze muss kleiner als die obere Grenze sein.")

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
        st.pyplot(plotten([f], flaeche=[untere_Grenze, obere_Grenze], xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-ableitung', textgroesse=textgroesse))
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