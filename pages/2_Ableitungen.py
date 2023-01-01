import streamlit as st
import sympy as sp
import numpy as np
import matplotlib as plt
from os import minor
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

def plotten(functions, xmin=-5, xmax=5, ymin=-5, ymax=5, draw_grid=True, draw_ticks=True, ticks_frequency_x=1, ticks_frequency_y=1, scale_x=1, scale_y=1, draw_pi=False):
    # Settings
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'tab:cyan', 'tab:orange', 'tab:brown', 'tab:pink', 'tab:purple']
    x = sp.symbols('x')

    x_schneidet_y = 0
    y_schneidet_x = 0

    xlist = np.linspace(xmin, xmax, 1000)

    fig, ax = plt.subplots(figsize=((xmax-xmin)/scale_x, (ymax-ymin)/scale_y))
    fig.patch.set_facecolor('#ffffff')        

    for index,function in enumerate(functions):
        if str(type(function))[19:26] != 'numbers':
            y = sp.lambdify(x, function, 'numpy')
            ylist = y(xlist)
            ylist[:-1][abs(np.diff(ylist)) > 100] = np.nan
            ax.plot(xlist,ylist,colors[index%11])
        else:
            ax.plot([xmin,xmax],[sp.Float(function),sp.Float(function)],colors[index%11])

    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax), aspect='auto')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params('both',labelsize=16)
    ax.set_xlabel('$x$', size=16, labelpad=-21, x=1+(0.03*scale_x))
    ax.set_ylabel('$y$', size=16, labelpad=-18, y=1+(0.02*scale_y), rotation=0)

    if draw_ticks == True:
        minor_ticks_x = np.arange(xmin, xmax, ticks_frequency_x/2)
        major_ticks_x = np.arange(xmin, xmax, ticks_frequency_x)
        minor_ticks_y = np.arange(ymin, ymax, ticks_frequency_y/2)
        major_ticks_y = np.arange(ymin, ymax, ticks_frequency_y)

        #ax.set_xticks(major_ticks_x[major_ticks_x != 0])
        ax.set_xticks(major_ticks_x)
        ax.set_xticks(minor_ticks_x, minor=True)
        #ax.set_yticks(major_ticks_y[major_ticks_y != 0])
        ax.set_yticks(major_ticks_y)
        ax.set_yticks(minor_ticks_y, minor=True)
    else:
        ax.set_xticks([],minor=False)
        ax.set_yticks([],minor=False)

    if draw_grid == True:
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.3)
        ax.grid(which='major', alpha=0.3)

    if draw_pi == True:
        ax.xaxis.set_major_formatter(FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else ''))
        ax.xaxis.set_major_locator(MultipleLocator(base=np.pi))    

    ax.plot((1), (x_schneidet_y), ls="", marker=">", ms=5, color="k",
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot((y_schneidet_x), (1), ls="", marker="^", ms=5, color="k",
            transform=ax.get_xaxis_transform(), clip_on=False)


    # Fläche zwischen Graphen
    #ax.fill_between(x,f,0, where=(x>0) & (x<=1.5), alpha=0.1, color='b', linewidth=0.0)
    #ax.fill_between(x,g,y2=0, where=(x>-2) & (x<=1), alpha=0.3, color='b', linewidth=0.0)
    

    #plt.plot(x, g, 'g-', linewidth=2)
    #plt.savefig('graph.png',bbox_inches='tight')
    plt.savefig('images/graph.pdf',bbox_inches='tight')
    return plt

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
anzahl = st.slider('Anzahl der Ableitungen', min_value=1, max_value=4, value=1)
eingabe = st.text_input("Rechte Seite der Funktion eingeben")
eingabe = eingabe.replace("^", "**")

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
        #skalierung_x = st.slider('Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #skalierung_y = st.slider('Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        #ticks_x = st.slider('Abstand Skalierung der x-Achse', min_value=1, max_value=4, value=1)
        #ticks_y = st.slider('Abstand Skalierung der y-Achse', min_value=1, max_value=4, value=1)
        gitter = st.checkbox('Gitter zeichnen', value=True)
        skala = st.checkbox('Achsen skalieren', value=True)
        with open("images/graph.pdf", "rb") as file:
            btn = st.download_button(
                label="Graph speichern",
                data=file,
                file_name="graph.pdf",
                mime="image/pdf"
            )
        st.pyplot(plotten(ableitungen, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, draw_grid=gitter, draw_ticks=skala))
        
        
except:
    st.write('Bitte korrekten Funktionsterm eingeben.')