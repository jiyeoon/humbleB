import streamlit as st
import pandas as pd

from utils.ui import *
from utils.func import *

# --- Streamlit Page Setting
set_page_config()
set_sidebar()

# --- Initialzie
if st.session_state.get('guest') is None:
    st.session_state.guest = {
        'name' : [],
        'gender' : [],
        'years' : [],
        'ntrp' : []
    }
st.html("""
<style>
[data-testid=stElementToolbarButton]:first-of-type {
    display: none;
}
</style>
""")

# --- UI (Main)
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

st.session_state.attendee_df = attendee_df
st.session_state.total_cnt = len(st.session_state.attendee_df)
st.session_state.male_cnt = len(st.session_state.attendee_df[st.session_state.attendee_df['gender']=='남'])
st.session_state.female_cnt = len(st.session_state.attendee_df[st.session_state.attendee_df['gender']=='여'])
st.write("총 {}명 / 최대 12명 (남 : {}명 / 여 : {}명)".format(st.session_state.total_cnt, st.session_state.male_cnt, st.session_state.female_cnt))
st.data_editor(st.session_state.attendee_df, hide_index=True, use_container_width=True, on_change='rerun')


if st.button("Generate Schedule"):
    attendee = st.session_state.attendee_df.values.tolist()
    schedule, games_per_member = create_tennis_schedule(attendee)

    st.write("Schedule Generated!")
    
    result = {
        'set' : [],
        '코트1' : [],
        '코트1 분류' : [],
        '코트2' : [],
        '코트2 분류' : [],
    }

    for timeslot, courts in schedule.items():
        result['set'].append(f'{timeslot} set')
        for court_idx, court_players in enumerate(courts, 1):
            result[f'코트{court_idx}'].append(court_players[0])
            result[f'코트{court_idx} 분류'].append(court_players[1])

    df = pd.DataFrame(result)
    
    st.data_editor(df.style.apply(highlight_cells, axis=1), hide_index=True)

    st.dataframe(games_per_member)

