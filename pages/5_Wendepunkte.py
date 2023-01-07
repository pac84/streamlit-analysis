import streamlit as st
import sympy as sp
import numpy as np
from pages.packages.plotFunk import *
from pages.packages.punkte import *

st.set_page_config(page_title="Wendepunkte bestimmen", page_icon="⚖️")

st.header("Wendepunkte bestimmen")
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
f3 = sp.Function('f3')

try:
    f = sp.parse_expr(eingabe)
    f1 = sp.simplify(sp.diff(f,x))
    f2 = sp.simplify(sp.diff(f1,x))
    f3 = sp.simplify(sp.diff(f2,x))
    
    ableitungen = [f]
    for i in range(1,4):
        ableitungen.append(sp.diff(ableitungen[i-1],x))
    st.subheader("Ableitungsfunktionen")
    st.write('Die Funktion und ihre Ableitung(en):')
    ausgabe = r'\begin{align*}'+'\n'
    for i in range(len(ableitungen)):
        ausgabe += 'f' + i*"'" + '(x) &= ' + sp.latex(sp.simplify(ableitungen[i])) + r'\\' + '\n'
    ausgabe += r'\end{align*}'
    st.latex(ausgabe)

    st.subheader("Gleichung lösen")
    st.markdown("Lösen der Gleichung $f''(x)=0$.")
    st.latex(r'%s = 0' % sp.latex(f2))
    try:
        lsg = sp.solve(f2, x, rational=True)
        lsg2 = []
        for i in range(len(lsg)):
            if sp.im(lsg[i]) == 0:
                lsg2.append(lsg[i])
        punkte = []    
        if len(lsg2) > 0:
            #st.write("Lösung der Gleichung")
            for i in range(len(lsg2)):
                punkt = Punkt(lsg2[i], f.subs(x,lsg2[i]), r"$W_{"+str(i)+r"}")
                punkte.append(punkt)
                lsg_string = "x_{%d} = " % ((i+1))
                lsg_string += sp.latex(sp.simplify(lsg2[i]))
                lsg_string = lsg_string
                st.latex(lsg_string)
            
            st.subheader("Überprüfung, y-Werte")
            st.markdown("Überprüfen der möglichen Wendestellen und Bestimmung der y-Werte")
            i=0
            zaehlerWP = 1
            
            for punkt in punkte:
                text1 = '#### Lösung %s' % (i+1)
                # Wendepunkt = 1, nichts = 0
                punktEigenschaft = 0
                st.markdown(text1)
                st.markdown(r"Überprüfung für mögliche Wendestelle $x_{%s}$" % (i+1))
                
                pruefe = f3.subs(x,punkt.x_wert)
                if pruefe != 0:
                    pruefeErg = r" \neq 0"
                else:
                    pruefeErg = ""
                st.latex(r"f''\left(%s\right) = %s = %s %s \\" % (sp.latex(punkt.x_wert), sp.latex(f3.subs(x,sp.UnevaluatedExpr(punkt.x_wert))), sp.latex(f3.subs(x,punkt.x_wert)), pruefeErg))
                if pruefe != 0:
                    st.markdown(r"Es gilt $f'''(x) \neq 0$, d.h. es handelt sich um eine Wendestelle.")
                    punktEigenschaft = 1
                else:
                    st.markdown("Es gilt $f'''(x) = 0$, d.h. die Überprüfung muss über den Vorzeichenwechsel (VZW) von $f''(x)$ erfolgen.")
                    erg1 = f2.subs(x,punkt.x_wert-0.1)
                    erg2 = f2.subs(x,punkt.x_wert+0.1)
                    ausgabe2 = r"\begin{align*}"
                    ausgabe2 += r"f''\left(%s\right) &= %s = %s \\" % (sp.latex(punkt.x_wert-0.1), sp.latex(f2.subs(x,sp.UnevaluatedExpr(punkt.x_wert-0.1))), sp.latex(erg1))
                    ausgabe2 += "\n"
                    ausgabe2 += r"f'\left(%s\right) &= %s = %s" % (sp.latex(punkt.x_wert+0.1), sp.latex(f2.subs(x,sp.UnevaluatedExpr(punkt.x_wert+0.1))), sp.latex(erg2))
                    ausgabe2 += "\n" + r'\end{align*}'
                    st.latex(ausgabe2)
                    if (erg1 < 0 and erg2 > 0) or (erg1 > 0 and erg2 < 0):
                        st.markdown("VZW bei $f''(X)$ d.h. es handelt sich um eine Wendestelle.")
                        punktEigenschaft = 1
                    else:
                        st.markdown("Es gibt keinen VZW bei $f''(x)$, d.h. es handelt sich nicht um eine Wendestelle.")
                i+=1
                
                if punktEigenschaft == 1:
                    st.markdown("Berechnung des y-Wertes")
                    st.latex(r"f\left(%s\right) = %s = %s" % (sp.latex(punkt.x_wert), sp.latex(f.subs(x,sp.UnevaluatedExpr(punkt.x_wert))), sp.latex(f.subs(x,punkt.x_wert))))
                    st.markdown("Es gilt:")
                    if punktEigenschaft == 1:
                        st.latex(r"W_{%d}\left(%s\middle|%s\right)" % (zaehlerWP, sp.latex(punkt.x_wert), sp.latex(punkt.y_wert)))
                        punkt.name = r"W_{%d}" % zaehlerWP
                        zaehlerWP += 1
        else:
            st.write("Die Gleichung ist nicht lösbar")
    except:
        st.write("Die Gleichung ist nicht lösbar")

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
        st.pyplot(plotten([f], punkte, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala, legende=legend, dateiname='graph-ableitung', textgroesse=textgroesse))
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