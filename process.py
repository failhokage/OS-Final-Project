class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.response_time = -1 
        self.first_execution = -1  
        self.priority = 0  
        self.allotment = 0  
        self.remaining_quantum = 0  

    def __str__(self):
        return f"P{self.pid} (AT: {self.arrival_time}, BT: {self.burst_time})"