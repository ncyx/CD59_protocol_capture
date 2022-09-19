#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:38:27 2022

@author: ncyx
"""
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

pd.set_option("display.max_rows", None, "display.max_columns", None)


''' The first part takes as input txt file with calculated RMSDs from BCL, renames column names, extracts rms. BCL txt file: deleted first row with this description '''


rmsd = pd.read_csv('/home/iwe24/Desktop/scripts_mine/I_sc_rms/RMSD.txt', sep="\s+", header = None)
rmsd.columns = ['description', 'rms']
rmsd_sorted = rmsd.sort_values('description')
rms_only = rmsd_sorted[['rms']]


''' I sorted here according to description, because BCL txt is sorted according to description. Then I reindexed column I_sc and created rms_Isc and then plotted it. '''


scores = pd.read_csv('/home/iwe24/Desktop/scripts_mine/I_sc_rms/Isc_sorted.csv', sep=",")
scores_sorted = scores.sort_values('description')


''' finally a normal file with correct rms/Isc/name combination...'''


rms_for_table = rmsd.sort_values('description')
rms_for_table.reset_index(drop = True, inplace = True)
I_sc_names = scores_sorted[['I_sc', 'description']]
I_sc_names.reset_index(drop=True, inplace=True)
rms_Isc_names = pd.concat([rms_for_table['rms'], I_sc_names], axis = 1)
# print(rms_Isc_names.head())
rms_Isc_names.to_csv('/home/iwe24/Desktop/scripts_mine/I_sc_rms/rms_Isc_description.csv')

''' Generates rms_Isc graph, takes as input rms_Isc_names which was created previously '''


def rms_Isc_graph(rms_and_I_sc):
    
    df = rms_and_I_sc
    # print(df)
    rms = df['rms']
    I_sc = df['I_sc']
    score_array = np.array(I_sc, dtype=float)
    rms_array = np.array(rms, dtype=float)
    
    fig, ax = plt.subplots()
    cm = plt.cm.get_cmap('viridis')
    cc = score_array
    sc = ax.scatter(rms_array, score_array, c = cc, s = 5, data=None, vmin = -40, vmax = 0, cmap=cm,)
    # ax.set_ylim(-35, 0)
    ax.set_title('Interface score vs RMSD')
    ax.set_xlabel('RMSD [$\AA$]')
    ax.set_ylabel('Rosetta Energy Units')
    plt.colorbar(sc, ax=ax)
    plt.savefig('I_sc_RMSD_run4_20k_abinitio', dpi=300)
    # # plt.savefig('high quality rmsd_colormap.png', dpi=300)
    plt.show()

rms_Isc_graph(rms_Isc_names)
