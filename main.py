# ALGORITHM FOR main.py
from server import MECServer
from edgeDevice import EdgeDevice

NUMBER_OF_MOBILE_DEVICES = 1
offload_dictionary = {}
global_result = []

# initialise server and devices
devices = []
for _ in range(0, NUMBER_OF_MOBILE_DEVICES):
    devices.append(EdgeDevice(30 * 10 ** 6, 128 * 10 ** 6, 4200 * 8 * 10 ** 6))
server = MECServer()
# initialise server and devices

time_step = 0
tasks_dropped = 0
while True:
    server.refresh_process_queue(
        time_step
    )  # remove tasks from server's process queue that have been processed
    for device in devices:
        popped = device.refresh_upload_queue(
            time_step
        )  # remove tasks from device's upload queue that have been uploaded
        for task in popped:
            # This way we won't need an additional data structure in main.py to store the task until it's uploaded
            tasks_dropped += server.offload(task, time_step)
        global_result += device.refresh_process_queue(time_step)
        tasks_dropped += device.run(time_step)
    time_step += 1

    # Display the compiled results
    print(global_result)
