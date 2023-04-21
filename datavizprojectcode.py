import streamlit as st
import numpy as np

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Select Year",
    ("2016", "2017, "2018, "2019", "2020")
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
   add_selectbox = st.selectbox(
    "Select Year",
    ("2016", "2017, "2018, "2019", "2020")

with col2:
   add_selectbox = st.selectbox(
    "Select Map",
    ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train")

with col3:
   add_selectbox = st.selectbox(
    "Select Event",
    ("Kato", "IEM", "Blast", "ESL")

# Container with graph
with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")

# Second chart
# Columns for chart/controls
col4, cols5 = st.columns(2)


with col4:
   add_selectbox = st.selectbox(
    "Select Year",
    ("2016", "2017, "2018, "2019", "2020")
       
   add_selectbox = st.selectbox(
    "Select Map",
    ("Mirage", "Inferno", "Nuke", "Overpass", "Cobblestone", "Dust 2", "Vertigo", "Cache", "Train")
   
   add_selectbox = st.selectbox(
    "Select Event",
    ("Kato", "IEM", "Blast", "ESL")

with col5:
   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))
