# ALGORITHM FOR main.py
from server import MECServer
from edgeDevice import EdgeDevice
from helper import plot, plot_single
from agent import Agent
from copy import deepcopy
import numpy as np
import random


# from tabulate import tabulate

NUMBER_OF_MOBILE_DEVICES = 1
offload_dictionary = {}
global_result = []
agent = Agent()
# initialise server and devices
server = MECServer()
devices = []
for _ in range(0, NUMBER_OF_MOBILE_DEVICES):
    devices.append(
        EdgeDevice(14 * 10**3, 2.5 * 10**6, 4200 * 8 * (10**3), agent, server)
    )

# initialise server and devices
tasks_generated = 0
time_step = 0
tasks_dropped = 0
global_latency = []
time_array = []
global_upload_latency = []
global_process_latency = []
global_local_latency = []
global_task_drop_rate = []
global_reward_sum = []
global_generated = []
global_dropped = []
global_running = []
global_energy = []
global_energy_running = []
prev_state = [0, 0]
prev_reward = 0
prev_action = 0
while time_step < 1000:
    time_array.append(time_step)
    new_tasks = 0
    drop = 0
    new_latency = 0

    server.refresh_process_queue(
        time_step
    )  # remove tasks from server's process queue that have been processed
    for device in devices:
        device.refresh_upload_queue(
            time_step
        )  # remove tasks from device's upload queue that have been uploaded

        device.refresh_process_queue(time_step)
        if time_step < 1000:

            result = device.poll(time_step)
            if result[0]:  # If task generated
                global_generated.append(1)
                new_tasks += 1
                agent.update(
                    prev_state,
                    prev_action,
                    prev_reward * 10,
                    result[5],
                )
                prev_state = deepcopy(result[5])
                print("State: ", prev_state)
                if result[1]:  # If Offload
                    # print(result)
                    prev_action = 1
                    global_upload_latency.append(result[2].upload_latency)
                    server_result = server.offload(
                        result[2], result[2].upload_latency + time_step
                    )
                    if len(global_local_latency) == 0:
                        global_local_latency.append(0)
                    else:
                        global_local_latency.append(global_local_latency[-1])

                    global_process_latency.append(server_result[1])
                    new_latency += server_result[1] + result[2].upload_latency
                    global_latency.append(server_result[1] + result[2].upload_latency)
                    if server_result[0]:  #  drop
                        drop += 1
                        prev_reward = -1
                        global_dropped.append(1)
                        print(
                            "Offload and drop, energy:",
                            (result[2].upload_latency + server_result[1])
                            * 0.05
                            * 0.001
                            * 6.87,
                            "Upload latency",
                            result[2].upload_latency,
                        )
                        global_energy.append(
                            (result[2].upload_latency + server_result[1])
                            * 0.05
                            * 0.001
                            * 6.87
                        )
                    else:  # Successfully processable
                        prev_reward = 1
                        global_dropped.append(0)
                        print(
                            "Offload",
                            server_result[1] + result[2].upload_latency,
                            "energy:",
                            (server_result[1] + result[2].upload_latency) * 0.05 * 6.87,
                            "Upload latency",
                            result[2].upload_latency,
                        )
                        global_energy.append(
                            (server_result[1] + result[2].upload_latency) * 0.05 * 6.87
                        )

                else:  # if not offload
                    prev_action = 0
                    new_latency += result[2]
                    global_latency.append(result[2])
                    global_local_latency.append(result[4])
                    if result[3]:  # Droop
                        drop += 1
                        global_dropped.append(1)
                        print(
                            "Local and drop, energy:", result[2] * 350 * 0.05
                        )  # in milli Joule
                        global_energy.append(result[2] * 350 * 0.05)
                        prev_reward = -1
                    else:
                        prev_reward = 1
                        global_dropped.append(0)
                        print(
                            "Local : ", result[2], "energy : ", result[2] * 0.05 * 350
                        )
                        global_energy.append(result[2] * 0.05 * 350)

                    if len(global_latency) > 0:
                        if len(global_process_latency) > 0:
                            global_upload_latency.append(global_upload_latency[-1])
                            global_process_latency.append(global_process_latency[-1])
                        else:
                            global_upload_latency.append(0)
                            global_process_latency.append(0)

                print(
                    "New Latency : ",
                    new_latency,
                    "New Tasks : ",
                    new_tasks,
                    "New Drop : ",
                    drop,
                    "Rate : ",
                    round(drop / new_tasks, 4),
                )
                try:

                    global_running.append(
                        sum(
                            global_dropped[
                                max(0, len(global_dropped) - 30) : len(global_dropped)
                            ]
                        )
                        / sum(
                            global_generated[
                                max(0, len(global_generated) - 30) : len(
                                    global_generated
                                )
                            ]
                        )
                    )

                except:
                    global_running.append(0)
                if len(global_energy) == 0:
                    global_energy_running.append(0)
                else:
                    global_energy_running.append(
                        sum(
                            global_energy[
                                max(0, len(global_energy) - 30) : len(global_energy)
                            ]
                        )
                    )
                global_task_drop_rate.append(prev_reward)
                global_reward_sum.append(sum(global_task_drop_rate))
                # plot(global_reward_sum, global_running, global_energy_running)
            else:
                global_dropped.append(0)
                print("No task generated")
                if len(global_latency) > 0:
                    global_latency.append(global_latency[-1])
                    global_upload_latency.append(global_upload_latency[-1])
                    global_process_latency.append(global_process_latency[-1])
                    global_local_latency.append(global_local_latency[-1])

                else:
                    global_local_latency.append(0)
                    global_upload_latency.append(0)
                    global_process_latency.append(0)

    tasks_dropped += drop
    tasks_generated += new_tasks

    if tasks_generated > 0:
        print(
            "Total Tasks : ",
            tasks_generated,
            "Total Drop : ",
            tasks_dropped,
            "Rate : ",
            round(tasks_dropped / tasks_generated, 4),
            "Running Rate = ",
            sum(global_dropped[max(0, len(global_dropped) - 30) : len(global_dropped)])
            / sum(
                global_generated[
                    max(0, len(global_generated) - 30) : len(global_generated)
                ]
            ),
        )

    time_step += 1

# Calculate drop rate
