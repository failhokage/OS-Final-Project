import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
import random
import copy

class CPUSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler GUI")
        self.geometry("900x650")
        self.processes = []
        self.pid_colors = {"CS": "#cccccc"}
        self.animation_speed = 300
        self.next_pid = 0
        self._build_input_frame()
        self._build_button_frame()
        self._build_gantt_frame()
        self._build_metrics_frame()

    def add_process(self):
        pid, at, bt = self.pid_var.get(), self.at_var.get(), self.bt_var.get()
        if any(p.pid == pid for p in self.processes):
            messagebox.showerror("Error", f"PID {pid} already exists.")
            return
        self.processes.append(Process(pid, at, bt))
        self._assign_colors()
        self.listbox.insert("end", f"P{pid} AT={at} BT={bt}")
        self.next_pid = max(p.pid for p in self.processes) + 1 if self.processes else 0
        self.pid_var.set(self.next_pid)

    def clear_processes(self):
        self.processes.clear()
        self.pid_colors = {"CS": "#cccccc"}
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_tat_var.set("0.00")
        self.avg_rt_var.set("0.00")
        self.pid_var.set(0)
        self.at_var.set(0)
        self.bt_var.set(0)
        self.random_n.set(5)
        self.mlfq_quantum_var.set(2)
        self.next_pid = 0
        self.algorithm_var.set("Selected Algorithm: None")

    def generate_processes(self):
        n = self.random_n.get()
        self.processes = [Process(i, random.randint(0, 10), random.randint(1, 20)) for i in range(n)]
        self._assign_colors()
        self.listbox.delete(0, tk.END)
        for p in self.processes:
            self.listbox.insert("end", f"P{p.pid} AT={p.arrival_time} BT={p.burst_time}")
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_tat_var.set("0.00")
        self.avg_rt_var.set("0.00")
        self.next_pid = max(p.pid for p in self.processes) + 1 if self.processes else 0
        self.pid_var.set(self.next_pid)

    def _build_input_frame(self):
        frame = ttk.LabelFrame(self, text="Add Process / Randomize", padding=8)
        frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame, text="PID:").grid(row=0, column=0)
        self.pid_var = tk.IntVar(value=self.next_pid)
        ttk.Entry(frame, textvariable=self.pid_var, width=6).grid(row=0, column=1)
        ttk.Label(frame, text="Arrival Time:").grid(row=0, column=2)
        self.at_var = tk.IntVar(value=0)
        ttk.Entry(frame, textvariable=self.at_var, width=6).grid(row=0, column=3)
        ttk.Label(frame, text="Burst Time:").grid(row=0, column=4)
        self.bt_var = tk.IntVar(value=0)
        ttk.Entry(frame, textvariable=self.bt_var, width=6).grid(row=0, column=5)
        ttk.Button(frame, text="Add", command=self.add_process).grid(row=0, column=6, padx=6)
        ttk.Button(frame, text="Clear All", command=self.clear_processes).grid(row=0, column=7)
        ttk.Label(frame, text="Random N:").grid(row=0, column=8, padx=(20,0))
        self.random_n = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=1, to=20, textvariable=self.random_n, width=6).grid(row=0, column=9)
        ttk.Button(frame, text="Generate", command=self.generate_processes).grid(row=0, column=10, padx=6)
        self.listbox = tk.Listbox(self, height=6)
        self.listbox.pack(fill="x", padx=10, pady=(0,10))

    def _build_button_frame(self):
        frame = ttk.Frame(self, padding=8)
        frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame, text="Choose Algorithm:").pack(side="left", padx=(0,10))
        ttk.Button(frame, text="FCFS", command=lambda: self.run_algorithm("FCFS")).pack(side="left", padx=4)
        ttk.Button(frame, text="SJF", command=lambda: self.run_algorithm("SJF")).pack(side="left", padx=4)
        ttk.Button(frame, text="SRTF", command=lambda: self.run_algorithm("SRTF")).pack(side="left", padx=4)
        ttk.Button(frame, text="RR", command=lambda: self.run_algorithm("RR")).pack(side="left", padx=4)
        self.mlfq_quantum_var = tk.IntVar(value=2)
        mlfq_frame = ttk.Frame(frame)
        mlfq_frame.pack(side="left", padx=4)
        ttk.Button(mlfq_frame, text="MLFQ", command=lambda: self.run_algorithm("MLFQ")).pack(side="left")
        ttk.Label(mlfq_frame, text="Quantum:").pack(side="left", padx=(5,0))
        ttk.Entry(mlfq_frame, textvariable=self.mlfq_quantum_var, width=6).pack(side="left")
        self.algorithm_var = tk.StringVar(value="Selected Algorithm: None")
        ttk.Entry(frame, textvariable=self.algorithm_var, width=25, state='readonly', font=('Arial', 10), justify='center').pack(side="left", padx=10)

    def _build_gantt_frame(self):
        frame = ttk.LabelFrame(self, text="Gantt Chart", padding=8)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)
        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(container, height=120, bg="white", xscrollcommand=xscrollbar.set, scrollregion=(0, 0, 2000, 120))
        self.canvas.pack(fill="both", expand=True)
        xscrollbar.config(command=self.canvas.xview)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.xview_scroll(-1 * int(event.delta/120), "units")

    def _build_metrics_frame(self):
        frame = ttk.LabelFrame(self, text="Metrics", padding=8)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        cols = ("PID", "AT", "BT", "CT", "TAT", "RT")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=70, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)
        avg_frame = ttk.Frame(frame)
        avg_frame.pack(fill="x", pady=(10,0))
        ttk.Label(avg_frame, text="Average TAT:").pack(side="left", padx=(0,5))
        self.avg_tat_var = tk.StringVar(value="0.00")
        ttk.Label(avg_frame, textvariable=self.avg_tat_var).pack(side="left", padx=(0,20))
        ttk.Label(avg_frame, text="Average RT:").pack(side="left", padx=(0,5))
        self.avg_rt_var = tk.StringVar(value="0.00")
        ttk.Label(avg_frame, textvariable=self.avg_rt_var).pack(side="left")

    def run_algorithm(self, algo_name):
        self.algorithm_var.set(f"Selected Algorithm: {algo_name}")
        if algo_name == "FCFS":
            self.run_fcfs()
        elif algo_name == "SJF":
            self.run_sjf()
        elif algo_name == "SRTF":
            self.run_srtf()
        elif algo_name == "RR":
            self.run_rr()
        elif algo_name == "MLFQ":
            self.run_mlfq()

    def _assign_colors(self):
        for p in self.processes:
            if p.pid not in self.pid_colors:
                r = int((random.random() + 1) * 127)
                g = int((random.random() + 1) * 127)
                b = int((random.random() + 1) * 127)
                self.pid_colors[p.pid] = f'#{r:02x}{g:02x}{b:02x}'

    def _add_context_switches(self, gantt):
        full = []
        for i, (start, end, pid) in enumerate(gantt):
            if i > 0 and gantt[i-1][2] != pid:
                full.append((0, "CS"))
            full.append((end - start, pid))
        return full

    def _show_metrics(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in sorted(self.processes, key=lambda x: x.pid):
            self.tree.insert("", "end", values=(
                p.pid, p.arrival_time, p.burst_time,
                p.completion_time, p.turnaround_time, p.response_time
            ))
        if self.processes:
            avg_tat = sum(p.turnaround_time for p in self.processes) / len(self.processes)
            avg_rt = sum(p.response_time for p in self.processes) / len(self.processes)
            self.avg_tat_var.set(f"{avg_tat:.2f}")
            self.avg_rt_var.set(f"{avg_rt:.2f}")

    def animate_gantt(self, gantt):
        self.canvas.delete("all")
        full = self._add_context_switches(gantt)
        self._assign_colors()
        total_time = sum(duration for duration, pid in full if pid != "CS")
        total_width = total_time * 25 + 100
        self.canvas.configure(scrollregion=(0, 0, total_width, 120))
        self._draw_segment(full, idx=0, x=10, elapsed=0)

    def _draw_segment(self, full, idx, x, elapsed):
        if idx >= len(full):
            self._show_metrics()
            return
        dur, pid = full[idx]
        scale = 25
        if pid == "CS":
            self.canvas.create_line(x, 20, x, 100, fill="black")
            self.canvas.create_text(x, 105, text=str(elapsed), anchor="n")
            self._draw_segment(full, idx+1, x, elapsed)
            return
        width = dur * scale
        color = self.pid_colors.get(pid, "#87CEEB")
        self.canvas.create_rectangle(x, 20, x+width, 100, fill=color, outline="black")
        self.canvas.create_text(x + width/2, 60, text=f"P{pid}", font=("Arial", 10, "bold"))
        self.canvas.create_text(x, 105, text=str(elapsed), anchor="n")
        new_elapsed = elapsed + dur
        delay = self.animation_speed * dur
        self.after(delay, lambda: self._draw_segment(full, idx+1, x+width, new_elapsed))
        if idx == len(full) - 1:
            self.after(delay, lambda: self.canvas.create_text(x+width, 105, text=str(new_elapsed), anchor="n"))

    def run_fcfs(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        temp_processes = [copy.deepcopy(p) for p in self.processes]
        temp_processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        gantt = []
        for p in temp_processes:
            if current_time < p.arrival_time:
                current_time = p.arrival_time
            gantt.append((current_time, current_time + p.burst_time, p.pid))
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.response_time = current_time - p.arrival_time
            current_time += p.burst_time
        self._update_process_metrics(temp_processes)
        self.animate_gantt(gantt)

    def run_sjf(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        temp_processes = [copy.deepcopy(p) for p in self.processes]
        current_time = 0
        gantt = []
        remaining_processes = temp_processes.copy()
        while remaining_processes:
            arrived = [p for p in remaining_processes if p.arrival_time <= current_time]
            if not arrived:
                current_time += 1
                continue
            arrived.sort(key=lambda x: x.burst_time)
            p = arrived[0]
            gantt.append((current_time, current_time + p.burst_time, p.pid))
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.response_time = current_time - p.arrival_time
            current_time += p.burst_time
            remaining_processes.remove(p)
        self._update_process_metrics(temp_processes)
        self.animate_gantt(gantt)

    def run_srtf(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        temp_processes = [copy.deepcopy(p) for p in self.processes]
        current_time = 0
        gantt = []
        remaining_processes = temp_processes.copy()
        while remaining_processes:
            arrived = [p for p in remaining_processes if p.arrival_time <= current_time and p.remaining_time > 0]
            if not arrived:
                current_time += 1
                continue
            arrived.sort(key=lambda x: x.remaining_time)
            p = arrived[0]
            start_time = current_time
            current_time += 1
            p.remaining_time -= 1
            if not gantt or gantt[-1][2] != p.pid:
                gantt.append((start_time, current_time, p.pid))
            else:
                last = gantt[-1]
                gantt[-1] = (last[0], current_time, last[2])
            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                remaining_processes.remove(p)
        self._update_process_metrics(temp_processes)
        self.animate_gantt(gantt)

    def run_rr(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        quantum = 3
        temp_processes = [copy.deepcopy(p) for p in self.processes]
        current_time = 0
        gantt = []
        queue = []
        remaining_processes = temp_processes.copy()
        while remaining_processes:
            new_arrivals = [p for p in remaining_processes if p.arrival_time <= current_time and p not in queue and p.remaining_time > 0]
            queue.extend(new_arrivals)
            if not queue:
                current_time += 1
                continue
            p = queue.pop(0)
            if p.first_execution == -1:
                p.first_execution = current_time
                p.response_time = p.first_execution - p.arrival_time
            exec_time = min(quantum, p.remaining_time)
            start_time = current_time
            current_time += exec_time
            p.remaining_time -= exec_time
            gantt.append((start_time, current_time, p.pid))
            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                remaining_processes.remove(p)
            else:
                queue.append(p)
        self._update_process_metrics(temp_processes)
        self.animate_gantt(gantt)

    def run_mlfq(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        quantum = self.mlfq_quantum_var.get()
        if quantum <= 0:
            messagebox.showerror("Error", "Quantum must be greater than 0")
            return
        temp_processes = [copy.deepcopy(p) for p in self.processes]
        for p in temp_processes:
            p.priority = 0
            p.remaining_time = p.burst_time
            p.first_execution = -1
            p.completion_time = -1
            p.response_time = -1
            p.turnaround_time = -1
            p.allotment = 5
            p.quantum = quantum
            p.last_executed = -1
            p.completed = False
        current_time = 0
        gantt = []
        queues = [[] for _ in range(3)]
        while True:
            for p in temp_processes:
                if p.arrival_time <= current_time and not p.completed and p not in queues[0] + queues[1] + queues[2]:
                    queues[0].append(p)
            current_queue = next((q for q in queues if q), None)
            if not current_queue:
                if all(p.completed for p in temp_processes):
                    break
                current_time += 1
                continue
            p = current_queue.pop(0)
            if p.first_execution == -1:
                p.first_execution = current_time
                p.response_time = p.first_execution - p.arrival_time
            exec_time = min(p.quantum, p.remaining_time)
            start_time = current_time
            current_time += exec_time
            p.remaining_time -= exec_time
            p.allotment -= exec_time
            gantt.append((start_time, current_time, p.pid))
            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.completed = True
            else:
                if p.allotment <= 0 and p.priority < 2:
                    p.priority += 1
                    p.allotment = 5
                    p.quantum *= 2
                queues[p.priority].append(p)
        self._update_process_metrics(temp_processes)
        self.animate_gantt(gantt)

    def _update_process_metrics(self, temp_processes):
        for temp_p in temp_processes:
            for orig_p in self.processes:
                if orig_p.pid == temp_p.pid:
                    orig_p.completion_time = temp_p.completion_time
                    orig_p.turnaround_time = temp_p.turnaround_time
                    orig_p.response_time = temp_p.response_time
                    break

    def clear_display(self):
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_tat_var.set("0.00")
        self.avg_rt_var.set("0.00")

if __name__ == "__main__":
    CPUSchedulerGUI().mainloop()