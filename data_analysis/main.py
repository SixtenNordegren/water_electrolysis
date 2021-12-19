import numpy as np
import math as m
import matplotlib.pyplot as plt

from galvani import BioLogic as BL
import pandas as pd

mpr_0 = BL.MPRfile("re_AgCl_we_PT_ce_PT_el_0.mpr")
mpr_1 = BL.MPRfile("re_AgCl_we_PT_ce_PT_el_2.mpr")
mpr_2 = BL.MPRfile("re_AgCl_we_PT_ce_PT_el_3.mpr")
mpr_3 = BL.MPRfile("re_AgCl_we_PT_ce_Ni_el_4.mpr")
mpr_4 = BL.MPRfile("re_AgCl_we_PT_ce_Au_el_5.mpr")
mpr_5 = BL.MPRfile("re_AgCl_we_PT_ce_Fe_el_6.mpr")
mpr_6 = BL.MPRfile("re_AgCl_we_PT_ce_Cu_el_7.mpr")
mpr_7 = BL.MPRfile("re_AgCl_we_PT_ce_Co_el_8.mpr")
mpr_8 = BL.MPRfile("re_AgCl_we_Au_ce_PT_el_9.mpr")
mpr_9 = BL.MPRfile("re_AgCl_we_Fe_ce_PT_el_10.mpr")
mpr_10 = BL.MPRfile("re_AgCl_we_Fe_ce_PT_el_11.mpr")
mpr_11 = BL.MPRfile("re_AgCl_we_Ni_ce_PT_el_12.mpr")
mpr_12 = BL.MPRfile("re_AgCl_we_Cu_ce_PT_el_13.mpr")
mpr_13 = BL.MPRfile("re_AgCl_we_Co_ce_PT_el_14.mpr")
mpr_14 = BL.MPRfile("re_AgCl_we_Pd_ce_PT_el_15.mpr")
mpr_15 = BL.MPRfile("re_AgCl_we_Pt_ce_PT_el_16.mpr")


# area_list_we_testing = 1e-4 * np.array(
# [1.20, 0.85, 1.04, 0.60, 0.66, 0.27]
# ,[1.04, 1.04, 1.04, 1.04, 1.04, 1.04]
# )

# area_list_ce_testing = 1e-4 * np.array(
# [1.04, 1.04, 1.04, 1.04, 1.04, 1.04],
# [1.28, 1.60, 1.70, 1.70, 1.60, 0.50])

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


def average_cycle(df):
    """Takes a dataframe and returns two lists, the first
    containing the average current for each cycle and one with
    the corresponding main potential"""

    cycle_list = []
    for i in range(1, 5):
        cycle_list.append(df.loc[df["cycle number"] == i]["Ewe/V"])

    average_list = np.average(cycle_list)
    potential_list = df["I/mA"][: len(df["Ewe/V"])]
    print(potential_list)
    return average_list, potential_list


# Important lists for current densities:

# Platinum Platinum.
Pl_Pl_I = data_frame_list[2]["I/mA"] / 1.20
Pl_Pl_V = data_frame_list[2]["Ewe/V"]
# Platinum nickel
Pl_Ni = data_frame_list[11]["I/mA"] / 0.85
Pl_Ni_V = data_frame_list[11]["Ewe/V"]
# Platinum copper
Pl_Cu = data_frame_list[12]["I/mA"] / 0.66
Pl_Cu_V = data_frame_list[12]["Ewe/V"]
# Platinum gold
Pl_Au = data_frame_list[8]["I/mA"] / 1.04
Pl_Au_V = data_frame_list[8]["Ewe/V"]


# Exchange current density dictionary.
ecd_dict = {
    "Palladium": 3.0,
    "Platinum": 3.1,
    "Rhodium": 3.6,
    "Iridium": 3.7,
    "Nickel": 5.2,
    "Gold": 5.4,
    "Tungsten": 5.9,
    "Niobium": 6.8,
    "Titanium": 8.2,
    "Cadmium": 10.8,
    "Manganese": 10.9,
    "Lead": 12.0,
    "Mercury": 12.3,
}

# I found this list on the Wikipedia page for exchange current densities.
# https://en.wikipedia.org/wiki/Exchange_current_density


def Tafel_OP(cd, ecd, alpha=1):
    """
    Returns the overpotential from current density and exchange current
    density.
    ecd - exchange current density
    cd - short for current density
    alpha - Is the charge transfer coefficient. This is supposed a value
    between 1 and 0. I'm not sure how to determining it so I'm leaving it
    as one for the time being.
    """
    Lambda = m.log(10)
    k = 1.38e-23  # J/K
    T = 293.0  # K
    e = 1.602e-19  # J

    A = Lambda * k * T / (e * alpha)

    ans = []
    # This rather awkward IF statement is here to replace the plus minus sign
    # in the Tafel equation. The plus sign in the Tafel is if the equation
    # is an anode and minus if it's a cathode. During our experiment however
    # we switch polarity between the electrodes during our measurement. This
    # IF statement takes this into account.
    for i in cd:
        if i >= 0:
            ans.append(A * m.log(i / ecd) / m.log(10))
        else:
            # Here we take the absolute value of the current density.
            # The practical reason for doing this is that we cant solve
            # for negative values of a logarithm*. We can justify
            # this in multiple ways. I start out with listing two.
            # the sign of a current really only signifies its direction
            # so when we talk about current density it really doesn't
            # make a lot of sense to talk about a direction so what we
            # really should have done is taken the absolute value from
            # when we make the current density list. The other reason
            # could be that when we observe negative currents in the
            # Tafel equation we really already take two cases into account.
            # When the current is either positive or negative and our
            # treatment of the electrode as a cathode is what it means
            # to take the sign into account.
            ans.append(-A * m.log(abs(i) / ecd) / m.log(10))
    return np.array(ans)


def Tafel_CD(op, ecd, alpha=1):
    """
    Returns the current density from a known over potential
    """
    Lambda = m.log(10)
    k = 1.38e-23  # J/K
    T = 293.0  # K
    e = 1.602e-19  # J

    ans = []
    for i in cd:
        if i >= 0:
            ans.append(ecd * np.exp(m.log(10) * op / A))
        else:
            ans.append(ecd * np.exp(-m.log(10) * op / A))
    return np.array(ans)


def main():
    Tafel_CD(1.23)


if __name__ == "__main__":
    main()
