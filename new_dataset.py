import pandas as pd

df = pd.read_csv("data_range_norm.csv.gz", compression="gzip")
columns = df.columns
print(df.head())



df_new = pd.read_csv("data_new_range.csv.zip", compression="zip")
df_new = df_new['loudness'].copy() # deep copy
min_loud = min(df_new)
print("old min=", min(df_new))
if(min_loud < 0):
    min_loud = abs(min_loud)
for i in range(len(df_new)):
    df_new[i] += min_loud
    # df_new._set_value(i,0,(df_new[i] + min_loud))
print("new min=", min(df_new))
max_loud = max(df_new)
for i in range(len(df_new)):
    df_new[i] /= max_loud
print("The new normalized min=%f and the max=%f"%(min(df_new), max(df_new)))


temp = {}
for c in columns:
    if(c=="loudness"):
        temp[c] = df_new
    else:
        temp[c] = df[c]

new_data = pd.DataFrame(temp)
print(new_data.head())

new_data.drop('year', inplace=True, axis=1)
new_data.drop('liveness', inplace=True, axis=1)
new_data.drop('duration_ms', inplace=True, axis=1)
new_data.drop('explicit', inplace=True, axis=1)
new_data.drop('valence', inplace=True, axis=1)
new_data.drop('mode', inplace=True, axis=1)

# dropping columns not extracted from querying the spotify api except for 'key'
new_data.to_csv("corrected_norm_data.csv.zip", compression="zip", index=False)