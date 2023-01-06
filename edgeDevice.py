import math
from numpy import random


class Task:
    def __init__(self, task_size, timeout, cycles_per_bit):
        self.task_size = task_size  # Number of bits
        self.task_timeout = timeout  # Deadline for the task to complete
        self.cycles_per_bit = (
            cycles_per_bit  # Algorithmic complexity => Eg: 2 -> n^2 time complexity
        )


class EdgeDevice:
    def __init__(self, uplink_speed, process_rate, ram, bus_speed):
        self.uplink_speed = uplink_speed  # Uplink bandwidth speed
        self.process_rate = process_rate  # No. of bits that can be processed in 1ms
        self.ram = ram  # Ram size
        self.bus_speed = bus_speed  # Transfer speed from secondary storage to ram in megabits per sec
        self.upload_queue = []
        self.process_queue = []

    def generate_task(self):
        prob = random.choice(a=[0, 1], p=[0.2, 0.8])
        if prob == 1:
            task_size = random.randint(
                32 * 8, 4 * 1024 * 8
            )  # 32 megabits to 4 gigabits
            task_timeout = math.round(
                random.normal(loc=10, scale=4)
            )  # mean = 500ms, std deviation = 300ms => 1 time step = 50ms
            cycles_per_bit = random.randint(1, 4)
            return Task(task_size, task_timeout, cycles_per_bit)
        else:
            return None

    def policy(self, task: Task) -> bool:
        return True

    def execution_time(self, task: Task) -> int:
        latency = (task.task_size * 1 / self.bus_speed) + (
            task.task_size * 1 / self.process_rate
        ) ** task.cycles_per_bit
        latency_timestep = int(math.ceil(latency / 50))
        return latency_timestep

    def upload_time(self, task: Task) -> int:
        up_time = task.task_size * 1 / self.uplink_speed
        upload_timestep = int(math.ceil(up_time / 50))
        return upload_timestep

    def run(self, timestep):
        task = self.generate_task()
        if task is None:
            return None
        else:
            if self.policy(task):
                # Offload
                self.upload_queue.append((task, timestep))
                return (task, timestep)
            else:
                # Do not offload
                delay_timestep = 0
                for (t, timestep) in self.process_queue:
                    delay_timestep += self.execution_time(t)
                latency_timestep = delay_timestep + self.execution_time(task)
                # Drop the task if task will not get executed within timeout
                if latency_timestep - timestep <= task.task_timeout:
                    self.process_queue.append((task, timestep))
                return None

    def refresh_upload_queue(self, timestep):
        delay = 0
        while len(self.upload_queue) > 0:
            task = self.upload_queue[0]
            latency = delay + self.upload_time(task)
            if latency <= timestep:
                self.upload_queue.pop(0)
            else:
                break
            delay = latency

    def refresh_process_queue(self, timestep):
        delay = 0
        while len(self.process_queue) > 0:
            task = self.process_queue[0]
            latency = delay + self.execution_time(task)
            if latency <= timestep:
                self.process_queue.pop(0)
            else:
                break
            delay = latency
