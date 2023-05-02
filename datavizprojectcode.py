import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.title("Counter Strike - Global Offensive Pro Match Data Analysis")
# Disables stupid max rows for data input
alt.data_transformers.disable_max_rows()

st.subheader("Introduction")

st.write("""CSGO (Counter-Strike: Global Offensive) is a popular first-person shooter video game. 
Players are divided into two teams, terrorists and counter-terrorists, and must complete objectives or eliminate the opposing team. 
The game features a wide variety of weapons and equipment, and players earn money by completing objectives and killing enemies to purchase better gear. 
CSGO also has a competitive matchmaking mode where players can compete for rankings and prizes. The game requires strategy, communication, and quick reflexes.
In pro CSGO matches, teams ban maps until one is left, then take turns choosing the next map. 
Matches are best-of-three, with each team playing as both terrorists and counter-terrorists. 
The main research question I wanted to answer is: 
What are the most popular and most unpopular maps in CSGO?""")
st.write("""
The dataset used for this project is a CSGO csv database with map picks and vetos of matches between the top 30 teams. 
The data included is consisted of: date the match was played, team 1, team 2, inverted teams 
(which shows us which team started banning maps first), the match ID, the even ID, best of 
format, system for picking and banning (example: 123412 t1_remove, t2_remove, t1_pick, t2_pick, t1_remove, t2_remove, left_over), 
which map was removed by team 1, which map was returned by team 2, which map was removed by team 1 in a bo1 format 
(this column has a lot of 0's since most matches were best of 3s) and so on. My EDA revealed that a couple of interesting things about Normalization in this dataset:\n
Cache makes up 8% of maps played, Cobble makes up only 6%, Dust 2 makes up 9%, and Vertigo makes up only 1% of maps played. 
This is most likely because all of these maps were either removed from active duty earlier on or were added late into the game, or in Dust 2's case both.
Maps like Mirage (20%), Inferno(18%), and Overpass(12%) all have massive pickrates in comparisson because of how long they've been in the game untouched.""")

with st.container():
   label_dict = {1: 'Cache', 2: 'Cobblestone', 3: 'Dust2', 4: 'Inferno', 5: 'Mirage', 6: 'Nuke', 7: 'Overpass', 8: 'Train', 9: 'Vertigo'}
   data_pie = pd.read_csv('updated_file.csv')

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
   height=600,
   title = 'CS:GO Most Banned Maps'
   ).configure_axis(
   grid=False
   ).add_selection(
   click
   )

   st.altair_chart(bars, use_container_width=False)
   
with st.container():
    data_scatter = pd.read_csv('pick_count.csv')

    scatter_plot = alt.Chart(data_scatter).mark_circle(size=100, strokeWidth=1, stroke='black').encode(
    x=alt.X('Count_pick', axis=alt.Axis(title='Count Pick')),
    y=alt.Y('Count_ban', axis=alt.Axis(title='Count Ban')),
    color=alt.Color('colors:N', scale=None),
    tooltip=['Map Name', 'Count_pick', 'Count_ban']
    ).properties(
    title='Pick vs. Ban Rate of CS:GO Maps'
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)

with st.container():
         map_datasets = {
         'Cache': 'Cache.csv',
         'Cobblestone': 'Cobblestone.csv',
         'Dust 2': 'Dust_2.csv',
         'Inferno': 'Inferno.csv',
         'Mirage': 'Mirage.csv',
         'Nuke': 'Nuke.csv',
         'Overpass': 'Overpass.csv',
         'Train': 'Train.csv',
         'Vertigo': 'Vertigo.csv',
         'All data': 'updated_file.csv'
         }

         dataset_choice = st.selectbox('Select a dataset: ', list(map_datasets.keys()))

         data_chart1 = pd.read_csv(map_datasets[dataset_choice]).sort_values('date')
         data_chart1['date'] = pd.to_datetime(data_chart1['date'])
         label_dict = {1: 'Cache', 2: 'Cobblestone', 3: 'Dust2', 4: 'Inferno', 5: 'Mirage', 6: 'Nuke', 7: 'Overpass', 8: 'Train', 9: 'Vertigo'}

         Cumulative_maps = alt.Chart(data_chart1).transform_window(
         cumulative_count = "count()",
         sort=[{"field": "date"}],
         ).mark_area(color="white").encode(
         x = alt.X("date:T", title = "Date"),
         y = alt.Y("cumulative_count:Q", title = "Times it has been picked"),
         ).properties(
         title='Frequency of Maps Picked Over Time'
         )
         
         st.altair_chart(Cumulative_maps, use_container_width=True)
         
         st.write('''This part is funky but for some reason it works just fine on google colab and in VSCode :(. 
                  Example link:https://colab.research.google.com/drive/14WqhnyHRNt2TEapdior6P-32SOh4PJXm?usp=sharing''')

st.subheader("Conclusion")
         
st.write("""This project has given me more insight than I originally thought. However, looking back on it, I wish I had incoorporated the normalization more
into my visualizations. Regardless, there is still a lot to learn from them. It was interesting to see that Mirage and Inferno are both maps that are popular
amongst casual players and pros alike. It was also interesting to see that Dust 2 isn't more popular considering how popular it is with the majority of the playerbase.
It also has proven to be a whole lot more difficult than I originally thought it would be.
I ended up making over 20 different graphs to see which ones would be the best in this case but that went pretty horribly cause I wasted SO MUCH time.
I really wanted this last graph to work but it just seems to me like that's not gonna work so I'm gonna just go to bed now.""")
