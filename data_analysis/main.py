import numpy as np
import matplotlib as plt

file_name = "~/water_electrolysis/data_analysis/data_5.txt"
delta = 1
min_lvl = 1
data = np.loadtxt(file_name, delimiter=" ", dtype=float)

def significance(margin, data_array):
    ans = "No significant value"
    for i in range(len((data_array))):
        if i == 1:
            pass
        else:
            diff = data_array[i] - data_array[i-1]

            if margin > diff:
                ans = (i, data_array[i])
                break
            elif data[i] > min_lvl:
                ans = (i, data_array[i])
                break
    return ans

def main():
    # significance(delta, data)
    print(data[:10, :10])


if __name__ == "__main__":
    # data_plotable = data
    # plt.plot(data_plotable)
    # plt.show()
    main()
