import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

origdata = pd.read_csv('data-us.csv')

# replacing the header
new_header = origdata.iloc[0]
origdata = origdata[1:]
origdata.columns = new_header

# split ppe needs into respective columns
# N95s
accepting = origdata['accepting']
origdata['N95'] = accepting.str.contains('N95s')

# select time and type of ppe
n95 = origdata[['timestamp', 'N95']]
# set True and False to be dummy variables
n95 = pd.get_dummies(n95, columns=['N95'])
# convert timestamp to DatetimeIndex
n95['timestamp'] = pd.to_datetime(n95['timestamp'])
n95 = n95.set_index(pd.DatetimeIndex(n95['timestamp']))
# sum needs by day
n95 = n95.resample('D').sum()
# calculate proportion of need
n95['prop'] = (n95['N95_True'] / (n95['N95_True'] + n95['N95_False'])) * 100
# reset timestamp to datetime64[ns]
n95 = n95.reset_index()
# assign weeks
n95['week'] = n95['timestamp'].dt.week - 11

# plot barplot (aggregated by week)
y = n95['prop']
x = n95['week']

sns.pointplot(x, y, join=False, ci='sd')
plt.title('N95 Masks')
plt.ylabel('%')
plt.xlabel('Week')
axes = plt.gca()
axes.set_ylim([0, 100])
plt.show()
