import numpy as np
import matplotlib.pyplot as plt

from galvani import BioLogic as BL
import pandas as pd

mpr = BL.MPRfile('re_AgCl_we_Pd_ce_PT_el_15.mpr')
df = pd.DataFrame(mpr.data)
df.head()

# file_name = "re_AgCl_we_Pd_ce_PT_el_15.mpr"
# file_name = bl.MPRfile("re_AgCl_we_Pd_ce_PT_el_15.mpr")
# data = pd.DataFrame(file_name)


def main():
    print(df)
    # plt.plot(df)
    # plt.show()


if __name__ == "__main__":
    main()
