from process import Process

def srtf_schedule(processes):
    time = 0
    gantt = []

    remaining_processes = [p for p in processes]
    for p in remaining_processes:
        p.remaining_time = p.burst_time
        p.response_time = -1

    queue = []

    while remaining_processes or queue:
        for p in remaining_processes[:]: 
            if p.arrival_time <= time:
                queue.append(p)
                remaining_processes.remove(p)

        if not queue:
            next_arrival = min(remaining_processes, key=lambda x: x.arrival_time)
            idle_time = next_arrival.arrival_time - time
            gantt.append(('IDLE', idle_time))
            time = next_arrival.arrival_time
            continue

        queue.sort(key=lambda x: x.remaining_time)
        current = queue[0]

        if current.response_time == -1:
            current.response_time = time - current.arrival_time

        next_arrivals = [p.arrival_time for p in remaining_processes if p.arrival_time > time]
        if next_arrivals:
            next_arrival_time = min(next_arrivals)
            time_slice = min(current.remaining_time, next_arrival_time - time)
        else:
            time_slice = current.remaining_time

        gantt.append((f'P{current.pid}', time_slice))
        time += time_slice
        current.remaining_time -= time_slice

        if current.remaining_time == 0:
            queue.remove(current)
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time

    return gantt, processes
