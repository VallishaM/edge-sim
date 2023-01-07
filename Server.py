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

    def refresh_process_queue(self,time_step):
        popped_tasks = list()
        while len(self.process_queue) > 0:
            task = self.process_queue[0][0]
            latency = self.process_queue[0][2]
            if latency + task.start_time <= time_step:
                popped_tasks.append(self.process_queue.pop(0))
            else:
                break
        return popped_tasks

    def compute_delay(self):
        latency = 0
        for element in self.process_queue:
            latency += element[2] # Keeps the latency of each task in it
        return latency
    
    def put_in_queue(self,newTask,timestep):
        total_time = self.execution_time(newTask)+self.compute_delay()
        if total_time + timestep <= newTask.start_time + newTask.timeout:
            self.process_queue.append((
                newTask,
                timestep,
                total_time
                ))
            
