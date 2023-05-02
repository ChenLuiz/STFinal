import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Disables stupid max rows for data input
alt.data_transformers.disable_max_rows()

st.write("""The dataset used for this project is a CSGO csv database with map picks and vetos of matches between the top 30 teams. 
         The data included is consisted of: date the match was played, team 1, team 2, inverted teams 
         (which shows us which team started banning maps first), the match ID, the even ID, best of 
         format, system for picking and banning (example: 123412 t1_remove, t2_remove, t1_pick, t2_pick, t1_remove, t2_remove, left_over), 
         which map was removed by team 1, which map was returned by team 2, which map was removed by team 1 in a bo1 format 
         (this column has a lot of 0's since most matches were best of 3s) and so on. The main research question I wanted to answer is: 
         What are the most popular maps in CSGO?""")

col1, col2 = st.columns(2)

year_datasets = {
         '2016': '2016.csv',
         '2017': '2017.csv',
         '2018': '2018.csv',
         '2019': '2019.csv',
         '2020': '2020.csv',
         'All data': 'updated_file.csv'
}
event_datasets = {
         '3883': '3883.csv',
         '4597': '4597.csv',
         '4702': '4702.csv',
         'All data': 'updated_file.csv'
}

with col1:
   year = st.selectbox(
    "Select Year",
    list(year_datasets.keys()),
    key = "year"
   )

with col2:
   event_id = st.selectbox(
    "Select Event",
    list(event_datasets.keys()),
    key = "event_id"
   )

with st.container():
   label_dict = {1: 'Cache', 2: 'Cobblestone', 3: 'Dust2', 4: 'Inferno', 5: 'Mirage', 6: 'Nuke', 7: 'Overpass', 8: 'Train', 9: 'Vertigo'}
   # Load the data based on the user's event selection
   if event_id == "All data":
       data_pie = pd.read_csv(event_datasets[event_id])
   else:
       data_pie = pd.read_csv(f"{event_id}.csv")

   # Apply filters based on the user's year and event selections
   data_pie = data_pie[(data_pie["Year"] == year) | (data_pie["event_id"] == event_id)]

   data_pie["left_over"] = data_pie["left_over"].map(label_dict)

   counts = data_pie["left_over"].value_counts().reset_index()
   counts.columns = ["map", "count"]

   pop_map = alt.Chart(counts).mark_bar().encode(
   x=alt.X("count:Q", title="Count"),
   y=alt.Y("map:N", title="Map", axis=alt.Axis(labelOverlap='greedy')),
   color=alt.Color("count:Q", scale=alt.Scale(scheme="greens")),
   tooltip=["map", "count"]
   ).properties(
   title="Most Popular Left Over Map"
   )

   st.altair_chart(pop_map, use_container_width=True)

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

with st.container():

   data = pd.read_csv('ban_count.csv')

   click = alt.selection_multi(encodings=['color'])

   bars = alt.Chart(data).mark_bar(strokeWidth=1, stroke='black').encode(
   alt.X('count:Q', axis=alt.Axis(ticks=True), title="Count"),
   alt.Y('map_name:N', sort=alt.EncodingSortField('count', order='ascending'), title="Map Name"),
   color=alt.Color('colors:N', scale=None),
   angle=alt.Angle('map_name:N', sort=alt.EncodingSortField('count', order='ascending')),
   tooltip=['count:Q']
   ).properties(
   width=600,
   height=600
   ).configure_axis(
   grid=False
   ).add_selection(
   click
   )

   st.altair_chart(bars, use_container_width=False)
