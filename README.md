# OS Final Project – CPU Scheduling Simulator

This project is our final requirement for Operating Systems. It simulates different CPU scheduling algorithms using Python and runs in the terminal.

## Features

We implemented the following scheduling algorithms:

- First-Come, First-Served (FCFS)
- Shortest Job First (SJF) – Non-Preemptive
- Shortest Remaining Time First (SRTF) – Preemptive
- Round Robin (RR)
- Multilevel Feedback Queue (MLFQ)

## How to Run

1. Make sure Python is installed.
2. Clone or download the repository.
3. Open the folder in VS Code or any IDE.
4. Run:

The output will show process info, waiting time, turnaround time, and averages.

## 📁 Files and Folders

- main.py – entry point, lets you select a scheduler
- process.py – defines the Process class
- fcfs.py – FCFS implementation
- sjf.py – SJF implementation
- srtf.py – SRTF implementation
- round_robin.py – Round Robin implementation
- mlfq.py – MLFQ implementation
- utils.py (optional) – helper functions
- README.md – this file

## 🧪 Sample Output (FCFS)


## 👨‍👩‍👧‍👦 Group Members and Contributions

| Name                | Work Done                              |
|---------------------|----------------------------------------|
| Christian Demetillo | GitHub, FCFS, structure, README, GUI   |
| Mary Vincent Lopez  | SJF, SRTF, MLFQ                        |


## ✅ Assumptions

- All processes are known at the start
- No I/O or interruptions
- No context switching time
- One core (single CPU)
- Input values are valid

## 📌 Notes

This project is for academic use only and meant to help us understand how CPU schedulers work.
