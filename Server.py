
class MECServer:
    
    def __init__(self):
        # primary storage capacity, secondary storage capacity, latency from secondary storage to primary, processor clock cycle
        self.CLOCK_CYCLES = 3200000 # clockcycle in ms. Processing 
        self.STORAGE_SIZE = 15360000000000*8 # 15.36 TB
        self.MEMORY_SIZE = 64000000000*8
        self.STORAGE_RATE = 1600000000*8 # 256
        self.time = 0
        self.process_queue = {
            # Key=UUID
            # Value: Array of tasks for each Device connected to server
        }
    
    def pop(self,task):
        pass

    def compute(self,time):
        pass