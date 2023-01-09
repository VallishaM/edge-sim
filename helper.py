import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(
    global_latency, global_upload_latency, global_process_latency, global_local_latency
):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Time step")
    plt.ylabel("Latency")
    plt.plot(global_latency, color="y", label="Total Latency")
    plt.plot(global_upload_latency, color="b", label="Upload Latency")
    plt.plot(global_process_latency, color="r", label="Process Latency at Server")
    plt.plot(global_local_latency, color="k", label="Process Latency at Device")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.text(len(global_latency) - 1, global_latency[-1], str(global_latency[-1]))
    plt.text(
        len(global_upload_latency) - 1,
        global_upload_latency[-1],
        str(global_upload_latency[-1]),
    )
    plt.text(
        len(global_process_latency) - 1,
        global_process_latency[-1],
        str(global_process_latency[-1]),
    )
    plt.text(
        len(global_local_latency) - 1,
        global_local_latency[-1],
        str(global_local_latency[-1]),
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
