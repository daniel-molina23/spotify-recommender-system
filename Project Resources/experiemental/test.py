import pandas as pd
import time

# extract info
users_info = pd.read_csv('../results and analysis/all_user_information_with_genre.csv.zip', compression='zip', index_col=0)
print(users_info.head())
print(users_info.columns)

# drop the empty columns
import numpy as np
users_info.dropna(inplace=True)
print('length of data after NaN removal',len(users_info))
print('Number of unique genres: ',len(set(users_info['genre'])))

# remove quotations at the ends of the string
cols = list(users_info.columns)
col = cols.index('genre')
count = 0
time_sum = 0
hundredTimes = 0
start = time.time()
for i in range(len(users_info)):
	b = False
	if((users_info.iloc[i,col][0] == '\"' or users_info.iloc[i,col][0] == "\'") and (users_info.iloc[i,col][-1] == '\"' or users_info.iloc[i,col][-1] == "\'")):
		users_info.iloc[i,col] = users_info.iloc[i,col][1:-1]
		b = True
	else:
		if(users_info.iloc[i,col][0] == '\"' or users_info.iloc[i,col][0] == "\'"): #single or double quote
			users_info.iloc[i,col] = users_info.iloc[i,col][1:]
			b = True
		if(users_info.iloc[i,col][-1] == '\"' or users_info.iloc[i,col][-1] == "\'"):
			users_info.iloc[i,col] = users_info.iloc[i,col][:-1]
			b = True
	count = (count + 1) if(b) else count
	if(i%100 == 0):
		time_sum += (time.time() - start)
		hundredTimes += 1
		print('%dTH iteration with time of %f'%(i, time_sum/hundredTimes))
		start = time.time()
print('Number of modified rows: ', count)
