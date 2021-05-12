import pandas as pd

#read the 'distances_total.csv' dataset using pandas
df = pd.read_csv('results and analysis\distances_total.csv', sep=',')

# Sort first by average_distance, then by variance if tied
sorted = (df.sort_values(by=['averages_distance', 'variances_distance'], ascending=True))

top10 = sorted.head(10)

print("Users to follow: ")
count = 1
for index, row in top10.iterrows():
    print(str(count) + ") " + row['user'])
    count += 1
