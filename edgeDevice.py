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
    def __init__(self, uplink_speed, process_rate, bus_speed):
        self.uplink_speed = uplink_speed  # Uplink bandwidth speed
        self.process_rate = process_rate  # No. of bits that can be processed in 1ms
        self.bus_speed = bus_speed  # Transfer speed from secondary storage to ram in megabits per sec
        self.upload_queue = []
        self.process_queue = []
        self.num_of_tasks = 0

    def generate_task(self, start_time):
        prob = random.choice(a=[0, 1], p=[0.2, 0.8])
        if prob == 1:
            task_size = (
                random.randint(32 * 8, 4 * 1024 * 8) * 10 ** 6
            )  # 32 megabits to 4 gigabits
            task_timeout = round(
                random.normal(loc=5000, scale=500)
            )  # mean = 500ms, std deviation = 300ms => 1 time step = 500ms
            cycles_per_bit = random.randint(1, 4)
            return Task(task_size, task_timeout, cycles_per_bit, start_time)
        else:
            return None

    def policy(self, task: Task) -> bool:
        prob = random.choice(a=[0, 1])
        return True if prob >= 0.5 else False

    def execution_time(self, task: Task) -> int:
        latency = (task.task_size * 1 / self.bus_speed) + (
            task.task_size * 1 / self.process_rate
        ) * task.cycles_per_bit
        latency_timestep = int(math.ceil(latency / 500))
        return latency_timestep

    def upload_time(self, task: Task) -> int:
        up_time = task.task_size * 1 / self.uplink_speed
        upload_timestep = int(math.ceil(up_time / 500))
        return upload_timestep

    def run(self, timestep):
        task = self.generate_task(timestep)
        if task is not None:
            self.num_of_tasks += 1
            if self.policy(task):
                # Offload
                task.upload_latency = self.upload_time(task) + self.compute_delay("U")
                self.upload_queue.append((task, timestep))
                return 0
            else:
                # Do not offload
                compute_latency = self.execution_time(task) + self.compute_delay("P")
                # Drop the task if task will not get executed within timeout
                if compute_latency + timestep <= task.start_time + task.task_timeout:
                    self.process_queue.append((task, timestep, compute_latency,))
                    return 0
                else:
                    # Drop task
                    return -1
        else:
            return 0

    def compute_delay(self, which_queue):
        queue = []
        if which_queue == "P":
            queue = self.process_queue
            return queue[-1][2] if len(queue) > 0 else 0
        elif which_queue == "U":
            queue = self.upload_queue
            return queue[-1][0].upload_latency if len(queue) > 0 else 0
        else:
            return None

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
