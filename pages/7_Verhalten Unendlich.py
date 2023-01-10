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

st.markdown('Eingabe des Polynoms im Zähler $p(x)$ und des Polynoms im Nenner $q(x)$:')
col1, col2 = st.columns([1,6])

with col1:
    st.latex('p(x) = ')
    st.latex('q(x) = ')
with col2:
    eingabe1 = st.text_input("Polynom im Zähler", label_visibility='collapsed')
    eingabe2 = st.text_input("Polynom im Nenner", label_visibility='collapsed')
eingabe1= eingabe1.replace("^", "**")
eingabe2= eingabe2.replace("^", "**")

x = sp.Symbol('x')
f = sp.Function('f')
p = sp.Function('p')
q = sp.Function('q')


try:
    p = sp.parse_expr(eingabe1)
    q = sp.parse_expr(eingabe2)
    f = p/q
    z = sp.degree(p)
    n = sp.degree(q)

    if p.is_polynomial() and q.is_polynomial():
        st.markdown('Es wurde die folgende Funktion eingegeben:')
        st.latex('f(x) = %s' % sp.latex(f))
        st.markdown('Der Zählergrad ist $z=%s$ und der Nennergrad ist $n=%s$.' % (sp.latex(z), sp.latex(n)))
        if (z<n):
            st.markdown(r'''
            Da der Zählergrad kleiner ist als der Nennergrad, gilt $f(x) \to 0$ für $x \to \pm\infty$.
            Damit ist die x-Achse mit $y=0$ waagerechte Asymptote''')
        elif (z>n):
            st.markdown(r'''
            Da der Zählergrad kleiner ist als der Nennergrad, gilt $f(x) \to \pm\infty$ für $x \to \pm\infty$.
            Aufgrund der Koeffizienten hilt hier
            $$
            f(x) \to %s \quad \text{für} \quad x \to -\infty\\
            f(x) \to %s \quad \text{für} \quad x \to +\infty\\
            $$
            ''' % (sp.latex(sp.limit(f,x,-sp.oo)), (sp.latex(sp.limit(f,x,sp.oo)))))
        else:
            st.write(r'''
            Der Zählergrad und der Nennergrad sind identisch, d.h. eine Paralle zur x-Achse ist waagerechte Asymptote. Maßgeblich dafür sind die Koeffizienten der Potenzen mit den größten Exponenten.
            Für den Zähler ist das $a = %s$ und für den Nenner ist das $b = %s$, damit gilt
            $$
                y = \frac{a}{b} = %s
            $$
            ist waagerechte Asymptote.
            ''' % (sp.latex(p.coeff(x,z)), sp.latex(q.coeff(x,n)), sp.latex(sp.limit(f,x,sp.oo))))
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
            st.pyplot(plotten([f], name_funktion=['f(x)'], xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-verhalten-unendlich', textgroesse=textgroesse))
            try:
                with open("images/graph-verhalten-unendlich.pdf", "rb") as file:
                        btn = st.download_button(
                        label="Graph speichern",
                        data=file,
                        file_name="images/graph-verhalten-unendlich.pdf",
                        mime="image/pdf"
                    )
            except:
                pass
    else:
        st.markdown('Bitte im Zähler und Nenner jeweils eine ganzrationale Funktion eingeben')
except:
    st.write('Bitte korrekten Funktionsterm eingeben.')