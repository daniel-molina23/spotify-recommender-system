import zipfile
import pandas as pd
import numpy as np


zf = zipfile.ZipFile('artist_to_genre.zip') 
genre = pd.read_csv(zf.open('artists.csv'))
print(genre.head())
print(len(genre))
artist_map = {}

for i in range(len(genre)):
    gen = genre.iloc[i,2]
    gen = gen.strip('][').strip("'").split(',') # remove brackets and quotations, then split by comma
    artist = genre.iloc[i,3]
    if(len(gen) > 0 and gen[0] != '' and artist not in artist_map):
        artist_map[artist] = gen[0]


total = pd.read_csv('all_user_information_total.csv.zip', compression='zip', index_col=0)
print(total.head())
print("total columns before: ", len(total.columns))



ls = []
# running a for loop and assigning some values to series
for i in range(len(total)):
    val = artist_map.get(total.iloc[i,1], np.nan) # retrieve genre if artist present, else NaN
    ls.append(val)


column_values = pd.Series(ls)

# inserting new column with values of list made above       
total.insert(loc=2, column='genre', value=column_values)

print(total.head())
print("total columns after: ", len(total.columns))
val = total['genre'].isna().sum()
print("total length BEFORE removing null values: ", len(total))
print("total null values in genre column: ", val)
print("rows AFTER removing null values: ", (len(total)-val))

# total.to_csv("all_user_info_clustering.csv.zip", compression='zip')