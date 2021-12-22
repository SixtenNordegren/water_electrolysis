import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from galvani import BioLogic as BL
import pandas as pd

mpr_1 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_0.mpr")
mpr_2 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_2.mpr")
mpr_3 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_3.mpr")
mpr_4 = BL.MPRfile("data/re_AgCl_we_PT_ce_Ni_el_4.mpr")
mpr_5 = BL.MPRfile("data/re_AgCl_we_PT_ce_Au_el_5.mpr")
mpr_6 = BL.MPRfile("data/re_AgCl_we_PT_ce_Fe_el_6.mpr")
mpr_7 = BL.MPRfile("data/re_AgCl_we_PT_ce_Cu_el_7.mpr")
mpr_8 = BL.MPRfile("data/re_AgCl_we_PT_ce_Co_el_8.mpr")
mpr_9 = BL.MPRfile("data/re_AgCl_we_Au_ce_PT_el_9.mpr")
mpr_10 = BL.MPRfile("data/re_AgCl_we_Fe_ce_PT_el_10.mpr")
mpr_11 = BL.MPRfile("data/re_AgCl_we_Fe_ce_PT_el_11.mpr")
mpr_12 = BL.MPRfile("data/re_AgCl_we_Ni_ce_PT_el_12.mpr")
mpr_13 = BL.MPRfile("data/re_AgCl_we_Ni_ce_PT_el_12.mpr")
mpr_14 = BL.MPRfile("data/re_AgCl_we_Cu_ce_PT_el_13.mpr")
mpr_15 = BL.MPRfile("data/re_AgCl_we_Co_ce_PT_el_14.mpr")
mpr_16 = BL.MPRfile("data/re_AgCl_we_Pd_ce_PT_el_15.mpr")
mpr_17 = BL.MPRfile("data/re_AgCl_we_Pt_ce_PT_el_16.mpr")

data_list = [
    mpr_1,
    mpr_2,
    mpr_3,
    mpr_4,
    mpr_5,
    mpr_6,
    mpr_7,
    mpr_8,
    mpr_9,
    mpr_10,
    mpr_11,
    mpr_12,
    mpr_13,
    mpr_14,
    mpr_15,
    mpr_16,
]
data_frame_list = []

for df in data_list:
    data_frame_list.append(pd.DataFrame(df.data))

A = 1 * 2 + 3 / 4

B = 2 + 3 - 4


def main():
    counter = 1
    for data in data_frame_list:
        plot_name = "plots/data_plot_" + str(counter)
        if os.path.isfile(plot_name):
            os.remove(plot_name)

        plt.plot(data["Ewe/V"], data["I/mA"])
        plt.xlabel("Something new.")
        plt.savefig(plot_name)
        plt.close()
        counter += 1


if __name__ == "__main__":
    main()
