from process import Process
from utils import generate_random_processes
from fcfs import run_fcfs
from sjf import run_sjf
from srtf import run_srtf
from round_robin import run_round_robin
from mlfq import run_mlfq

def get_processes():
    print("\nProcess Input Method:")
    print("1. Manual Input")
    print("2. Random Generation")
    choice = int(input("Enter your choice (1-2): "))
    
    if choice == 1:
        processes = []
        n = int(input("Enter number of processes: "))
        for i in range(n):
            at = int(input(f"Enter arrival time for P{i}: "))
            bt = int(input(f"Enter burst time for P{i}: "))
            processes.append(Process(i, at, bt))
        return processes
    else:
        n = int(input("Enter number of processes: "))
        return generate_random_processes(n)

def main():
    print("CPU Scheduling Algorithm Simulator")
    
    while True:
        processes = get_processes()
        
        print("\nSelect scheduling algorithm:")
        print("1. FCFS")
        print("2. SJF (Non-Preemptive)")
        print("3. SRTF (Preemptive)")
        print("4. Round Robin")
        print("5. MLFQ")
        print("6. Exit")
        choice = int(input("Enter your choice (1-6): "))
        
        if choice == 1:
            run_fcfs(processes.copy())
        elif choice == 2:
            run_sjf(processes.copy())
        elif choice == 3:
            run_srtf(processes.copy())
        elif choice == 4:
            run_round_robin(processes.copy())
        elif choice == 5:
            run_mlfq(processes.copy())
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()