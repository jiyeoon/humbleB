import os, sys, json
import sqlite3
import random
import itertools

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
    schedule = {str(i+1): [[], []] for i in range(NUM_TIMESLOTS)}
    games_per_member = defaultdict(lambda:defaultdict(lambda:0)) # {name: {total: 0, 남복: 0, 여복: 0, 혼복: 0, 기타: 0}}
    used_combinations = set()  # (player1, player2, player3, player4)
    used_partner_combinations = set()  # (partner1, partner2)
    game_type_count = defaultdict(int)

    members = []
    for i in range(len(attendee)):
        name, gender, years, ntrp, start_time, end_time = attendee[i]
        members.append({
            "name": str(name),
            "gender": str(gender),
            "years": int(years),
            "ntrp": float(ntrp),
            "start_time": int(start_time),
            "end_time": int(end_time),
            "available_times": set(range(start_time, end_time+1))
        })

    for timeslot in range(1, NUM_TIMESLOTS+1):
        available_members = [m for m in members if timeslot in m['available_times']]

        for court in range(NUM_COURT):
            if not available_members:
                break  # 남은 멤버가 없으면 종료
            
            available_members.sort(key=lambda x : (games_per_member[x['name']]['total'], -x['ntrp']))

            males = sorted([m for m in available_members if m['gender'] == '남'],
                           key=lambda x: (games_per_member[x['name']]['total'], len(x['available_times']), x['years'], x['ntrp']))
            females = sorted([m for m in available_members if m['gender'] == '여'],
                             key=lambda x: (games_per_member[x['name']]['total'], len(x['available_times']), x['years'], x['ntrp']))

            selected_players = []
            game_type = "기타"

            # 4명 이상일 때는 파트너를 먼저 정하고, 그에 맞춰 4명 구성
            if len(available_members) >= 4:
                possible_pairs = []

                # 남남, 여여, 남녀 조합을 가능한 모든 조합으로 생성
                for pair in itertools.combinations(females, 2):
                    p1, p2 = pair[0], pair[1]
                    ntrp_sum = p1['ntrp'] + p2['ntrp']
                    possible_pairs.append((pair, "여여", ntrp_sum))
                for pair in itertools.combinations(males, 2):
                    p1, p2 = pair[0], pair[1]
                    ntrp_sum = p1['ntrp'] + p2['ntrp']
                    possible_pairs.append((pair, "남남", ntrp_sum))
                for male, female in itertools.product(males, females):
                    p1, p2 = pair[0], pair[1]
                    ntrp_sum = p1['ntrp'] + p2['ntrp']
                    possible_pairs.append(((male, female), "남녀", ntrp_sum))

                # 기존에 사용된 파트너 조합이 아닌 것을 우선 선택
                random.shuffle(possible_pairs)
                # possible_pairs = sorted(possible_pairs, key=lambda p: (games_per_member[p[0][0]["name"]]['total'], games_per_member[p[0][1]['name']]['total'], len(p[0][0]['available_times']), len(p[0][1]['available_times'])))
                possible_pairs = sorted(possible_pairs, key=lambda p: (games_per_member[p[0][0]["name"]]['total'], games_per_member[p[0][1]['name']]['total'], -p[2]))

                # possible_pairs = [p for p in possible_pairs if tuple([p[0][0]["name"], p[0][1]["name"]]) not in used_partner_combinations]
                
                comb = []
                for (pair1, type1, _) in possible_pairs * 2:
                    for (pair2, type2, _) in possible_pairs * 2:
                        if pair1 == pair2:
                            continue
                        if type1 == type2: #or (type1, type2) in [("남남", "여여"), ("여여", "남남"), ("남녀", "남녀")]:
                            team1 = tuple(sorted([pair1[0]["name"], pair1[1]["name"]]))
                            team2 = tuple(sorted([pair2[0]["name"], pair2[1]["name"]]))

                            # **중복 방지: 같은 사람이 두 번 선택되지 않도록 함**
                            if team1 in used_partner_combinations or team2 in used_partner_combinations:
                                continue  # 이미 사용된 파트너 조합이면 패스
                            if set(team1) & set(team2):  # 같은 사람이 포함되면 패스
                                continue  
                            if set(team1).union(team2) in used_combinations and set(team1).union(team2) not in comb:
                                comb.append(set(team1).union(team2))
                                continue

                            selected_players = [pair1[0], pair1[1], pair2[0], pair2[1]]
                            used_partner_combinations.add(team1)
                            used_partner_combinations.add(team2)

                            # 게임 타입 결정
                            if type1 == "남남" and type2 == "남남":
                                game_type = "남복"
                            elif type1 == "여여" and type2 == "여여":
                                game_type = "여복"
                            else:
                                game_type = "혼복"
                            break
                    if selected_players:
                        break
            
            # 4명 미만일 경우 가능한 모든 멤버 추가
            if not selected_players:
                selected_players = available_members[:]
                game_type = "기타"

            # 조합 기록 (같은 4명이 다시 만나지 않도록)
            court_combination = tuple(sorted([p["name"] for p in selected_players]))

            if len(selected_players) == 4:
                used_combinations.add(court_combination)

            # 스케줄에 추가
            schedule[str(timeslot)][court] = [[p["name"] for p in selected_players], game_type]
            game_type_count[game_type] += 1

            # ✅ **배정된 멤버들을 안전하게 제거**
            assigned_names = set(p["name"] for p in selected_players)
            available_members = [m for m in available_members if m["name"] not in assigned_names]

            # 멤버 사용 횟수 증가
            for player in selected_players:
                games_per_member[player["name"]]['total'] += 1
                games_per_member[player["name"]][game_type] += 1
    
    # ✅ 게임 수 불균형 조정 단계
    min_games = min(games_per_member[m['name']]['total'] for m in members)
    max_games = max(games_per_member[m['name']]['total'] for m in members)

    ii = 0
    while min_games < 4 and ii <= 100:
        min_player = next(m for m in members if games_per_member[m['name']]['total'] == min_games)
        max_player_candidates = [m for m in members if games_per_member[m['name']]['total'] == max_games and m['gender'] == min_player['gender']]

        if not max_player_candidates:
            break
            
        max_player = max_player_candidates[0]

        swapped = False
        for timeslot in range(min_player['start_time'], min_player['end_time'] + 1):
            if min_player['name'] in [p for court in range(NUM_COURT) for p in schedule[str(timeslot)][court][0]]:
                continue  # min_player가 이미 같은 timeslot에 배정되어 있으면 넘어감
            
            for court in range(NUM_COURT):
                if min_player['name'] not in schedule[str(timeslot)][court][0] and max_player['name'] in schedule[str(timeslot)][court][0]:
                    # 🔄 교체 실행
                    schedule[str(timeslot)][court][0].remove(max_player['name'])
                    schedule[str(timeslot)][court][0].append(min_player['name'])
                    games_per_member[min_player["name"]]['total'] += 1
                    games_per_member[max_player["name"]]['total'] -= 1
                    swapped = True
                    break
            if swapped:
                break
        
        min_games = min(games_per_member[m['name']]['total'] for m in members)
        max_games = max(games_per_member[m['name']]['total'] for m in members)
        ii += 1

    return schedule, games_per_member



@st.dialog("게스트 정보 입력")
def guest_info():
    name = st.text_input('이름')
    gender = st.selectbox('성별', ['남', '여'])
    years = st.number_input('구력 (required)', value=1, min_value=1)
    ntrp = st.number_input('NTRP (required)', value=2.5, min_value=1.0, max_value=7.0, step=0.5)

    # 나중엔 그냥 session에만 더하는게 아니라 데이터베이스나... 뭐에도 저장해야할듯?
    if st.button('Submit'):
        st.session_state.guest['name'].append(name)
        st.session_state.guest['gender'].append(gender)
        st.session_state.guest['years'].append(years)
        st.session_state.guest['ntrp'].append(ntrp)
        st.write('게스트 정보 추가 완료!')
        st.rerun()