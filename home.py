import os, sys

import streamlit as st 

from utils.ui import set_sidebar

st.set_page_config(
    page_title="humbleB App", 
    page_icon=":home:",    
    layout="wide", 
    initial_sidebar_state="collapsed"
)
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)


set_sidebar()

st.markdown("# Test App")