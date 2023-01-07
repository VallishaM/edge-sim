# ALGORITHM FOR main.py
from server import Server
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
server = Server()
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
        for (
            task
        ) in (
            popped
        ):  # This way we won't need an additional data structure in main.p to store the task until it's uploaded
            server.offload(task, time_step)
        device.refresh_process_queue(
            time_step
        )  # same as server's refresh process queue
        if random.uniform(0, 1) <= 0.95:  # generate task
            new_task = device.generate(time_step)
            offload_decision = device.decide(new_task)
            if offload_decision:  # offload to server
                device.push_to_upload_queue(new_task)
            else:  # local execution
                result = device.process(new_task)
                global_result.append(result)

# Display the compiled results
