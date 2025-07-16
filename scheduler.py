def print_gantt(gantt):
    print("\nGantt Chart:")
    print("-" * 50)
    print("|", end="")
    for item in gantt:
        if isinstance(item, tuple):
            process, duration = item
        else:
            process, duration = item, 1  
        
        process_str = str(process)
        print(f" {process_str} ({duration}) |", end="")
    print("\n" + "-" * 50)
    
    time = 0
    print("0", end="")
    for item in gantt:
        if isinstance(item, tuple):
            process, duration = item
        else:
            process, duration = item, 1
        
        process_str = str(process)
        time += duration
        spacing = ' ' * len(process_str) + len(str(duration)) + 4
        print(f"{spacing}{time}", end="")
    print()

def print_metrics(processes):
    print("\nProcess Metrics:")
    print("-" * 80)
    print("| PID | Arrival | Burst | Completion | Turnaround | Waiting | Response |")
    print("-" * 80)
    total_turnaround = 0
    total_waiting = 0
    total_response = 0
    for p in sorted(processes, key=lambda x: x.pid):
        print(f"| P{p.pid:3} | {p.arrival_time:7} | {p.burst_time:5} | {p.completion_time:10} | {p.turnaround_time:10} | {p.waiting_time:7} | {p.response_time:8} |")
        total_turnaround += p.turnaround_time
        total_waiting += p.waiting_time
        total_response += p.response_time
    print("-" * 80)
    avg_turnaround = total_turnaround / len(processes)
    avg_waiting = total_waiting / len(processes)
    avg_response = total_response / len(processes)
    print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Response Time: {avg_response:.2f}")