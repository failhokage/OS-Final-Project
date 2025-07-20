class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.first_execution = -1
        self.completion_time = 0
        self.response_time = -1
        self.turnaround_time = 0
