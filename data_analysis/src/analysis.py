import matplotlib.pyplot as plt


def plot_dijkstra_results(frequency, times_random):
    plt.figure(figsize=(8, 6))
    plt.plot(frequency, times_random, marker="o", label="Random graphs")
    # plt.plot(frequency, times_worst, marker="s", label="Worst-case graphs")
    plt.xlabel("Graph Size")
    plt.ylabel("Elapsed Time [s]")
    plt.title("Dijkstra Algorithm Performance")
    plt.legend()
    plt.grid(True)
    plt.show()
