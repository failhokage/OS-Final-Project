from process import Process 

def print_gantt_chart(processes, gantt):
    print("\nGantt Chart:")
    print("-" * 50)
    for time, pid in gantt:
        print(f"| P{pid} ", end="")
    print("|")
    print("-" * 50)
    print("0", end="")
    current_time = 0
    for time, pid in gantt:
        current_time += time
        print(f"     {current_time}", end="")
    print()

def print_metrics(processes):
    print("\nProcess Metrics:")
    print("PID | Arrival | Burst | Completion | Turnaround | Response")
    for p in sorted(processes, key=lambda x: x.pid):
        print(f"{p.pid:3} | {p.arrival_time:7} | {p.burst_time:5} | {p.completion_time:10} | {p.turnaround_time:10} | {p.response_time:8}")

def print_averages(processes):
    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
    avg_rt = sum(p.response_time for p in processes) / len(processes)
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")

def generate_random_processes(n):
    import random
    processes = []
    for i in range(n):
        at = random.randint(0, 10)
        bt = random.randint(1, 20)
        processes.append(Process(i, at, bt))
    return processes