from process import Process

def schedule(processes):
    time = 0
    gantt = []
    remaining_processes = processes.copy()
    remaining_processes.sort(key=lambda x: x.arrival_time)
    queue = []
    
    while remaining_processes or queue:
        while remaining_processes and remaining_processes[0].arrival_time <= time:
            queue.append(remaining_processes.pop(0))
        
        if not queue:
            if remaining_processes:
                next_arrival = remaining_processes[0].arrival_time
                idle_time = next_arrival - time
                gantt.append(('IDLE', idle_time))
                time = next_arrival
                continue
        
        queue.sort(key=lambda x: x.remaining_time)
        current = queue.pop(0)
        if current.response_time == -1:
            current.response_time = time - current.arrival_time
        
        execution_time = current.remaining_time
        gantt.append((f'P{current.pid}', execution_time))
        time += execution_time
        current.remaining_time = 0
        current.completion_time = time
        current.turnaround_time = current.completion_time - current.arrival_time
        current.waiting_time = current.turnaround_time - current.burst_time
    
    return gantt, processes