from process import Process

def rr(processes, time_quantum):
    processes.sort(key=lambda p: p.arrival_time)
    gantt = []
    current_time = 0
    ready_queue = []
    remaining = processes[:]

    while ready_queue or remaining:

        arriving = [p for p in remaining if p.arrival_time <= current_time]
        for p in arriving:
            ready_queue.append(p)
            remaining.remove(p)

        if not ready_queue:
            current_time += 1
            continue

        p = ready_queue.pop(0)
        if p.first_execution == -1:
            p.first_execution = current_time
            p.response_time = current_time - p.arrival_time

        exec_time = min(time_quantum, p.remaining_time)
        gantt.append((exec_time, p.pid))
        p.remaining_time -= exec_time
        current_time += exec_time


        arriving_during = [x for x in remaining if x.arrival_time <= current_time]
        for x in arriving_during:
            ready_queue.append(x)
            remaining.remove(x)

        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time

    return gantt
