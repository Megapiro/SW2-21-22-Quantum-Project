import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    qpu_processing_times = []

    file = open("2000Q_test.txt", "r")
    count = 0
    for line in file:
        count +=1
        if line != "\n":
            row = line.split()
            sample = row[12].replace(",","")
            sample = sample.replace("\'", "")
            qpu_processing_times.append(float(sample))
    print(str(qpu_processing_times))
    plt.figure(0)
    plt.xlabel("subset")
    plt.ylabel("qpu_time")
    times = np.arange(1,66, 1)
    print(str(times))
    z = np.polyfit(times, qpu_processing_times, 1)
    p = np.poly1d(z)
    plt.plot(times, p(times), "r--")
    plt.plot(qpu_processing_times, 'g')
    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
