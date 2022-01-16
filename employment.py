#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt

# Read data - reading a csv file is much, much quicker than an Excel file. So save file as CSV, then read.
# df stands for 'DataFrame', which is the object that pandas uses
df_data = pd.read_csv('data.csv',header=3,usecols=range(6))

# Rename columns to make them easier to reference
cols = df_data.columns.tolist()
new_cols = ['Date', 'Sex', 'States', 'Occupation', "Employed ('000)", "Hours ('000)"]
df_renamed = df_data.rename(columns=dict(zip(cols,new_cols)))

# Convert date (str) to datetime format
df_renamed['Date'] = pd.to_datetime(df_renamed['Date'])

# Get list of state & territory names
states = df_renamed['States'].unique().tolist()

# Filter DataFrame for Occupations that contain the string 'ICT'
df_filt = df_renamed[df_renamed['Occupation'].str.contains('ICT')]

## By nation
# Cross-tabulate data to group & summarise it by relevant categories
df = pd.crosstab(index=df_filt['Date'], columns=df_filt['Sex'], values=df_filt["Employed (\'000)"], aggfunc='sum')
df_res = df.resample(rule='Y').sum()
ax=df.plot()
ax.set_title('National')
ax.set_ylabel('Employed (\'000)')
plt.gcf().savefig('national_plot.png')


## By state
# Cross-tabulate data to group & summarise it by relevant categories
df_ct = pd.crosstab(index=df_filt['Date'], columns=[df_filt['States'],df_filt['Sex']], values=df_filt["Employed (\'000)"], aggfunc='sum')

# Get dataframes for each state - take a cross section of the df at each state
df_states = [df_ct.xs(states[i], axis=1) for i in range(len(states))]

# Separate plots per states
for i in range(len(states)):
    df = df_states[i]
    state = states[i]

    ax = df.plot()
    ax.set_title(state)
    ax.set_xticklabels([dt.strftime("%Y") for dt in df_res.index]);
    fig = plt.gcf().savefig(state+'_plot.png')

# One big plot with all states
fig,axes = plt.subplots(4,2,figsize=(15,30),sharex=True)
for i in range(len(states)):
    df = df_states[i]
    state = states[i]
    axi = df.plot()
    axi.set_title(state)
fig.savefig('all_states_plot.png')
