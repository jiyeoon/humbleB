import streamlit as st
import pandas as pd

from utils.ui import set_sidebar
from utils.func import get_member, guest_info

# --- Streamlit Config  
st.set_page_config(
    page_title="Streamlit App", 
    page_icon="🧊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)
if st.session_state.get('guest') is None:
    st.session_state.guest = {
        'name' : [],
        'gender' : [],
        'years' : [],
        'ntrp' : []
    }

# --- 냐옹
set_sidebar()


# --- 
st.write("# Schedule")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("### Members")
    member = pd.DataFrame(get_member())
    member_df = st.dataframe(member, hide_index=True, on_select='rerun', use_container_width=True)

with col2:
    st.write("### Guest")
    guest = pd.DataFrame(st.session_state.guest)
    if len(guest['name']) != 0:
        guest_df = st.dataframe(pd.DataFrame(guest), hide_index=True, on_select='rerun', use_container_width=True)
    if st.button('Add Guest', icon=":material/person_add:"):
        guest_info()

st.write("### Attendees")
filtered_member = member.iloc[member_df.selection.rows]
if len(guest['name']) != 0:
    filtered_guest = guest.iloc[guest_df.selection.rows]
    attendee_df = pd.concat([filtered_member, filtered_guest])
else:
    attendee_df = filtered_member
attendee_df['start_time'] = 1 
attendee_df['end_time'] = 6
st.data_editor(attendee_df, hide_index=True, use_container_width=True)

if st.button("Generate Schedule"):
    st.write("Schedule Generated!")