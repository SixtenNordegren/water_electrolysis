import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from galvani import BioLogic as BL
import pandas as pd

mpr_1 = BL.MPRfile('re_AgCl_we_PT_ce_PT_el_0.mpr')
mpr_2 = BL.MPRfile('re_AgCl_we_PT_ce_PT_el_2.mpr')
mpr_3 = BL.MPRfile('re_AgCl_we_PT_ce_PT_el_3.mpr')
mpr_4 = BL.MPRfile('re_AgCl_we_PT_ce_Ni_el_4.mpr')
mpr_5 = BL.MPRfile('re_AgCl_we_PT_ce_Au_el_5.mpr')
mpr_6 = BL.MPRfile('re_AgCl_we_PT_ce_Fe_el_6.mpr')
mpr_7 = BL.MPRfile('re_AgCl_we_PT_ce_Cu_el_7.mpr')
mpr_8 = BL.MPRfile('re_AgCl_we_PT_ce_Co_el_8.mpr')
mpr_9 = BL.MPRfile('re_AgCl_we_Au_ce_PT_el_9.mpr')
mpr_10 = BL.MPRfile('re_AgCl_we_Fe_ce_PT_el_10.mpr')
mpr_11 = BL.MPRfile('re_AgCl_we_Fe_ce_PT_el_11.mpr')
mpr_12 = BL.MPRfile('re_AgCl_we_Ni_ce_PT_el_12.mpr')
mpr_13 = BL.MPRfile('re_AgCl_we_Ni_ce_PT_el_12.mpr')
mpr_14 = BL.MPRfile('re_AgCl_we_Cu_ce_PT_el_13.mpr')
mpr_15 = BL.MPRfile('re_AgCl_we_Co_ce_PT_el_14.mpr')
mpr_16 = BL.MPRfile('re_AgCl_we_Pd_ce_PT_el_15.mpr')
mpr_17 = BL.MPRfile('re_AgCl_we_Pt_ce_PT_el_16.mpr')


area_list_we_testing = 1e-4 * np.array(
        [1.20, 0.85, 1.04, 0.60, 0.66, 0.27]
        ,[1.04, 1.04, 1.04, 1.04, 1.04, 1.04]
        )

area_list_ce_testing = 1e-4 * np.array(
        [1.04, 1.04, 1.04, 1.04, 1.04, 1.04],
        [1.28, 1.60, 1.70, 1.70, 1.60, 0.50])

data_list = [mpr_1, mpr_2, mpr_3, mpr_4, mpr_5, mpr_6, mpr_7, mpr_8, mpr_9, mpr_10, mpr_11, mpr_12, mpr_13, mpr_14, mpr_15, mpr_16]
data_frame_list = []
counter = 0

for df in data_list:
    data_frame_list.append(pd.DataFrame(df.data))

counter = 0

def average_cycle(df):
    """Takes a dataframe and returns two lists, the first
    containing the average current for each cycle and one with 
    the corresponding main potential"""

    cycle_list = []
    for i in range(1, 5):
        cycle_list.append(df.loc[df["cycle number"] == i]['Ewe/V'])

    average_list = np.average(cycle_list)
    potential_list = df['I/mA'][:len(df['Ewe/V'])]
    return average_list, potential_list
        
def current_density_converter(current_list, area_list):
    current_density_list = []
    counter = 0
    for df in data_frame_list:
        current_list / area_list[counter]
        counter += 1

def main():

if __name__ == "__main__":
    main()
