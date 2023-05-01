import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Select Year",
    ("2016", "2017", "2018", "2019", "2020"),
    key = "Sidebar"
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Select Map",
        ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train")
    )

# Columns with individual controls
col1, col2, col3 = st.columns(3)


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

# Container with graph
with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   label_dict = {1: 'Cache', 2: 'Cobblestone', 3: 'Dust2', 4: 'Inferno', 5: 'Mirage', 6: 'Nuke', 7: 'Overpass', 8: 'Train', 9: 'Vertigo'}

   data_chart1 = pd.read_csv('updated_file.csv')
   data_chart1_labels = pd.DataFrame({'Map': label_dict.values()})

   # create a chart with the area mark
   Cumulative_maps = alt.Chart(data_chart1).transform_window(
        cumulative_count = "count()",
        sort=[{"field": "left_over"}],
        #tooltip = ['left_over']
   ).mark_area(color="darkseagreen").encode(
        x = alt.X("left_over:Q", title = "Map", axis=alt.Axis(values=[1, 2, 3, 4, 5, 6, 7, 8, 9])),
        y = alt.Y("cumulative_count:Q", title = "Times it has been picked"),
   )

   # create a chart with the vertical lines
   Map_ticks = alt.Chart(data_chart1_labels).mark_rule(color='seagreen', strokeWidth=5).encode(
        x=alt.X('Map:N', axis=None),
   )

   # layer the two charts and show the result
   st.altair_chart(Cumulative_maps + Map_ticks, use_container_width=True)

st.write("This is outside the container")

# Second chart
# Columns for chart/controls
col4, col5 = st.columns(2)


with col4:
   add_selectbox5 = st.selectbox(
    "Select Year",
    ("2016", "2017", "2018", "2019", "2020"),
    key = "col4"
   )

   add_selectbox6 = st.selectbox(
    "Select Map",
    ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train"),
    key = "col4-1"
   )
    
   add_selectbox7 = st.selectbox(
    "Select Event",
    ("Kato", "IEM", "Blast", "ESL"),
    key = "col4-2"
   )

with col5:
   # You can call any Streamlit command, including custom components:
   data = pd.read_csv('ban_count.csv')

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
    ).interactive()

    st.altair_chart(bars, use_container_width=True)

