from collections import deque

def rr(processes, quantum):
    time = min(p.arrival_time for p in processes)
    queue = deque()
    gantt = []
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)
    i = 0
    completed = 0

    for p in processes:
        p.remaining_time = p.burst_time
        p.first_execution = -1

    # Enqueue initial processes
    while i < n and processes[i].arrival_time <= time:
        queue.append(processes[i])
        i += 1

    while completed < n:
        if not queue:
            time += 1
            while i < n and processes[i].arrival_time <= time:
                queue.append(processes[i])
                i += 1
            continue

        current = queue.popleft()

        if current.first_execution == -1:
            current.first_execution = time
            current.response_time = time - current.arrival_time

        run_time = min(quantum, current.remaining_time)
        gantt.append((run_time, current.pid))
        time += run_time
        current.remaining_time -= run_time

        # ⛔ Fix: capture newly arrived processes first
        arrived = []
        while i < n and processes[i].arrival_time <= time:
            arrived.append(processes[i])
            i += 1

        # 🔁 Re-queue current process if not done
        if current.remaining_time > 0:
            queue.append(current)
        else:
            current.completion_time = time
            current.turnaround_time = time - current.arrival_time
            completed += 1

        # ✅ Append new arrivals AFTER the current process
        for p in arrived:
            queue.append(p)

    return gantt
