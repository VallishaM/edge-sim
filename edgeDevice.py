import math
from numpy import random


class Task:
    def __init__(self, task_size, timeout, cycles_per_bit, start_time):
        self.task_size = task_size  # Number of bits
        self.task_timeout = timeout  # Deadline for the task to complete
        self.cycles_per_bit = (
            cycles_per_bit  # Algorithmic complexity => Eg: 2 -> n^2 time complexity
        )
        self.start_time = start_time
        self.upload_latency = 0


class EdgeDevice:
    def __init__(self, uplink_speed, clock_rate, bus_speed, agent, server):
        self.uplink_speed = uplink_speed  # Uplink bandwidth speed
        self.clock_rate = clock_rate  # No. of bits that can be processed in 1ms
        self.bus_speed = bus_speed  # Transfer speed from secondary storage to ram in megabits per sec
        self.upload_queue = []
        self.process_queue = []
        self.num_of_tasks = 0
        self.agent = agent
        self.server = server

    def generate_task(self, start_time):
        prob = random.choice(a=[0, 1], p=[0.7, 0.3])
        if prob == 1:
            task_size = random.randint(3, 5) * 10**6  # 20 megabits to 50 megabits
            task_timeout = random.randint(12, 18)
            cycles_per_bit = random.randint(28, 32) / 100
            return Task(task_size, task_timeout, cycles_per_bit, start_time)
        else:
            return None

    def policy(self, task: Task, t) -> bool:

        state = self.get_state(task)
        decision = self.agent.get_action(state, t)
        # d = [True, False]
        return (True, state) if decision == 1 else (False, state)

    def execution_time(self, task: Task) -> int:
        latency = (task.task_size * 1 / self.bus_speed) * 1000 + (
            task.task_size * task.cycles_per_bit * 1000
        ) / self.clock_rate
        latency_timestep = int(math.ceil(latency / 100))
        return latency_timestep

    def upload_time(self, task: Task) -> int:
        up_time = task.task_size * 1 / self.uplink_speed
        upload_timestep = int(math.ceil(up_time / 100))

        return upload_timestep

    def get_state(self, task):
        upload = self.compute_delay("U")
        server = self.server.compute_delay() + self.server.execution_time(task)
        process_local = self.compute_delay("P") + self.execution_time(task)
        state = [
            round(task.task_size / 10**6),
            round((task.task_timeout)),
            round(upload),
            round(server),
            round(process_local),
        ]

        return state

    def poll(self, timestep):
        task = self.generate_task(timestep)
        if task is not None:
            self.num_of_tasks += 1
            policy = self.policy(task, timestep)
            if policy[0]:
                # Offload
                task.upload_latency = self.upload_time(task) + self.compute_delay("U")
                self.upload_queue.append((task, timestep, self.upload_time(task)))
                return (
                    True,
                    True,
                    task,
                    False,
                    0,
                    policy[1],
                )  # (Generated?,Offload?,Latency,Dropout?)
            else:
                # Do not offload
                compute_latency = self.execution_time(task) + self.compute_delay("P")
                # Drop the task if task will not get executed within timeout
                if compute_latency + timestep <= task.start_time + task.task_timeout:
                    self.process_queue.append(
                        (
                            task,
                            timestep,
                            self.execution_time(task),
                        )
                    )
                    return (
                        True,
                        False,
                        compute_latency,
                        False,
                        self.execution_time(task),
                        policy[1],
                    )  # (generated?,offloaded?,latency,dropped?,process time)
                else:
                    # Drop task
                    return (True, False, compute_latency, True, 0, policy[1])
        else:
            return (False, False, -2, False, None)

    def compute_delay(self, which_queue):
        queue = []
        if which_queue == "P":
            queue = self.process_queue

        elif which_queue == "U":
            queue = self.upload_queue

        else:
            return None
        delay = 0
        for task_tuple in queue:
            delay += task_tuple[2]
        return delay

    def refresh_upload_queue(self, timestep):
        popped = []
        while len(self.upload_queue) > 0:
            task = self.upload_queue[0][0]
            latency = task.upload_latency  # delay + self.upload_time(task)
            if (
                latency + task.start_time <= timestep
            ):  # Task is done if current_time >=start_time+time_needed
                popped.append(task)
                self.upload_queue.pop(0)
            else:
                break
        return popped  # This way we won't need an additional data structure in main.py to store the task until it's uploaded. We can just upload the tasks which have been uploaded before start of this time step. As we are checking for completion at start of each time step, we are sure to get all tasks that have completed uploading by the end of the last time step. We can just upload these tasks at this time step, in each time step.

    def refresh_process_queue(self, timestep):
        popped = []
        while len(self.process_queue) > 0:
            task = self.process_queue[0][0]
            latency = self.process_queue[0][2]
            if latency + task.start_time <= timestep:
                # Task is done if current_time >=start_time+time_needed
                popped.append((task, latency))
                self.process_queue.pop(0)
            else:
                break
        return popped
