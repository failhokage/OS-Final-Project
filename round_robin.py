from collections import deque

def rr(processes, quantum):
    time = 0
    queue = deque()
    gantt = []
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)
    i = 0
    completed = 0

    for p in processes:
        p.remaining_time = p.burst_time
        p.first_execution = -1
        p.response_time = -1

    # Enqueue initial processes
    while i < n and processes[i].arrival_time <= time:
        queue.append(processes[i])
        i += 1

    while completed < n:
        if not queue:
            # CPU is IDLE
            next_arrival = processes[i].arrival_time
            idle_duration = next_arrival - time
            gantt.append((idle_duration, "IDLE"))
            time = next_arrival
            while i < n and processes[i].arrival_time <= time:
                queue.append(processes[i])
                i += 1
            continue

        current = queue.popleft()

        if current.first_execution == -1:
            current.first_execution = time
        if current.response_time == -1:
            current.response_time = time - current.arrival_time

        run_time = min(quantum, current.remaining_time)
        gantt.append((run_time, current.pid))
        time += run_time
        current.remaining_time -= run_time

        # Capture any new arrivals during this time
        arrived = []
        while i < n and processes[i].arrival_time <= time:
            arrived.append(processes[i])
            i += 1

        # Re-queue current process if not done
        if current.remaining_time > 0:
            queue.append(current)
        else:
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time

        # Add new arrivals to queue after current process
        for p in arrived:
            queue.append(p)

        if current.remaining_time == 0:
            completed += 1

    return gantt
