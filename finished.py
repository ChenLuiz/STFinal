import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

# loading data
data = pd.read_csv("picks.csv")

# Map list, pretty self explanatory tbh
map_list = ['Mirage', 'Inferno', 'Nuke', 'Vertigo', 'Overpass', 'Cache', 'Cobblestone', 'Dust2', 'Train']

# makes sure I don't have any data that doesn't belong in there
mask = ~data['left_over'].isin(map_list)
data = data.drop(index=data[mask].index)

# counts how many times each map has been played
map_counts = data.groupby('left_over').size().reset_index(name='Count')

# Normalize the count of times each map has been played
map_counts['Normalized Count'] = map_counts['Count'] / map_counts['Count'].sum()

# Manually ordinal encoding cause ordinal encoder function was giving me some funky results
data = data.replace('Cache', 1)
data = data.replace('Cobblestone', 2)
data = data.replace('Dust2', 3)
data = data.replace('Inferno', 4)
data = data.replace('Mirage', 5)
data = data.replace('Nuke', 6)
data = data.replace('Overpass', 7)
data = data.replace('Train', 8)
data = data.replace('Vertigo', 9)

# save normalized data into its own csv
map_counts.to_csv("normalized_map_counts.csv", index=False)

# export data to be visualized into updated_file.csv
data.to_csv('updated_file.csv', index=False)