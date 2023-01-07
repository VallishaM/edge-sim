import  math
class MECServer:
    
    def __init__(self):
        # primary storage capacity, secondary storage capacity, latency from secondary storage to primary, processor clock cycle
        self.CLOCK_CYCLES = 3200000 # clockcycle in ms. Processing 
        self.STORAGE_SIZE = 15360000000000*8 # 15.36 TB
        self.MEMORY_SIZE = 64000000000*8
        self.STORAGE_RATE = 1600000000*8 # 256
        self.time = 0
        # self.process_queue = {
        #     # Key=UUID
        #     # Value: Array of tasks for each Device connected to server
        # }
        self.process_queue = list()
    
    def execution_time(self,task):
        latency =  (task.task_size/self.STORAGE_RATE)+(task.task_size/self.CLOCK_CYCLES)**task.cycles_per_bit
        return math.ceil((latency/50))

    def refresh_process_queue(self,time):
        # val = self.process_queue.copy()
        delay = 0
        while len(self.process_queue) > 0:
            delay += self.execution_time(self.process_queue[0])
            if delay > time:
                self.process_queue.pop(0)
            else:
                break

    def compute_latency(self,newTask):
        latency = 0
        for (task,timestep) in self.process_queue:
            latency += self.execution_time(task)
        if newTask.timeout > latency:
            return -1
        return latency
    
    def put_in_queue(self,newTask):
        self.process_queue.append(newTask)
