#must first run parser.py to generate cleaned datagrame

#use to generate value counts and resource usage percentages

#Credits to Benjamin Solecki's Amazon Access Challenge Solution
#https://github.com/bensolucky/Amazon

import pandas as pd
import numpy as np


df = pd.read_csv('cleaned.csv', header=0)
df = df.drop(['Unnamed: 0'], axis=1)

df = df.replace(r'^\s*$', np.nan, regex=True)
train = df.dropna()
train = train[['resource', 'manager', 'department', 'title', 'bufugu', 'business', 'ccode', 'dn']]
train.head()

X_all = train

# Adding Count Features for Each Column
print("Counts")
for col in X_all.columns:
    count = X_all[col].value_counts()
    X_all['count_'+col] = X_all[col].replace(count)


# usage percentages takes some time to run
for col in X_all.columns[1:8]:
    X_all['resource_usage_'+col] = 0.0
    counts = X_all.groupby([col, 'resource']).size()
    percents =  counts.groupby(level=0).transform(lambda x: x/sum(x))
    cc = 0
    print(col, len(percents))
    for c, r in percents.index:
        X_all.loc[(X_all[col]==c) & (X_all['resource']==r), 'resource_usage_'+ col] = percents[(c, r)]
        cc += 1
        if cc % 1000 == 1:
            print(cc)


# Number of Resources that a manager manages. I recall that many other similar
# features were tested, but this is the only that seemed to reliably move the
# needle.
m_r_counts = X_all.groupby(['manager', "resource"]).size()
m_counts = m_r_counts.groupby(level=0).size()
X_all['Manager_Resources'] = X_all['manager'].replace(m_counts)
dn_counts = X_all.groupby(['dn', "resource"]).size()
d_counts = dn_counts.groupby(level=0).size()
X_all['dn_Resources'] = X_all['dn'].replace(d_counts)


#save to csv
X_all.to_csv('newcounts.csv')
