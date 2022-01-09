import numpy as np
import math as m
import matplotlib.pyplot as plt

from galvani import BioLogic as BL
import pandas as pd

op_H = 0.77
op_O = 0.45


def list_beautifier(B):
    """Takes a list of lists and compares their length. Shortens the longer ones
    until they are all of the same length."""

    A = B.copy()
    for i in range(len(A)):
        if i == 0:
            length = len(A[0])

        elif length > len(A[i]):
            length = len(A[i])

    for i in range(len(A)):
        A[i] = A[i][:length]

    return A


def average_cycle(df, column_name):
    """Takes a dataframe and returns two lists, the first
    containing the average current for each cycle and one with
    the corresponding main potential"""

    cycle_list = []
    for i in range(1, 5):
        bullet = df.loc[df["cycle number"] == i][column_name].to_numpy()
        cycle_list.append(bullet)

    average_list = np.average(list_beautifier(cycle_list), axis=0)
    return average_list


def list_cropper(A, n=5):
    """
    Returns a list with the top 1 / n largest elements of that list.

    This function does care about the sign of element. So -12 is smaller
    than +1.

    This function should also keep the order of the elements in a given
    list.
    """

    B = []

    for element in A:
        if len(B) == len(A) // n:
            C = B.copy()
            C.sort()
            if element > C[0]:
                B.remove(C[0])  # We know this is sin
                B.append(element)
        else:
            B.append(element)
    return B


def list_cropper_2(X, Y, n=6, peak="max"):

    """
    Takes a list of floats and integers. Returns the largest numbers in
    an environment around it's largest point.

    Then retuns another list "X" that is the correstopinding coordinates
    for "Y" to be plotted against and returns both "X" and "Y" cropped by
    the same inexes.

    If peak is set to anything but max it will reutrn a point around it's
    smalles point instead of its largets.

    This function does care about the sign of the element. So -12 is
    smaller than +1 etc.

    This function should also keep the order of the elements in a given
    list.
    """

    Y = Y.tolist()
    X = X.tolist()

    B = Y.copy()
    C = Y.copy()

    rope_lenght = len(C) // (2 * n)

    B.sort()
    if peak == "max":
        maximum = B[-1]
    else:
        maximum = B[0]

    start = C.index(maximum) - rope_lenght
    finish = C.index(maximum) + rope_lenght

    Y = np.array(Y[start:finish:1])
    X = np.array(X[start:finish:1])

    return X, Y


def least_sqaures(x, y, err=False):
    """
    Takes a set of X and Y values from a data set and returns the linear
    constants in the classical linear equation.

    y = m + kx or y = A + Bx or whatever convention is usually followed.

    """
    x = np.array(x)
    y = np.array(y)
    if len(x) != len(y):
        raise TypeError(
            "Both parameters need to be of the same shape.\n{0},{1}".format(
                len(x), len(y)
            )
        )
    N = len(y)

    delta = N * np.sum(x ** 2) - np.sum(x) ** 2
    m = (np.sum(x ** 2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / delta
    k = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / delta

    # k = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
    # N * np.sum(x ** 2) - (np.sum(x)) ** 2
    # )

    # m = (np.sum(y) - k * np.sum(x)) / N
    if err == True:
        sigma_y = np.sqrt(1 / (N - 2) * np.sum((y - m - k * x) ** 2))

        sigma_m = sigma_y * np.sqrt(np.sum(x ** 2) / delta)
        sigma_k = sigma_y * np.sqrt(N / delta)
        return sigma_m, sigma_k

    return m, k


def Tafel_OP_OLD(cd, ecd, slope):
    """
    Returns the overpotential from current density and exchange current
    density.
    ecd - exchange current density
    cd - short for current density
    alpha - Is the charge transfer coefficient. This is supposed a value
    between 1 and 0. I'm not sure how to determining it so I'm leaving it
    as one for the time being.
    """
    A = slope

    ans = []
    # This rather awkward IF statement is here to replace the plus minus sign
    # in the Tafel equation. The plus sign in the Tafel is if the equation
    # is an anode and minus if it's a cathode. During our experiment however
    # we switch polarity between the electrodes during our measurement. This
    # IF statement takes this into account.
    for i in cd:
        if i >= 0:
            ans.append(A * np.log10(i / ecd))
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
            ans.append(-A * np.log10(i / ecd))
    return np.array(ans)


def Tafel_OP(cd, ecd, slope, hydrogen=True):
    """
    Returns the overpotential from current density and exchange current
    density.
    ecd - exchange current density
    cd - short for current density
    alpha - Is the charge transfer coefficient. This is supposed a value
    between 1 and 0. I'm not sure how to determining it so I'm leaving it
    as one for the time being.
    """
    A = slope

    # When taking the current density for hydrogen we need to convert it
    # to positive numbers if we want sensible numbers from the logarithm.
    if hydrogen == True:
        ans = -A * np.log10(-1 * cd / ecd)
    else:
        ans = A * np.log10(cd / ecd)

    return np.array(ans)


def TafelSlope(OP, ECD, CD, alpha=1, hydrogen="True"):
    if hydrogen == True:
        CD, OP = list_cropper_2(
            -1 * np.log10(-1 * np.array(CD)), OP - op_H, n=12, peak="min"
        )
    else:
        CD, OP = list_cropper_2(np.log10(np.array(CD)), OP - op_O)

    slope = OP / (CD - np.log10(ECD))
    return np.mean(slope)


def ecd(data_i, data_v, err=False):
    """
    Takes two lists of current densities and corresponding potential.

    Returns two exhange current densities one for the Oxygen reaction
    and one for the Hydrogen reaction.
    """

    # Oxygen reaction
    log_i_s, V_s = list_cropper_2(np.log10(np.array(data_i)), data_v - op_O)
    m, k = least_sqaures(log_i_s, V_s)

    # Hydrogen reaction

    # Since the hydrogen reaction happens for negative voltage
    # at the working electrode I first need to turn the numbers
    # into possitive ones in order to take the logarith of that
    # set of data. Then since we dont want to keep the actual data
    # possitive we would want to turn it back into the negatives.
    # This is what the extra line of code is doing.

    log_i_s_H, V_s_H = list_cropper_2(
        -1 * np.log10(-1 * data_i), data_v - op_H, n=12, peak="min"
    )
    m_H, k_H = least_sqaures(log_i_s_H, V_s_H)

    if err == True:
        sigma_m_H, sigma_k_H = least_sqaures(log_i_s_H, V_s_H, err=True)
        sigma_ecd_H = m_H/k_H * np.sqrt((sigma_m_H/m_H)**2 + (sigma_k_H/k_H) ** 2)

        sigma_m, sigma_k = least_sqaures(log_i_s, V_s, err=True)
        sigma_ecd = m/k * np.sqrt((sigma_m/m)**2 + (sigma_k/k) ** 2)

        return sigma_ecd, sigma_ecd_H


    return -m / k, -m_H / k_H
