import os, sys

import streamlit as st

# --- streamlit page 
def set_page_config():
    st.set_page_config(
        page_title="HumbleB", 
        page_icon=":tennis:", 
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

def set_sidebar():
    st.sidebar.page_link('home.py', label='Home', icon=':material/home:')
    st.sidebar.page_link('pages/member.py', label='Member', icon=':material/group:')
    st.sidebar.page_link('pages/schedule.py', label='Schedule', icon=':material/calendar_month:')
    st.sidebar.page_link('pages/notice.py', label='Notice', icon=':material/insert_comment:')
    st.sidebar.page_link('https://www.instagram.com/humblebee_tennis/', label='Instagram', icon=':material/favorite:')


# --- data frame style
def highlight_cells(row):
    styles = ['' for _ in row]

    if row['코트1 분류'] == '남복':
        styles[1] = 'background-color: lightblue'
        styles[2] = 'background-color: lightblue'
    elif row['코트1 분류'] == '여복':
        styles[1] = 'background-color: lightpink'
        styles[2] = 'background-color: lightpink'
    elif row['코트1 분류'] == '혼복':
        styles[1] = 'background-color: lightyellow'
        styles[2] = 'background-color: lightyellow'
    else:
        styles[1] = 'background-color: lightgrey'
        styles[2] = 'background-color: lightgrey'
    
    if row['코트2 분류'] == '남복':
        styles[3] = 'background-color: lightblue'
        styles[4] = 'background-color: lightblue'
    elif row['코트2 분류'] == '여복':
        styles[3] = 'background-color: lightpink'
        styles[4] = 'background-color: lightpink'
    elif row['코트2 분류'] == '혼복':
        styles[3] = 'background-color: lightyellow'
        styles[4] = 'background-color: lightyellow'
    else:
        styles[3] = 'background-color: lightgrey'
        styles[4] = 'background-color: lightgrey'
    
    return styles