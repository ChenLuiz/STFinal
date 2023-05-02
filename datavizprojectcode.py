import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Disables stupid max rows for data input
alt.data_transformers.disable_max_rows()

add_selectbox = st.sidebar.selectbox(
    "Select Year",
    ("2016", "2017", "2018", "2019", "2020"),
    key = "Sidebar"
)

with st.sidebar:
    add_radio = st.radio(
        "Select Map",
        ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train")
    )

col1, col2, col3 = st.columns(3)

st.write("""The dataset used for this project is a CSGO csv database with map picks and vetos of matches between the top 30 teams. 
         The data included is consisted of: date the match was played, team 1, team 2, inverted teams 
         (which shows us which team started banning maps first), the match ID, the even ID, best of 
         format, system for picking and banning (example: 123412 t1_remove, t2_remove, t1_pick, t2_pick, t1_remove, t2_remove, left_over), 
         which map was removed by team 1, which map was returned by team 2, which map was removed by team 1 in a bo1 format 
         (this column has a lot of 0's since most matches were best of 3s) and so on. The main research question I wanted to answer is: 
         What are the most popular maps in CSGO?""")

with col1:
   add_selectbox2 = st.selectbox(
    "Select Year",
    ("2016", "2017", "2018", "2019", "2020"),
    key = "col1"
   )

with col2:
   add_selectbox3 = st.selectbox(
    "Select Map",
    ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train"),
    key = "col2"
   )

with col3:
   add_selectbox4 = st.selectbox(
    "Select Event",
    ("Kato", "IEM", "Blast", "ESL"),
    key = "col3"
   )

with st.container():

   label_dict = {1: 'Cache', 2: 'Cobblestone', 3: 'Dust2', 4: 'Inferno', 5: 'Mirage', 6: 'Nuke', 7: 'Overpass', 8: 'Train', 9: 'Vertigo'}

   data_chart1 = pd.read_csv('updated_file.csv')
   data_chart1_labels = pd.DataFrame({'Map': label_dict.values()})

   Cumulative_maps = alt.Chart(data_chart1).transform_window(
        cumulative_count = "count()",
        sort=[{"field": "left_over"}],
   ).mark_area(color="darkseagreen").encode(
        x = alt.X("left_over:Q", title = "Map", axis=alt.Axis(values=[1, 2, 3, 4, 5, 6, 7, 8, 9])),
        y = alt.Y("cumulative_count:Q", title = "Times it has been picked"),
   )

   Map_ticks = alt.Chart(data_chart1_labels).mark_rule(color='seagreen', strokeWidth=5).encode(
        x=alt.X('Map:N', axis=None),
   )

   st.altair_chart(Cumulative_maps + Map_ticks, use_container_width=True)

with st.container():
    
   data = pd.read_csv('ban_count.csv')

   click = alt.selection_multi(encodings=['color'])

   bars = alt.Chart(data).mark_bar(strokeWidth=1, stroke='black').encode(
   alt.X('count:Q', axis=alt.Axis(ticks=True), title="Count"),
   alt.Y('map_name:N', sort=alt.EncodingSortField('count', order='ascending'), title="Map Name"),
   color=alt.Color('colors:N', scale=None),
   angle=alt.Angle('map_name:N', sort=alt.EncodingSortField('count', order='ascending')),
   tooltip=['count:Q']
   ).configure_axis(
   grid=False
   ).add_selection(
   click
   )

   st.altair_chart(bars, use_container_width=True)

with st.container():
    data_scatter = pd.read_csv('pick_count.csv')

    scatter_plot = alt.Chart(data_scatter).mark_circle(size=100, strokeWidth=1, stroke='black').encode(
    x=alt.X('Count_pick', axis=alt.Axis(title='Count Pick')),
    y=alt.Y('Count_ban', axis=alt.Axis(title='Count Ban')),
    color=alt.Color('colors:N', scale=None),
    tooltip=['Map Name', 'Count_pick', 'Count_ban']
    ).properties(
    title='Pick vs Ban rate of CS:GO maps'
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)
