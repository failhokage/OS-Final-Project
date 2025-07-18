from process import Process
from utils import print_gantt_chart, print_metrics, print_averages


def round_robin(processes, quantum):
    processes.sort(key=lambda x: x.arrival_time)
    gantt = []
    current_time = 0
    queue = []
    remaining = [p for p in processes]
    prev_pid = -1
    
    while remaining or queue:
   
        new_arrivals = [p for p in remaining if p.arrival_time <= current_time]
        for p in new_arrivals:
            queue.append(p)
            remaining.remove(p)
        
        if not queue:
            current_time += 1
            continue
            
        p = queue.pop(0)
        
    
        if p.first_execution == -1:
            p.first_execution = current_time
        
     
        exec_time = min(quantum, p.remaining_time)
        
     
        if prev_pid != p.pid:
            gantt.append((exec_time, p.pid))
        else:
            gantt[-1] = (gantt[-1][0] + exec_time, gantt[-1][1])
        prev_pid = p.pid
        
        p.remaining_time -= exec_time
        current_time += exec_time
        
      
        new_arrivals = [p for p in remaining if p.arrival_time <= current_time]
        for new_p in new_arrivals:
            queue.append(new_p)
            remaining.remove(new_p)
        
        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.response_time = p.first_execution - p.arrival_time
    
    return gantt

def run_round_robin(processes):
    print("\nRunning Round Robin Scheduling Algorithm")
    quantum = int(input("Enter time quantum: "))
    gantt = round_robin(processes, quantum)
    print_gantt_chart(processes, gantt)
    print_metrics(processes)
    print_averages(processes)