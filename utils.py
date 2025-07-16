import random
from process import Process

def manual_input():
    processes = []
    pid = 1
    print("\nManual Process Entry")
    
    while True:
        print(f"\nProcess P{pid}")
        arrival = input("Arrival Time (0 if not specified): ")
        burst = input("Burst Time: ")
        
        if not burst:
            break
            
        try:
            arrival = int(arrival) if arrival else 0
            burst = int(burst)
            processes.append(Process(pid, arrival, burst))
            pid += 1
        except ValueError:
            print("Please enter valid numbers")
            continue
            
    return processes

def random_input():
    try:
        n = int(input("\nNumber of processes: "))
        max_arrival = int(input("Maximum arrival time: "))
        max_burst = int(input("Maximum burst time: "))
        
        processes = []
        for pid in range(1, n+1):
            arrival = random.randint(0, max_arrival)
            burst = random.randint(1, max_burst)
            processes.append(Process(pid, arrival, burst))
            
        return processes
    except ValueError:
        print("Please enter valid numbers")
        return []