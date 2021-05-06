import pandas as pd
import zipfile


r = []
d = []
val = [(0,250), (250,500), (500,750), (750,950), (950,975), (976,1002)]

for s,e in val:
    fileS = "all_user_information_%d_%d.csv.zip"%(s,e)
    fileD = "distances_%d_%d.csv"%(s,e)
    df = pd.read_csv(fileS, compression='zip', index_col=0)
    df2 = pd.read_csv(fileD)
    r.append(df)
    d.append(df2)

total = pd.concat(r)
print(total.head())
print(len(total))

dist = pd.concat(d)
print(dist.head())
print(len(dist))

total.to_csv("all_user_information_total.csv.zip", compression='zip')
dist.to_csv("distances_total.csv")
