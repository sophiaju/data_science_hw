import pandas as pd
import numpy as np

df = pd.read_csv("../data/IRAhandle_tweets_1.csv", sep=",")[:10000]

#print(df)

#just english tweets
df_eng = df.loc[df['language'] == 'English']
#print(df_eng)

#non question tweets
df_q = df_eng[~df_eng['content'].str.contains(r'\?.*')]
print(df_q)

#create new file with these tweets
df_q.to_csv('pruned_tweets.tsv', sep = '\t', index=False)

#new trump_mention feature
df_trump = df_q.assign(trump_mention = df_q['content'].str.contains(r'(\s|\W|\b)Trump(\s|\W|\b)'))

#get only the columns we want
df_pruned = df_trump[['tweet_id','publish_date','content','trump_mention']]
df_pruned.columns = df_pruned.columns.astype(str)
print(df_pruned)

value_counts = df_trump['trump_mention'].value_counts()
print(value_counts)

#get number of tweets with Trump
trump_true = value_counts.iloc[1]
print(value_counts.iloc[1])
#get total number of tweets
total = df_pruned.shape[0]

#save dataset to tsv
df_pruned.to_csv('../dataset.tsv', sep = '\t', index=False)
print(list(df_pruned))

#make result dataframe
df_results = pd.DataFrame(data = {'result':['frac-trump-mentions'], 'value': ['%.3f'% ((trump_true/total)*100)] })
print(df_results)

#save results to tsv
df_results.to_csv('../results.tsv', sep = '\t', index=False)