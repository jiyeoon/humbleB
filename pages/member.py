import os, sys

import streamlit as st
import pandas as pd

from utils.ui import set_sidebar, set_page_config
from utils.func import get_member, guest_info

# --- Streamlit Page Setting
set_page_config()
set_sidebar()


# --- UI (Main)
st.write("# Member")

data = get_member()

df = pd.DataFrame(data)
st.session_state.df = df
st.session_state.df.index += 1
editor_df = st.dataframe(st.session_state.df, use_container_width=True, hide_index=False)#, num_rows='dynamic', on_change=None, hide_index=True, use_container_width=True)
st.session_state.editor_df = editor_df

st.html("""
<style>
[data-testid=stElementToolbarButton]:first-of-type {
    display: none;
}
</style>
""")

# if st.button("Edit", icon=":material/edit:"):
#     st.session_state.editor_df = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True)
#     st.rerun()
#     # st.session_state.df = st.data_editor(df, use_container_width=True, hide_index=True)
#     st.write("Save Complete!")

# if st.button("Add Member", icon=":material/person_add:"):
#     guest_info()