import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(global_task_drop_rate):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Cumulative Reward")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_task_drop_rate, color="b", label="Cumulative Reward")

    plt.legend(loc="upper left")
    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_task_drop_rate) - 1,
        global_task_drop_rate[-1],
        str(global_task_drop_rate[-1]),
    )

    plt.show(block=False)
    plt.pause(0.1)


def plot_single(global_latency):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Latency")
    plt.plot(global_latency, color="y", label="Total Latency")

    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.show(block=False)
    plt.pause(0.1)
