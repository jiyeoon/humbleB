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
attendee_edited = st.data_editor(st.session_state.attendee_df, hide_index=True, use_container_width=True)


if st.button("Generate Schedule"):
    attendee = attendee_edited.values.tolist()
    schedule, games_per_member = create_tennis_schedule(attendee)
    
    st.write("##### Schedule")
    result = {
        'set' : [],
        '코트1' : [],
        '코트1 분류' : [],
        '코트2' : [],
        '코트2 분류' : [],
    }

    for timeslot, courts in schedule.items():
        result['set'].append(f'{timeslot} set')
        for court_idx, court_info in enumerate(courts, 1):
            if not court_info:
                result[f'코트{court_idx}'].append('')
                result[f'코트{court_idx} 분류'].append('')
                continue

            court_players, game_type = court_info
            if len(court_players) == 4:
                players = "{}, {} / {}, {}".format(court_players[0], court_players[1], court_players[2], court_players[3])
            else:
                players = ", ".join(court_players)
            result[f'코트{court_idx}'].append(players)
            result[f'코트{court_idx} 분류'].append(game_type)
    df = pd.DataFrame(result)
    df.index = df.index + 1
    st.dataframe(df.style.apply(highlight_cells, axis=1), hide_index=True, use_container_width=True)

    st.write("##### Games per Member")
    cnt_df = []
    for key, value in games_per_member.items():
        tmp = {k: v for k, v in value.items()}
        tmp['name'] = key
        cnt_df.append(tmp)
    cnt_df = pd.DataFrame(cnt_df, columns=['name', 'total', '남복', '여복', '혼복', '기타'])
    cnt_df.fillna(0, inplace=True)
    st.dataframe(cnt_df, hide_index=True)
    # st.dataframe(games_per_member)

