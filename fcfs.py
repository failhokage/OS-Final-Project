from process import Process

def schedule(processes):
    time = 0
    gantt = []
    processes = sorted(processes, key=lambda x: x.arrival_time)
    
    for p in processes:
        if time < p.arrival_time:
            time = p.arrival_time
            gantt.append(('IDLE', time - p.arrival_time))
        
        p.response_time = time - p.arrival_time
        gantt.append((f'P{p.pid}', p.burst_time))
        time += p.burst_time
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
    
    return gantt, processes