import numpy as np
import math as m
import matplotlib.pyplot as plt
import os

from galvani import BioLogic as BL
import pandas as pd

from function_sheet import *

mpr_0 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_0.mpr")
mpr_1 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_2.mpr")
mpr_2 = BL.MPRfile("data/re_AgCl_we_PT_ce_PT_el_3.mpr")
mpr_3 = BL.MPRfile("data/re_AgCl_we_PT_ce_Ni_el_4.mpr")
mpr_4 = BL.MPRfile("data/re_AgCl_we_PT_ce_Au_el_5.mpr")
mpr_5 = BL.MPRfile("data/re_AgCl_we_PT_ce_Fe_el_6.mpr")
mpr_6 = BL.MPRfile("data/re_AgCl_we_PT_ce_Cu_el_7.mpr")
mpr_7 = BL.MPRfile("data/re_AgCl_we_PT_ce_Co_el_8.mpr")
mpr_8 = BL.MPRfile("data/re_AgCl_we_Au_ce_PT_el_9.mpr")
mpr_9 = BL.MPRfile("data/re_AgCl_we_Fe_ce_PT_el_10.mpr")
mpr_10 = BL.MPRfile("data/re_AgCl_we_Fe_ce_PT_el_11.mpr")
mpr_11 = BL.MPRfile("data/re_AgCl_we_Ni_ce_PT_el_12.mpr")
mpr_12 = BL.MPRfile("data/re_AgCl_we_Cu_ce_PT_el_13.mpr")
mpr_13 = BL.MPRfile("data/re_AgCl_we_Co_ce_PT_el_14.mpr")
mpr_14 = BL.MPRfile("data/re_AgCl_we_Pd_ce_PT_el_15.mpr")
mpr_15 = BL.MPRfile("data/re_AgCl_we_Pt_ce_PT_el_16.mpr")

data_list = [
    mpr_0,
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
]

data_frame_list = []

for df in data_list:
    data_frame_list.append(pd.DataFrame(df.data))

# Using the list_beautifier function is sort of a necessary evil. And not really
# an optimal solution. However it's better than the alternatives. I might go
# into more details about it in an external reference file.


# Important lists for current densities:
# Currently these current densities are in mA/cm^2 units.

# Platinum Platinum.
Pl_Pl_I = data_frame_list[2]["I/mA"] / 1.20
Pl_Pl_V = data_frame_list[2]["Ewe/V"]

Pl_Pl_I_avg = average_cycle(data_frame_list[2], "I/mA") / 1.20
Pl_Pl_V_avg = average_cycle(data_frame_list[2], "Ewe/V")

# Platinum nickel
Pl_Ni_I = data_frame_list[11]["I/mA"] / 0.85
Pl_Ni_V = data_frame_list[11]["Ewe/V"]

Pl_Ni_I_avg = average_cycle(data_frame_list[11], "I/mA") / 0.85
Pl_Ni_V_avg = average_cycle(data_frame_list[11], "Ewe/V")

# Platinum copper
Pl_Cu_I = data_frame_list[12]["I/mA"] / 0.66
Pl_Cu_V = data_frame_list[12]["Ewe/V"]

Pl_Cu_I_avg = average_cycle(data_frame_list[12], "I/mA") / 0.66
Pl_Cu_V_avg = average_cycle(data_frame_list[12], "Ewe/V")

# Platinum gold
Pl_Au_I = data_frame_list[8]["I/mA"] / 1.04
Pl_Au_V = data_frame_list[8]["Ewe/V"]

Pl_Au_I_avg = average_cycle(data_frame_list[8], "I/mA") / 1.04
Pl_Au_V_avg = average_cycle(data_frame_list[8], "Ewe/V")

# Platinum iron
Pl_Fe_I = data_frame_list[10]["I/mA"] / 1.04
Pl_Fe_V = data_frame_list[10]["Ewe/V"]

Pl_Fe_I_avg = average_cycle(data_frame_list[10], "I/mA") / 1.04
Pl_Fe_V_avg = average_cycle(data_frame_list[10], "Ewe/V")


def main():

    # It's worth noting that during our experiment we ploted the current
    # vs the potential. But if we want m to be the ecd_oxygen we need the current
    # density on the x axis. I need to write this down somewhere bucause I
    # will forget it.

    # Exchange current densities

    ecd_oxygen = {
        "Platinum": ecd(Pl_Pl_I_avg, Pl_Pl_V_avg)[0],
        "Copper": ecd(Pl_Cu_I_avg, Pl_Cu_V_avg)[0],
        "Gold": ecd(Pl_Au_I_avg, Pl_Au_I_avg)[0],
        "Nickel": ecd(Pl_Ni_I_avg, Pl_Ni_V_avg)[0],
        "Iron" : ecd(Pl_Fe_I_avg, Pl_Fe_V_avg)[0]
    }

    ecd_hydrogen = {
        "Platinum": ecd(Pl_Pl_I_avg, Pl_Pl_V_avg)[1],
        "Copper": ecd(Pl_Cu_I_avg, Pl_Cu_V_avg)[1],
        "Gold": ecd(Pl_Au_I_avg, Pl_Au_I_avg)[1],
        "Nickel": ecd(Pl_Ni_I_avg, Pl_Ni_V_avg)[1],
        "Iron" : ecd(Pl_Fe_I_avg, Pl_Fe_V_avg)[1]
    }

    print("Oxygen Exchange current densities:")
    for key in ecd_oxygen:
        print("{0} & {1} \\\\ \n".format(key, np.around(ecd_oxygen[key], 3)))

    print("\nHydrogen Exchange current densities")
    for key in ecd_hydrogen:
        print("{0} & {1} \\\\ \n".format(key, np.around(ecd_hydrogen[key], 3)))


    # x, y = list_cropper_2(Pl_Pl_I_avg, Pl_Pl_V_avg, n=12, peak="min")
    # x = np.log10(-1 * np.array(x))
    # m, k = least_sqaures(x, -1 * y)
    # regression = [i for i in m + k * np.array(x)]

    log_i = -1 * np.log10(-1 * np.array(Pl_Pl_I_avg))
    x_ni, y_ni = list_cropper_2(log_i, Pl_Pl_V_avg, n = 8, peak="min")
    # x_ni, y_ni = -1 * x_ni, -1 * y_ni

    m_ni, k_ni = least_sqaures(x_ni, y_ni)
    regression_ni = [i for i in m_ni + k_ni * np.array(x_ni)]

    plt.plot(x_ni, y_ni, ".", label ="Hydrogen Cropped data")
    plt.plot(x_ni, regression_ni, label="Hydrogen linear regresion")

    log_i = np.log10(np.array(Pl_Pl_I_avg))
    x_ni, y_ni = list_cropper_2(log_i, Pl_Pl_V_avg, n = 6, peak="max")

    m_ni, k_ni = least_sqaures(x_ni, y_ni)
    regression_ni = [i for i in m_ni + k_ni * np.array(x_ni)]

    plt.plot(x_ni, y_ni, ".", label ="Oxygen Cropped data")
    plt.plot(x_ni, regression_ni, label ="Oxygen linear regression" )
    plt.grid()
    plt.xlabel("Current density (i)")
    plt.ylabel("Potentail (V)")
    plt_name = "plots/Cropped_data.pdf"
    plt.legend()

    if os.path.isfile(plt_name):
        os.remove(plt_name)
    plt.savefig(plt_name, type="pdf")
    plt.show()


if __name__ == "__main__":
    main()
