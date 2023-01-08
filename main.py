# ALGORITHM FOR main.py
from server import MECServer
from edgeDevice import EdgeDevice
from tabulate import tabulate

NUMBER_OF_MOBILE_DEVICES = 1
offload_dictionary = {}
global_result = []

# initialise server and devices
devices = []
for _ in range(0, NUMBER_OF_MOBILE_DEVICES):
    devices.append(EdgeDevice(600 * (10 ** 3), 128 * (10 ** 6), 4200 * 8 * (10 ** 3)))
server = MECServer()
# initialise server and devices

time_step = 0
tasks_dropped = 0
while time_step < 100000:
    global_result.extend(
        server.refresh_process_queue(time_step)
    )  # remove tasks from server's process queue that have been processed
    for device in devices:
        popped = device.refresh_upload_queue(
            time_step
        )  # remove tasks from device's upload queue that have been uploaded
        for task in popped:
            # This way we won't need an additional data structure in main.py to store the task until it's uploaded
            tasks_dropped += server.offload(task, time_step)
        global_result.extend(device.refresh_process_queue(time_step))
        if time_step < 1000:
            tasks_dropped += device.run(time_step)
    time_step += 1

# Calculate drop rate
num_of_tasks = 0
for (idx, device) in enumerate(devices):
    num_of_tasks += device.num_of_tasks
    if len(device.upload_queue) > 0:
        print(
            f"Number of tasks left in upload queue of device {idx}: {len(device.upload_queue)}"
        )
    if len(device.process_queue) > 0:
        print(
            f"Number of tasks left in process queue of device {idx}: {len(device.process_queue)}"
        )
print("Number of tasks left in process queue of server: ", len(server.process_queue))
print("Number of tasks generated: ", num_of_tasks)
print("Task drop rate: ", (-1 * tasks_dropped / num_of_tasks))

# Display the compiled results
table = []
for res in global_result:
    if len(res) > 0:
        table.append(
            [
                res[0].task_size,
                res[0].task_timeout,
                res[0].upload_latency + res[1],
                res[0].start_time,
            ]
        )
print(tabulate(table, headers=["Task Size", "Task Timeout", "Latency", "Start Time"]))
