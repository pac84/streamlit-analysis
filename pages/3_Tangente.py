import streamlit as st
import sympy as sp
import numpy as np
import matplotlib as plt
from pages.packages.plotFunk import *

st.set_page_config(page_title="Tangentengleichung", page_icon="⚖️")

st.header("Berechnen der Tangentengleichung")
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
Gib zusätzlich den x-Wert des Berührpunktes der Tangente an den Graphen an.
""")
col1, col2 = st.columns([1,10])
with col1:
    st.latex('f(x) = ')
with col2:
    eingabe = st.text_input("Rechte Seite der Funktion eingeben", label_visibility='collapsed')
col3, col4 = st.columns([1,2])
with col3:
    st.markdown('x-Wert des Berührpunkts')
with col4:
    x_Wert = st.text_input('x-Wert des Berührpunktes', label_visibility='collapsed')
eingabe = eingabe.replace("^", "**")

f = sp.Function('f')
f1 = sp.Function('f1')
t = sp.Function('t')
x,u = sp.symbols('x u')

try:
    f = sp.parse_expr(eingabe)
    f1 = sp.diff(f,x)
    u = sp.sympify(x_Wert)
    t = sp.simplify(f1.subs(x,u)*(x-u)+f.subs(x,u))
    beruehrpunkt = Punkt(u, f.subs(x,u), "P")
    st.markdown('Berechnung der Ableitungsfunktion')
    st.latex(r'''
        \begin{align*}
            f(x) &= %s\\
            f'(x) &= %s
        \end{align*}
        ''' % (sp.latex(f), sp.latex(f1))
    )
    st.markdown("Berechnung der benötigten Werte")
    st.latex(r'''
        \begin{align*}
        u &= %s\\
        f(%s) &= %s = %s\\
        f'(%s) &= %s = %s\\
        \end{align*}
    ''' % (sp.latex(u), sp.latex(u), sp.latex(f.subs(x,sp.UnevaluatedExpr(u))), sp.latex(f.subs(x,u)), sp.latex(u), sp.latex(f1.subs(x,sp.UnevaluatedExpr(u))), sp.latex(f1.subs(x,u)))
    )
    st.markdown("Aufstellen der Tangentengleichung und einsetzen der Werte")
    st.latex(r'''
        \begin{align*}
            y &= f'(u) \cdot (x - u) +f(u)\\
            y &= f'(%s) \cdot (%s) +f(%s)\\   
            y &=  %s \cdot (%s) + (%s)\\
            t:y &= %s
        \end{align*}
    ''' % (sp.latex(u), sp.latex(x-u), sp.latex(u), sp.latex(f1.subs(x,u)), sp.latex(x-u), sp.latex(f.subs(x,u)), sp.latex(t))
    )
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
        fig = plotten([f,t], [beruehrpunkt], name_funktion=['f', 't'], xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=True, dateiname='graph-tangente', textgroesse=textgroesse)
        st.pyplot(fig)
        try:
            with open("images/graph-tangente.pdf", "rb") as file:
                    btn = st.download_button(
                    label="Graph speichern",
                    data=file,
                    file_name="images/graph-tangente.pdf",
                    mime="image/pdf"
                )
        except:
            pass
        
except:
    st.markdown('Bitte Funktion und x-Wert eingeben.')
