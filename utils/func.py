import os, sys, json
import sqlite3

import streamlit as st

def get_member(file_path='./asset/members'):
    data = {
        'name' : [],
        'gender' : [],
        'years' : [],
        'ntrp' : []
    }

    with open(file_path, 'r') as f:
        for line in f:
            name, gender, years, ntrp = line.strip().split(' ')
            data['name'].append(name)
            data['gender'].append(gender)
            data['years'].append(years)
            data['ntrp'].append(ntrp)
    
    return data


# TODO
def set_member(data, file_path='./asset/members'):
    return 

@st.dialog("게스트 정보 입력")
def guest_info():
    name = st.text_input('이름')
    gender = st.selectbox('성별', ['남', '여'])
    years = st.number_input('구력 (required)', value=1, min_value=1)
    ntrp = st.number_input('NTRP (required)', value=2.5, min_value=1.0, max_value=7.0, step=0.5)
    # start_time = st.number_input('시작시간', value=1, min_value=1, max_value=6)
    # end_time = st.number_input('종료시간', value=6, min_value=1, max_value=6)

    # 나중엔 그냥 session에만 더하는게 아니라 데이터베이스나... 뭐에도 저장해야할듯?
    if st.button('Submit'):
        st.session_state.guest['name'].append(name)
        st.session_state.guest['gender'].append(gender)
        st.session_state.guest['years'].append(years)
        st.session_state.guest['ntrp'].append(ntrp)
        # st.session_state.guest[name] = [gender, years, ntrp, start_time, end_time]
        st.write('게스트 정보 추가 완료!')
        st.rerun()