# ALGORITHM FOR main.py
from server import MECServer
from edgeDevice import EdgeDevice
import random

NUMBER_OF_MOBILE_DEVICES = 1
offload_dictionary = {}
global_result = []

time_step = 0
# initialise server and devices
devices = []
for _ in range(0, NUMBER_OF_MOBILE_DEVICES):
    params = ()
    devices.append(EdgeDevice(params))
server = MECServer()
# initialise server and devices

while True:
    time_step += 1
    server.refresh_process_queue(
        time_step
    )  # remove tasks from server's process queue that have been processed
    for device in devices:
        popped = device.refresh_upload_queue(
            time_step
        )  # remove tasks from device's upload queue that have been uploaded
        for task in popped:
            # This way we won't need an additional data structure in main.py to store the task until it's uploaded
            result = server.offload(task, time_step)
            global_result.append(result)
        device.refresh_process_queue(time_step)
        device.run(time_step)


# Display the compiled results
