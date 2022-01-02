import numpy as np
import math as m
import matplotlib.pyplot as plt

from galvani import BioLogic as BL
import pandas as pd


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

    A = Y.tolist()
    X = X.tolist()

    B = A.copy()
    C = A.copy()

    B.sort()
    if peak == "max":
        maximum = B[-1]
    else:
        maximum = B[0]
    rope_lenght = len(A) // (2 * n)

    start = C.index(maximum) - rope_lenght
    finish = C.index(maximum) + rope_lenght

    Y = Y[start:finish:1]

    X = X[start:finish:1]

    return X, Y


def least_sqaures(x, y):
    """
    Takes a set of X and Y values from a data set and returns the linear
    constants in the classical linear equation.

    y = m + kx or y = A + Bx or whatever convention is usually followed.

    """
    x = np.array(x)
    y = np.array(y)
    if len(x) != len(y):
        raise TypeError("Both parameters need to be of the same shape.")
    N = len(y)

    delta = N * np.sum(x ** 2) - np.sum(x) ** 2
    m = (np.sum(x ** 2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / delta
    k = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / delta

    return m, k


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


def ecd(data_i, data_v):
    """ 
    Takes two lists of current densities and corresponding potential.

    Returns two exhange current densities one for the Oxygen reaction
    and one for the Hydrogen reaction. 
    """

    # Oxygen reaction
    log_i_s, V_s = list_cropper_2(data_i, data_v)
    log_i_s = np.log10(log_i_s)
    m, k = least_sqaures(log_i_s, V_s)

    # Hydrogen reaction
    # Since the hydrogen reaction happens for negative voltage 
    # at the working electrode I first need to turn the numbers
    # into possitive ones in order to take the logarith of that
    # set of data. Then since we dont want to keep the actual data
    # possitive we would want to turn it back into the negatives. 
    # This is what the extra line of code is doing.

    i_s_H, V_s_H = list_cropper_2(data_i, data_v, peak="min", n=12)
    log_i_s_H = np.log10(-1 * np.array(i_s_H))
    m_H, k_H = least_sqaures(log_i_s_H,-1* V_s_H)

    return -m / k, -m_H / k_H
