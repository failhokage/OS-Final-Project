from process import Process
from utils import print_gantt_chart, print_metrics, print_averages

def srtf(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.pid))
    gantt = []
    current_time = 0
    completed = 0
    n = len(processes)
    prev_pid = None
    last_start = 0
    
    while completed < n:
      
        ready = [p for p in processes 
                if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if ready:
        
            ready.sort(key=lambda x: (x.remaining_time, x.arrival_time, x.pid))
            current_p = ready[0]
            
          
            if current_p.pid != prev_pid:
                if prev_pid is not None:
                    gantt.append((current_time - last_start, prev_pid))
                last_start = current_time
                prev_pid = current_p.pid
                
              
                if current_p.first_execution == -1:
                    current_p.first_execution = current_time
            
        
            current_p.remaining_time -= 1
            current_time += 1
            
          
            if current_p.remaining_time == 0:
                gantt.append((current_time - last_start, current_p.pid))
                prev_pid = None
                current_p.completion_time = current_time
                current_p.turnaround_time = current_p.completion_time - current_p.arrival_time
                current_p.response_time = current_p.first_execution - current_p.arrival_time
                completed += 1
        else:
            current_time += 1
    
    return gantt

def run_srtf(processes):
    """
    Run SRTF scheduling and print results
    Args:
        processes: List of Process objects
    """
    print("\nRunning SRTF (Preemptive) Scheduling Algorithm")
    
   
    for p in processes:
        p.remaining_time = p.burst_time
        p.first_execution = -1
        p.completion_time = 0
        p.response_time = -1
        p.turnaround_time = 0
    

    gantt = srtf(processes)
    
   
    print_gantt_chart(processes, gantt)
    print_metrics(processes)
    print_averages(processes)