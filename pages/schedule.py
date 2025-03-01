import streamlit as st
import pandas as pd

from utils.ui import set_sidebar
from utils.func import get_member, guest_info, create_tennis_schedule

# --- Streamlit Config  
st.set_page_config(
    page_title="Streamlit App", 
    page_icon="🧊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

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
    attendee = attendee_df.values.tolist()
    schedule, games_per_member = create_tennis_schedule(attendee)

    st.write("Schedule Generated!")

    result = {
        '코트1' : [],
        '코트1 분류' : [],
        '코트2' : [],
        '코트2 분류' : [],
    }

    for timeslot, courts in schedule.items():
        for court_idx, court_players in enumerate(courts, 1):
            result[f'코트{court_idx}'].append(court_players[0])
            result[f'코트{court_idx} 분류'].append(court_players[1])

    df = pd.DataFrame(result)

    def highlight_cells(row):
        styles = ['' for _ in row]

        if row['코트1 분류'] == '남복':
            styles[0] = 'background-color: lightblue'
            styles[1] = 'background-color: lightblue'
        elif row['코트1 분류'] == '여복':
            styles[0] = 'background-color: lightpink'
            styles[1] = 'background-color: lightpink'
        elif row['코트1 분류'] == '혼복':
            styles[0] = 'background-color: lightyellow'
            styles[1] = 'background-color: lightyellow'
        
        if row['코트2 분류'] == '남복':
            styles[2] = 'background-color: lightblue'
            styles[3] = 'background-color: lightblue'
        elif row['코트2 분류'] == '여복':
            styles[2] = 'background-color: lightpink'
            styles[3] = 'background-color: lightpink'
        elif row['코트2 분류'] == '혼복':
            styles[2] = 'background-color: lightyellow'
            styles[3] = 'background-color: lightyellow'
        
        return styles
    
    st.data_editor(df.style.apply(highlight_cells, axis=1))


