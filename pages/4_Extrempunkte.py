import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *
from pages.packages.punkte import *

st.set_page_config(page_title="Extrempunkte bestimmen", page_icon="⚖️")

st.header("Extrempunkte bestimmen")
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

with col1:
    st.latex('f(x) = ')
with col2:
    eingabe = st.text_input("Rechte Seite der Funktion eingeben", label_visibility='collapsed')
eingabe= eingabe.replace("^", "**")

x = sp.Symbol('x')
f = sp.Function('f')
f1 = sp.Function('f1')
f2 = sp.Function('f2')

try:
    f = sp.parse_expr(eingabe)
    f1 = sp.simplify(sp.diff(f,x))
    f2 = sp.simplify(sp.diff(f1,x))
    
    ableitungen = [f]
    for i in range(1,3):
        ableitungen.append(sp.diff(ableitungen[i-1],x))
    st.subheader("Ableitungsfunktionen")
    st.write('Die Funktion und ihre Ableitung(en):')
    ausgabe = r'\begin{align*}'+'\n'
    for i in range(len(ableitungen)):
        ausgabe += 'f' + i*"'" + '(x) &= ' + sp.latex(sp.simplify(ableitungen[i])).replace('log', 'ln') + r'\\' + '\n'
    ausgabe += r'\end{align*}'
    st.latex(ausgabe)

    st.subheader("Gleichung lösen")
    st.markdown("Lösen der Gleichung $f'(x)=0$.")
    st.latex(r'%s = 0' % sp.latex(f1))
    try:
        lsg = sp.solve(f1, x, rational=True)
        lsg2 = []
        for i in range(len(lsg)):
            if sp.im(lsg[i]) == 0:
                lsg2.append(lsg[i])
        punkte = []    
        if len(lsg2) > 0:
            #st.write("Lösung der Gleichung")
            for i in range(len(lsg2)):
                punkt = Punkt(lsg2[i], f.subs(x,lsg2[i]), r"$E_{"+str(i)+r"}")
                punkte.append(punkt)
                lsg_string = "x_{%d} = " % ((i+1))
                lsg_string += sp.latex(sp.simplify(lsg2[i]))
                lsg_string = lsg_string.replace("log", "ln")
                st.latex(lsg_string)
            
            st.subheader("Überprüfung, y-Werte")
            st.markdown("Überprüfen der möglichen Extremstellen und Bestimmung der y-Werte")
            i=0
            zaehlerHP = 1
            zaehlerTP = 1
            
            for punkt in punkte:
                text1 = '#### Lösung %s' % (i+1)
                # Minimum = 1, Maximum = 2, nichts = 0
                punktEigenschaft = 0
                st.markdown(text1)
                st.markdown(r"Überprüfung für mögliche Extremstelle $x_{%s}$" % (i+1))
                
                pruefe = f2.subs(x,punkt.x_wert)
                if pruefe > 0:
                    pruefeErg = " > 0"
                elif pruefe < 0:
                    pruefeErg = " < 0"
                else:
                    pruefeErg = ""
                st.latex(r"f''\left(%s\right) = %s = %s %s \\" % (sp.latex(punkt.x_wert), sp.latex(f2.subs(x,sp.UnevaluatedExpr(punkt.x_wert))), sp.latex(f2.subs(x,punkt.x_wert)), pruefeErg))
                if pruefe > 0:
                    st.markdown("Es gilt $f''(x) > 0$, d.h. es handelt sich um ein Minimum.")
                    punktEigenschaft = 1
                elif pruefe < 0:
                    st.markdown("Es gilt $f''(x) < 0$, d.h. es handelt sich um ein Maximum.")
                    punktEigenschaft = 2
                else:
                    st.markdown("Es gilt $f''(x) = 0$, d.h. die Überprüfung muss über den Vorzeichenwechsel (VZW) von $f'(x)$ erfolgen.")
                    erg1 = f1.subs(x,punkt.x_wert-0.1)
                    erg2 = f1.subs(x,punkt.x_wert+0.1)
                    ausgabe2 = r"\begin{align*}"
                    ausgabe2 += r"f'\left(%s\right) &= %s = %s \\" % (sp.latex(punkt.x_wert-0.1), sp.latex(f1.subs(x,sp.UnevaluatedExpr(punkt.x_wert-0.1))), sp.latex(erg1))
                    ausgabe2 += "\n"
                    ausgabe2 += r"f'\left(%s\right) &= %s = %s" % (sp.latex(punkt.x_wert+0.1), sp.latex(f1.subs(x,sp.UnevaluatedExpr(punkt.x_wert+0.1))), sp.latex(erg2))
                    ausgabe2 += "\n" + r'\end{align*}'
                    st.latex(ausgabe2)
                    if erg1 < 0 and erg2 > 0:
                        st.markdown("VZW von - zu +, d.h. es handelt sich um ein Minimum.")
                        punktEigenschaft = 1
                    elif erg1 > 0 and erg2 < 0:
                        st.markdown("VZW von + zu -, d.h. es handelt sich um ein Maximum.")
                        punktEigenschaft = 2
                    else:
                        st.markdown("Es gibt keinen VZW bei $f'(x)$, d.h. es handelt sich nicht um eine Extremstelle.")
                i+=1
                
                if punktEigenschaft == 1 or punktEigenschaft == 2:
                    st.markdown("Berechnung des y-Wertes")
                    st.latex(r"f\left(%s\right) = %s = %s" % (sp.latex(punkt.x_wert), sp.latex(f.subs(x,sp.UnevaluatedExpr(punkt.x_wert))), sp.latex(f.subs(x,punkt.x_wert))))
                    st.markdown("Es gilt:")
                    if punktEigenschaft == 1:
                        st.latex(r"T_{%d}\left(%s\middle|%s\right)" % (zaehlerTP, sp.latex(punkt.x_wert), sp.latex(punkt.y_wert)))
                        punkt.name = r"T_{%d}" % zaehlerTP
                        zaehlerTP += 1
                    else:
                        st.latex(r"H_{%d}\left(%s\middle|%s\right)" % (zaehlerTP, sp.latex(punkt.x_wert), sp.latex(punkt.y_wert)))
                        punkt.name = r"H_{%d}" % zaehlerHP
                        zaehlerHP += 1
        else:
            st.write("Die Gleichung ist nicht lösbar")
    except:
        st.write("Die Gleichung ist nicht lösbar")

    zeichnen = st.checkbox('Zeichnen der Funktionsgraphen?')
    if zeichnen:
        st.write('Einstellungen ändern')    
        xmin = st.slider(r'$x_{\text{min}}$', min_value=-10, max_value=-1, value=-5)
        xmax = st.slider(r'$x_{\text{max}}$', min_value=1, max_value=10, value=5)
        ymin = st.slider(r'$y_{\text{min}}$', min_value=-10, max_value=-1, value=-5)
        ymax = st.slider(r'$y_{\text{max}}$', min_value=1, max_value=10, value=5)
        #skalierung_x = st.slider('Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #skalierung_y = st.slider('Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        #ticks_x = st.slider('Abstand Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #ticks_y = st.slider('Abstand Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        gitter = st.checkbox('Gitter zeichnen', value=True)
        skala = st.checkbox('Achsen skalieren', value=True)
        legend = st.checkbox('Legende hinzufügen', value=True)
        st.pyplot(plotten([f], punkte, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-ableitung'))
        try:
            with open("images/graph-extrempunkte.pdf", "rb") as file:
                    btn = st.download_button(
                    label="Graph speichern",
                    data=file,
                    file_name="images/graph-extrempunkte.pdf",
                    mime="image/pdf"
                )
        except:
            pass
except:
    st.write('Bitte korrekten Funktionsterm eingeben.')