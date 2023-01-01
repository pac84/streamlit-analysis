import sympy as sp
import numpy as np
import matplotlib as plt
from os import minor
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

def plotten(functions, punkte=[], xmin=-5, xmax=5, ymin=-5, ymax=5, draw_grid=True, draw_ticks=True, ticks_frequency_x=1, ticks_frequency_y=1, scale_x=1, scale_y=1, draw_pi=False, legende=False, dateiname='graph'):
    # Settings
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'tab:cyan', 'tab:orange', 'tab:brown', 'tab:pink', 'tab:purple']
    x = sp.symbols('x')

    x_schneidet_y = 0
    y_schneidet_x = 0

    xlist = np.linspace(xmin, xmax, 1000)

    fig, ax = plt.subplots(figsize=((xmax-xmin)/scale_x, (ymax-ymin)/scale_y))
    fig.patch.set_facecolor('#ffffff')        
    #legende = []
    for index,function in enumerate(functions):
        if str(type(function))[19:26] != 'numbers':
            y = sp.lambdify(x, function, 'numpy')
            ylist = y(xlist)
            ylist[:-1][abs(np.diff(ylist)) > 100] = np.nan
            ax.plot(xlist,ylist,colors[index%11])
        else:
            ax.plot([xmin,xmax],[sp.Float(function),sp.Float(function)],colors[index%11])
    if legende:
        leg = []
        for i in range(len(functions)):
            leg.append('$f$' + i*"'" + '(x)')
        ax.legend(leg)
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
    
    # Punkt zeichnen
    if len(punkte)>0:
        for i in range(len(punkte)):
            koordinaten = r'$P_{%s}(%s|%s)$' % (i+1, sp.latex(punkte[i][0]), sp.latex(punkte[i][1]))
            ax.plot(punkte[i][0], punkte[i][1], marker="x", markersize=10, markeredgecolor="green", markerfacecolor="green")
            ax.text(punkte[i][0]+0.2,punkte[i][1],koordinaten,fontsize='16',fontfamily='sans-serif',color='green')

    #plt.plot(x, g, 'g-', linewidth=2)
    #plt.savefig('graph.png',bbox_inches='tight')
    plt.savefig('images/'+dateiname+'.pdf',bbox_inches='tight')
    return plt