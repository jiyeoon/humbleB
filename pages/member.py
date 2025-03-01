import os, sys

import streamlit as st
import pandas as pd

from utils.ui import set_sidebar
from utils.func import get_member

# --- Page Config
st.set_page_config(
    page_title="Streamlit App", 
    page_icon="🧊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

# --- Side Bar
set_sidebar()


# --- Main
st.write("# Member")

data = get_member()

df = pd.DataFrame(data)
editor_df = st.data_editor(df, num_rows='dynamic', on_change=None, hide_index=True, use_container_width=True)

