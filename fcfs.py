from process import Process

def schedule(processes):
    time = 0
    gantt = []
    processes = sorted(processes, key=lambda x: x.arrival_time)

    for p in processes:
        # Insert IDLE only if the CPU has to wait before the next process arrives
        if time < p.arrival_time:
            idle_time = p.arrival_time - time
            gantt.append(('IDLE', idle_time))
            time = p.arrival_time  # CPU jumps to the arrival of the next process

        p.response_time = time - p.arrival_time
        gantt.append((f'P{p.pid}', p.burst_time))
        time += p.burst_time

        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    return gantt, processes
