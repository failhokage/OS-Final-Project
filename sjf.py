from process import Process
from utils import print_gantt_chart, print_metrics, print_averages

def sjf(processes):
    processes.sort(key=lambda x: x.arrival_time)
    gantt = []
    current_time = 0
    completed = 0
    n = len(processes)

    while completed != n:
        # Filter ready processes
        ready = [p for p in processes if p.arrival_time <= current_time and p.remaining_time == p.burst_time]
        ready.sort(key=lambda x: x.burst_time)

        if not ready:
            # IDLE until the next arrival
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time == p.burst_time)
            if current_time < next_arrival:
                gantt.append((next_arrival - current_time, "IDLE"))
                current_time = next_arrival
            continue

        p = ready[0]
        execution_time = p.burst_time
        gantt.append((execution_time, p.pid))

        p.completion_time = current_time + execution_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.response_time = current_time - p.arrival_time
        p.remaining_time = 0
        current_time = p.completion_time
        completed += 1

    return gantt

def run_sjf(processes):
    print("\nRunning SJF (Non-Preemptive) Scheduling Algorithm")
    gantt = sjf(processes)
    print_gantt_chart(processes, gantt)
    print_metrics(processes)
    print_averages(processes)
