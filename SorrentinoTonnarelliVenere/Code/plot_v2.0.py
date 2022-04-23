import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize


def quadratic(x, a, b, c):
    return (a*x + c*x*x + b)


if __name__ == '__main__':
    min_energy_2000Q = np.empty((10, 60))
    max_energy_2000Q = np.empty((10, 60))

    min_energy_Advantage = np.empty((10, 150))
    max_energy_Advantage = np.empty((10, 150))

    qpu_processing_times_Advantage = np.empty((10, 150))
    qpu_processing_times_2000Q = np.empty((10, 60))

    for i in range(1, 11, 1):
        file = open("Composite/try_"+str(i)+".txt", "r")
        count = 0
        for line in file:
            if line != "\n":
                row = line.split()
                min_energy_2000Q_sample = row[2].replace(",", "")
                max_energy_2000Q_sample = row[4].replace(",", "")
                sample = row[16].replace(",", "")
                sample = sample.replace("\'", "")
                qpu_processing_times_2000Q[i-1, count] = float(sample)
                min_energy_2000Q[i-1, count] = float(min_energy_2000Q_sample)
                max_energy_2000Q[i-1, count] = float(max_energy_2000Q_sample)
                count += 1
    count = 0
    for i in range(1, 11, 1):
        file = open("Advantage/try_"+str(i)+".txt", "r")
        count = 0
        for line in file:
            if line != "\n":
                row = line.split()
                min_energy_Advantage_sample = row[2].replace(",", "")
                max_energy_Advantage_sample = row[4].replace(",", "")
                sample = row[16].replace(",", "")
                sample = sample.replace("\'", "")
                qpu_processing_times_Advantage[i-1, count] = float(sample)
                min_energy_Advantage[i-1, count] = float(min_energy_Advantage_sample)
                max_energy_Advantage[i-1, count] = float(max_energy_Advantage_sample)
                count += 1

    qpu_processing_times_Advantage
    qpu_processing_times_2000Q
    times_Advantage = np.arange(1, 151, 1)
    times_2000Q = np.arange(1, 61, 1)

    mean_Advantage = np.mean(qpu_processing_times_Advantage, axis=0)
    mean_2000Q = np.mean(qpu_processing_times_2000Q, axis=0)
    var_Advantage = np.var(qpu_processing_times_Advantage, axis=0)
    var_2000Q = np.var(qpu_processing_times_2000Q, axis=0)

    plt.figure(0)
    plt.plot(mean_2000Q, 'r')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(1)
    plt.plot(mean_Advantage, 'r')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(2)
    plt.plot(var_2000Q, 'b')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(3)
    plt.plot(var_Advantage, 'b')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(4)
    for i in range(0, 10, 1):
        plt.scatter(x=times_2000Q, y=qpu_processing_times_2000Q[i], s=5, marker='o', color='green')
    qfit, qerr = scipy.optimize.curve_fit(quadratic, times_2000Q, mean_2000Q)
    plt.plot(times_2000Q, quadratic(times_2000Q, *qfit), 'r', label='Fitted Quadratic Curve')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(5)
    for i in range(0, 10, 1):
       plt.scatter(x=times_Advantage, y=qpu_processing_times_Advantage[i], s=5, marker='o', color='green')
    afit, aerr = scipy.optimize.curve_fit(quadratic, times_Advantage, mean_Advantage)
    plt.plot(times_Advantage, quadratic(times_Advantage, *afit), 'r', label='Fitted Quadratic Curve')
    plt.xlabel("subset")
    plt.ylabel("qpu_time")

    plt.figure(6)
    plt.xlabel("subset")
    plt.ylabel("energy")
    for i in range(0, 10, 1):
        plt.scatter(x=times_2000Q, y=min_energy_2000Q[i], s=5, marker='o', color='green', label='Min Energy')
        plt.scatter(x=times_2000Q, y=max_energy_2000Q[i], s=5, marker='o', color='red', label='Max energy')

    plt.figure(7)
    plt.xlabel("subset")
    plt.ylabel("energy")
    for i in range(0, 10, 1):
        plt.scatter(x=times_Advantage, y=min_energy_Advantage[i], s=5, marker='o', color='green', label='Min Energy')
        plt.scatter(x=times_Advantage, y=max_energy_Advantage[i], s=5, marker='o', color='red', label='Max energy')

    plt.figure(8)
    plt.xlabel("subset")
    plt.ylabel("energy")
    plt.plot(np.mean(min_energy_2000Q, axis=0), 'g')
    plt.plot(np.mean(max_energy_2000Q, axis=0), 'r')

    plt.figure(9)
    plt.xlabel("subset")
    plt.ylabel("energy")
    plt.plot(np.mean(min_energy_Advantage, axis=0), 'g')
    plt.plot(np.mean(max_energy_Advantage, axis=0), 'r')

    plt.show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
