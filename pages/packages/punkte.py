import streamlit as st
import sympy as sp
import numpy as np

class Punkt:
    def __init__(self, x_wert, y_wert, name) -> None:
        self.x_wert = x_wert
        self.y_wert = y_wert
        self.name = name

    def nameAusgeben(self):
        ausgabe = r"$%s\left(%s,%s \right)$" % (self.name, sp.latex(self.x_wert), sp.latex(self.y_wert))
        return ausgabe
                
        
class Extrempunt(Punkt):
    def __init__(self, x_wert, y_wert, name) -> None:
        super().__init__(x_wert, y_wert, name)