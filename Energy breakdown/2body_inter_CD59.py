#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:53:05 2022

@author: iwe24
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('/home/iwe24/Desktop/scripts_mine/energy_breakdown_extract/energy_breakdown_top12.out', sep="\s+", index_col = 0) #takes as input energy_breakdown file 
# print(df.head())
inter_resis = df[['resi1', 'pdbid1', 'resi2', 'pdbid2']]
two_body = df[83:] #here I select only 2-body interactions from the data set
# print(type(two_body))
condition_only_chA = two_body['pdbid1'].str.contains('A')
two_body_chA = two_body[condition_only_chA]

condition_inter_AB = two_body_chA['pdbid2'].str.contains('B')
CD59_pep_inter_resi = two_body_chA[condition_inter_AB] #in principle you can do it in one line, but I wanted to check different columns and defined boolean variables


# CD59_pep_inter_resi.to_csv('/home/iwe24/Desktop/scripts_mine/energy_breakdown_extract/2_body_interactions_AF2_run4_total.csv')

'''For seaborn CD59_resi and pep_resi should be defined and total_score plotted: '''

CD59_seaborn = CD59_pep_inter_resi['resi1']
pep_seaborn = CD59_pep_inter_resi['resi2']
score_seaborn = CD59_pep_inter_resi['total']

data_seaborn = pd.concat([CD59_seaborn, pep_seaborn, score_seaborn], axis = 1)
data_seaborn = data_seaborn.rename(columns = {'resi1':'CD59', 'resi2':'peptide', 'total':'score'}) #redefining names of columns for my graph 
data_seaborn = data_seaborn.pivot(columns = 'peptide', index = 'CD59', values = 'score')
print(data_seaborn)

y_ticklabels_CD59 = []
x_ticklabels_pep = ['D', 'V', 'S', 'L', 'A', 'F', 'S', 'E'] #aa-labels of my peptide. You can put whatever you want... 

for i in range(len(CD59_pep_inter_resi['restype1'])):
    if CD59_pep_inter_resi['restype1'][i] + ' '+ str(CD59_pep_inter_resi['resi1'][i]) not in y_ticklabels_CD59:
        y_ticklabels_CD59.append(CD59_pep_inter_resi['restype1'][i] + ' '+ str(CD59_pep_inter_resi['resi1'][i])) #here I just generate labels for the graph
        
print(y_ticklabels_CD59)
        
'''graph begins here'''

fig, ax = plt.subplots()
sns.heatmap(data_seaborn, ax = ax, annot = True, cmap='mako', vmin = -8, vmax = 0, xticklabels = True, yticklabels = True)
ax.set_yticklabels(y_ticklabels_CD59, fontsize = 8, rotation = 0)
ax.set_xticklabels(x_ticklabels_pep, fontsize = 10)
# plt.yticks(rotation=45, fontsize = 8)
ax.set_title('Energy breakdown')
plt.savefig('run4_20k_top1_Isc', dpi=300, bbox_inches = 'tight')
plt.show()

# data_seaborn = data_seaborn.pivot('CD59', 'pep', 'score')
