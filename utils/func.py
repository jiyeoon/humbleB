import os, sys, json
import sqlite3
import random

from collections import defaultdict
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


def create_tennis_schedule(attendee, NUM_TIMESLOTS=6, NUM_COURT=2, PLAYERS_PER_COURT=4):
    schedule = {str(i+1) : [[], []] for i in range(NUM_TIMESLOTS)}
    games_per_member = defaultdict(int)
    used_combinations = defaultdict(set)
    game_type_count = defaultdict(int)

    members = []
    for i in range(len(attendee)):
        name, gender, years, ntrp, start_time, end_time = attendee[i]
        members.append({
            "name" : name,
            "gender" : gender,
            "years" : years,
            "ntrp" : ntrp,
            "start_time" : start_time,
            "end_time" : end_time,
            "available_times" : [i for i in range(start_time, end_time+1)]
        })
    
    for timeslot in range(1, NUM_TIMESLOTS+1):
        available_members = [m for m in members if timeslot in m['available_times']]

        for court in range(NUM_COURT):
            
            available_members_sorted = sorted(available_members, key=lambda x : [games_per_member[x['name']], x['gender'], len(x['available_times']), x['years'], x['ntrp']])
            
            court_players = available_members_sorted[:2]
            genders = [p['gender'] for p in court_players]

            if genders.count("남") == 2:
                if game_type_count['남복'] <= game_type_count['여복'] and game_type_count['남복'] <= game_type_count['혼복']:
                    court_players += [p for p in available_members_sorted[2:] if p['gender'] == '남'][:2]
                    game_type = "남복"
                else:
                    court_players += [p for p in available_members_sorted[2:] if p['gender'] == '여'][:2]
                    game_type = "혼복"
            elif genders.count("여") == 2:
                if game_type_count["여복"] <= game_type_count["남복"] and game_type_count["여복"] <= game_type_count["혼복"]:
                    court_players += [p for p in available_members_sorted[2:] if p['gender'] == '여'][:2]
                    game_type = "여복"
                else:
                    court_players += [p for p in available_members_sorted[2:] if p['gender'] == '남'][:2]
                    game_type = "혼복"
            else:
                court_players += [p for p in available_members_sorted[2:] if p['gender'] == '남'][:1]
                court_players += [p for p in available_members_sorted[2:] if p['gender'] == '여'][:1]
                game_type = "혼복"
            
            if len(court_players) < PLAYERS_PER_COURT:
                court_players = available_members_sorted[:PLAYERS_PER_COURT]
                game_type = "기타"

            # 멤버들의 조합을 튜플로 만들어서 중복 체크
            court_combination = tuple(sorted([court_players[i]["name"] for i in range(len(court_players))]))

            # 중복 최소화를 위한 전략
            if all(mem_id not in used_combinations[court_players[i]["name"]] for i, mem_id in enumerate(court_combination)):
                for player in court_players:
                    used_combinations[player["name"]].update(court_combination)

            # 대진표에 추가
            game_type_count[game_type] += 1
            court_schedule = [[court_players[i]["name"] for i in range(len(court_players))], game_type]
            schedule[str(timeslot)][court] = court_schedule

            # 참여 멤버 기록 업데이트
            for player in court_players:
                games_per_member[player["name"]] += 1
            
            for p in court_players:
                available_members.remove(p)


    return schedule, games_per_member
            




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