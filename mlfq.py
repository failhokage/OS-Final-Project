from collections import deque

def mlfq(processes, quantums=[2, 4, 8, 16], allotments=[5, 10, 20, float('inf')], boost_interval=50):
    queues = [deque() for _ in range(4)]
    gantt = []
    current_time = 0
    prev_pid = None
    last_start = 0
    MAX_TIME = 1000
    
    for p in processes:
        p.priority = 0
        p.remaining_time = p.burst_time
        p.allotment = allotments[0]
        p.quantum = quantums[0]
        p.first_execution = -1
        p.completed = False
        p.last_executed = -1

    while current_time < MAX_TIME:
        if all(p.completed for p in processes):
            break

        if current_time > 0 and current_time % boost_interval == 0:
            for p in processes:
                if not p.completed and p.priority > 0:
                    p.priority = 0
                    p.allotment = allotments[0]
                    p.quantum = quantums[0]
                    for q in queues:
                        if p in q:
                            q.remove(p)
                    queues[0].append(p)

        for p in processes:
            if (not p.completed and 
                p.arrival_time <= current_time and 
                all(p not in q for q in queues) and
                p.last_executed < current_time):
                queues[0].append(p)

        current_queue = next((i for i in range(4) if queues[i]), None)
        if current_queue is None:
            current_time += 1
            continue

        current_process = queues[current_queue].popleft()
        
        if current_process.first_execution == -1:
            current_process.first_execution = current_time

        exec_time = min(
            current_process.quantum,
            current_process.remaining_time,
            current_process.allotment
        )
        
        if prev_pid != current_process.pid:
            if prev_pid is not None:
                gantt.append((last_start, current_time, prev_pid))
            last_start = current_time
            prev_pid = current_process.pid

        current_process.remaining_time -= exec_time
        current_process.allotment -= exec_time
        current_process.last_executed = current_time + exec_time
        current_time += exec_time

        if current_process.remaining_time <= 0:
            gantt.append((last_start, current_time, current_process.pid))
            current_process.completion_time = current_time
            current_process.completed = True
            prev_pid = None
        else:
            if current_process.allotment <= 0 and current_process.priority < 3:
                current_process.priority += 1
                current_process.allotment = allotments[current_process.priority]
                current_process.quantum = quantums[current_process.priority]
            elif current_process.quantum <= 0:
                current_process.quantum = quantums[current_process.priority]
            
            queues[current_process.priority].append(current_process)

    if current_time >= MAX_TIME:
        print("Warning: Reached MAX_TIME. Forcing completion.")
        for p in processes:
            if not p.completed:
                if prev_pid == p.pid:
                    gantt.append((last_start, current_time, p.pid))
                p.completion_time = current_time
                p.remaining_time = 0
                p.completed = True

    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.response_time = p.first_execution - p.arrival_time

    return gantt