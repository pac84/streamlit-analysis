import streamlit as st
import sympy as sp
import numpy as np
import matplotlib as plt
from PIL import Image

image = Image.open('images/intro.png')

st.set_page_config(
    page_title="Analysis",
    page_icon="🏫"
)

st.write("# Berechnungen in der Analysis")

st.markdown(
    """
    Hier finden sich Berechnungen und Hilfen zur Analysis. Auf der linken Seite findet sich ein Menü mit Links zu verschiedenen Anwendungen.
    """
)

st.image(image)