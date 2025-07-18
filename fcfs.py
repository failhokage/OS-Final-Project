from process import Process
from utils import print_gantt_chart, print_metrics, print_averages

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    gantt = []
    current_time = 0
    
    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        
        execution_time = p.burst_time
        gantt.append((execution_time, p.pid))
        
        p.completion_time = current_time + execution_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.response_time = current_time - p.arrival_time
        current_time = p.completion_time
    
    return gantt

def run_fcfs(processes):
    print("\nRunning FCFS Scheduling Algorithm")
    gantt = fcfs(processes)
    print_gantt_chart(processes, gantt)
    print_metrics(processes)
    print_averages(processes)