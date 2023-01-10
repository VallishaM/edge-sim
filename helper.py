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
    plt.title("Cumulative Reward")
    plt.xlabel("Time step")
    plt.ylabel("Cumulative Reward")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_task_drop_rate, color="b")

    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_task_drop_rate) - 1,
        global_task_drop_rate[-1],
        str(global_task_drop_rate[-1]),
    )

    plt.savefig("./results/cumulative_reward.png")
    # plt.show(block=True)
    # plt.pause(0.1)

    plt.figure(2)
    plt.clf()
    plt.title("Running Drop Rate")
    plt.xlabel("Time step")
    plt.ylabel("Running Drop Rate")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_running, color="b")

    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_running) - 1,
        global_running[-1],
        str(global_running[-1]),
    )
    plt.savefig("./results/running_rate.png")

    # plt.show(block=True)
    # plt.pause(0.1)

    plt.figure(3)
    plt.clf()
    plt.title("Running Energy")
    plt.xlabel("Time step")
    plt.ylabel("Running Energy")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_energy_running, color="b")

    # plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_energy_running) - 1,
        global_energy_running[-1],
        str(global_energy_running[-1]),
    )
    plt.savefig("./results/running_energy.png")
    # plt.show(block=True)
    # plt.pause(0.1)

    plt.figure(4)
    plt.clf()
    plt.title("Running Latency")
    plt.xlabel("Time step")
    plt.ylabel("Running Latency")
    # plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_latency_running, color="b")

    plt.text(
        len(global_latency_running) - 1,
        global_latency_running[-1],
        str(global_latency_running[-1]),
    )
    plt.savefig("./results/running_latency.png")

    # plt.show(block=True)
    # plt.pause(0.1)
