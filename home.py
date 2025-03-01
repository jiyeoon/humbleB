import os, sys

import streamlit as st 

from utils.ui import set_sidebar

st.set_page_config(
    page_title="humbleB App", 
    page_icon=":home:",    
    layout="wide", 
    initial_sidebar_state="collapsed"
)

set_sidebar()

st.markdown("# Test App")