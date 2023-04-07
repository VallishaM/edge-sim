import math

class MECServer:
    def __init__(self):
        # primary storage capacity, secondary storage capacity, latency from secondary storage to primary, processor clock cycle
        self.CLOCK_CYCLES = 0.3 * 10**9 
        self.STORAGE_SIZE = 15360000000000 * 8  # 15.36 TB
        self.MEMORY_SIZE = 64000000000 * 8
        self.STORAGE_RATE = 10000000 * 8  # 10 GBps
        self.time = 0
        self.process_queue = list()

    def execution_time(self, task):
        latency = (task.task_size * 1000 / self.STORAGE_RATE) + (
            task.task_size * task.cycles_per_bit * 1000
        ) / self.CLOCK_CYCLES
        return math.ceil((latency / 100))

    def refresh_process_queue(self, time_step):
        popped_tasks = []
        while len(self.process_queue) > 0:
            task = self.process_queue[0][0]
            latency = self.process_queue[0][2]
            if latency + task.start_time <= time_step:
                popped_tasks.append((task, latency))
                self.process_queue.pop(0)
            else:
                break
        return popped_tasks

    def compute_delay(self):
        latency = 0
        for task_tuple in self.process_queue:
            latency += task_tuple[2]

        return latency

    def offload(self, newTask, timestep):
        execution_time = self.execution_time(newTask)
        delay_time = self.compute_delay()
        total_time = execution_time + delay_time
        if total_time + timestep <= newTask.start_time + newTask.task_timeout:
            self.process_queue.append((newTask, timestep, execution_time))
            return (False, total_time)  # (Drop?,latency)
        else:
            # Drop task
            return (True, 0)