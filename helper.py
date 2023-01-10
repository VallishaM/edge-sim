import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(
    global_task_drop_rate, global_running, global_energy_running, global_latency_running
):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.figure(1)
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

    plt.figure(2)
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Running Drop Rate")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_running, color="b", label="Running Drop Rate")

    plt.legend(loc="upper left")
    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_running) - 1,
        global_running[-1],
        str(global_running[-1]),
    )

    plt.show(block=False)
    plt.pause(0.1)

    plt.figure(3)
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Running Energy")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_energy_running, color="b", label="Running Energy")

    plt.legend(loc="upper left")
    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_energy_running) - 1,
        global_energy_running[-1],
        str(global_energy_running[-1]),
    )

    plt.show(block=False)
    plt.pause(0.1)

    plt.figure(4)
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Running Latency")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_latency_running, color="b", label="Running Latency")

    plt.legend(loc="upper left")

    plt.text(
        len(global_latency_running) - 1,
        global_latency_running[-1],
        str(global_latency_running[-1]),
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
    # plt.pause(0.1)
