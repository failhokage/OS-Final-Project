from process import Process
from utils import print_gantt_chart, print_metrics, print_averages

def srtf(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    gantt = []
    last_pid = None

    while completed != n:
        # Get ready processes
        ready = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not ready:
            # Batch IDLE time
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            idle_duration = next_arrival - current_time
            if last_pid != "IDLE":
                gantt.append((idle_duration, "IDLE"))
                last_pid = "IDLE"
            else:
                gantt[-1] = (gantt[-1][0] + idle_duration, "IDLE")
            current_time = next_arrival
            continue

        # Select process with shortest remaining time
        p = min(ready, key=lambda x: x.remaining_time)

        # Set response time BEFORE execution
        if p.response_time == -1:
            p.response_time = current_time - p.arrival_time

        # Update Gantt chart
        if last_pid != p.pid:
            gantt.append((1, p.pid))
            last_pid = p.pid
        else:
            gantt[-1] = (gantt[-1][0] + 1, gantt[-1][1])  # Extend current block

        # Execute process for 1 time unit
        p.remaining_time -= 1

        if p.remaining_time == 0:
            p.completion_time = current_time + 1
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

            completed += 1

        current_time += 1

    return gantt
