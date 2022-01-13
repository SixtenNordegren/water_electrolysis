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
Pl_Fe_I = data_frame_list[5]["I/mA"] / 1.04
Pl_Fe_V = data_frame_list[5]["Ewe/V"]

Pl_Fe_I_avg = average_cycle(data_frame_list[11], "I/mA") / 1.04
Pl_Fe_V_avg = average_cycle(data_frame_list[11], "Ewe/V")

ecd_oxygen = {
    "Platinum": ecd(Pl_Pl_I_avg, Pl_Pl_V_avg)[0],
    "Copper": ecd(Pl_Cu_I_avg, Pl_Cu_V_avg)[0],
    "Gold": ecd(Pl_Au_I_avg, Pl_Au_I_avg)[0],
    "Nickel": ecd(Pl_Ni_I_avg, Pl_Ni_V_avg)[0],
    "Iron": ecd(Pl_Fe_I_avg, Pl_Fe_V_avg)[0],
}

ecd_hydrogen = {
    "Platinum": ecd(Pl_Pl_I_avg, Pl_Pl_V_avg)[1],
    "Copper": ecd(Pl_Cu_I_avg, Pl_Cu_V_avg)[1],
    "Gold": ecd(Pl_Au_I_avg, Pl_Au_I_avg)[1],
    "Nickel": ecd(Pl_Ni_I_avg, Pl_Ni_V_avg)[1],
    "Iron": ecd(Pl_Fe_I_avg, Pl_Fe_V_avg)[1],
}


def main():
    fig, axs = plt.subplots(1, 4, sharey=True)
    axs[0].plot(Pl_Pl_V_avg, Pl_Pl_I_avg)
    axs[1].plot(Pl_Cu_V_avg, Pl_Cu_I_avg)
    axs[2].plot(Pl_Fe_V_avg, Pl_Fe_I_avg)
    axs[3].plot(Pl_Ni_V_avg, Pl_Ni_I_avg)

    counter = 0
    for i in axs:
        axs[counter].grid()
        axs[counter].set_xlabel("E (V)")

        counter += 1
    axs[0].set_title("Platinum")
    axs[1].set_title("Copper")
    axs[2].set_title("Iron")
    axs[3].set_title("Nickel")

    axs[0].set_ylabel("i (mA/cm^2)")

    plt_name = "plots/multiplot_avg_li.pdf"
    if os.path.isfile(plt_name) == True:
        os.remove(plt_name)
    plt.savefig(plt_name, type="pdf")
    plt.show()

    Slope_Pl_hydrogen = TafelSlope(Pl_Pl_V_avg, ecd_hydrogen["Platinum"], Pl_Pl_I_avg)
    
    Pl_I, Pl_V = list_cropper_2(Pl_Pl_I_avg, Pl_Pl_V_avg, n=6, peak="min")
    # Pl_I, Pl_V = list_cropper_2(Pl_Pl_I_avg, Pl_Pl_V_avg, n=6, peak="max")

    taf = Tafel_OP(Pl_I, ecd_hydrogen["Platinum"], Slope_Pl_hydrogen)
    plt.plot(
        1*Pl_I,
        1*taf,
        label="Theoretical prediction",
    )
    plt.plot(Pl_I, Pl_V, label="Collected data")
    plt.legend()
    plt.grid()

    plt_name = "plots/fin.pdf"
    plt.xlabel("Current density i (mA / cm^2)")
    plt.ylabel("Potential E (V)")
    if os.path.isfile(plt_name) == True:
        os.remove(plt_name)
    plt.savefig(plt_name, type="pdf")
    plt.show()

    print(Slope_Pl_hydrogen)

# def main():

    # Pl_I, Pl_V = list_cropper_2(Pl_Pl_I_avg, Pl_Pl_V_avg, n=8, peak="max")
    # m, k = least_sqaures(Pl_I, Pl_V)
    # x = np.linspace(0, 21, num=1000)
    # regression = [y for y in m + k * x]

    # Pl_I, Pl_V = list_cropper_2(Pl_Pl_I_avg, Pl_Pl_V_avg, n=3, peak="max")
    # plt.plot(Pl_V, Pl_I)
    # plt.plot(regression, x)

    # x_axis = np.linspace(0.25,1.3, 1000)


    # plt.plot(x_axis, np.zeros((1000)), color='black', label="Platinum data")
    # plt.scatter(regression[0], 0, s=5000, facecolors='none', edgecolors='red', label="Current exchange density")

    # plt.xlabel("Current density i (mA/cm^2)")
    # plt.ylabel("Potential E (V)")
    # plt.grid()
    # plt.savefig("plots/pl_current_exchange_density.pdf", format="pdf")
    # plt.show()


if __name__ == "__main__":
    main()
