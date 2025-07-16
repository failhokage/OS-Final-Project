from collections import deque
from process import Process

def schedule(processes, time_quantums=[4,8,16,32], allotment_times=[10,20,40,80]):
    time = 0
    gantt = []
    queues = [deque() for _ in range(4)]
    remaining_processes = sorted(processes.copy(), key=lambda x: x.arrival_time)
    allotment_counters = [0] * 4
    
    while remaining_processes or any(queues):
        while remaining_processes and remaining_processes[0].arrival_time <= time:
            p = remaining_processes.pop(0)
            p.priority = 0
            queues[0].append(p)
        
        current_queue = next((i for i, q in enumerate(queues) if q), None)
        
        if current_queue is None:
            if remaining_processes:
                next_arrival = remaining_processes[0].arrival_time
                idle_time = next_arrival - time
                gantt.append(('IDLE', idle_time))
                time = next_arrival
                allotment_counters = [0] * 4
                continue
            else:
                break
        
        current = queues[current_queue].popleft()
        if current.response_time == -1:
            current.response_time = time - current.arrival_time
        
        execution_time = min(time_quantums[current_queue], current.remaining_time)
        gantt.append((f'P{current.pid}(Q{current_queue})', execution_time))
        time += execution_time
        current.remaining_time -= execution_time
        allotment_counters[current_queue] += execution_time
        
        while remaining_processes and remaining_processes[0].arrival_time <= time:
            p = remaining_processes.pop(0)
            p.priority = 0
            queues[0].append(p)
        
        if current.remaining_time > 0:
            if allotment_counters[current_queue] >= allotment_times[current_queue]:
                new_queue = min(current_queue + 1, 3)
                current.priority = new_queue
                queues[new_queue].append(current)
                allotment_counters[current_queue] = 0
            else:
                queues[current_queue].append(current)
        else:
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time
    
    return gantt, processes