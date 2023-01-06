# ALGORITHM FOR main.py
from server import Server
from device import Device
import random

NUMBER_OF_MOBILE_DEVICES = 1
offload_dictionary = {}
global_result = []

time_step = 0
# initialise server and devices
devices = []
for _ in range(0, NUMBER_OF_MOBILE_DEVICES):
    params = ()
    devices.append(Device(params))
server = Server()
# initialise server and devices

while True:
    time_step += 1
    server.refresh_process_queue(
        time_step
    )  # remove tasks from server's process queue that have been processed
    for device in devices:
        device.refresh_upload_queue(
            time_step
        )  # remove tasks from device's upload queue that have been uploaded
        device.refresh_process_queue(
            time_step
        )  # same as server's refresh process queue
        if random.uniform(0, 1) <= 0.95:  # generate task
            new_task = device.generate(time_step)
            offload_decision = device.decide(new_task)
            if offload_decision:  # offload to server
                upload_latency = device.compute_latency(new_task)
                time_to_offload_new_task = time_step + upload_latency
                if time_to_offload_new_task in offload_dictionary:
                    offload_dictionary[time_to_offload_new_task].append(new_task)
                else:
                    offload_dictionary[time_to_offload_new_task] = [new_task]
            else:  # local execution
                result = device.process(new_task)
                global_result.append(result)

# Display the compiled results
