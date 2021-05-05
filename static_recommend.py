import pandas as pd
import numpy as numpy

#idk how to read the csv and stuff
distances = pd.read_csv("distances-7501001-1.csv",)


subset = distances[['user', 'averages_distance', 'variances_distance']]
distances_tuples = [tuple(x) for x in subset.to_numpy()]

# Sort first by average_distance, then by variance if tied
distances_tuples.sort(key=lambda x: (x[1], x[2]))


counter = 1
for x in distances_tuples[:10]:
    print(str(counter) + ") " + x[0])
    counter+=1