import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
from collections import deque
from process import Process

class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        self.processes = []
        self.current_time = 0
        self.simulation_end_time = 0
        self.animation_id = None
        self.simulation_speed = 1.0
        self.is_simulating = False
        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        control_frame.pack(fill=tk.X)
        tk.Label(control_frame, text="Algorithm:", bg="#f0f0f0").grid(row=0, column=0, padx=2)
        self.algorithm = ttk.Combobox(control_frame, values=["FCFS", "SJF", "Round Robin", "MLFQ"], width=12)
        self.algorithm.grid(row=0, column=1, padx=2)
        self.algorithm.current(0)
        tk.Label(control_frame, text="Quantum:", bg="#f0f0f0").grid(row=0, column=2, padx=2)
        self.quantum_entry = tk.Entry(control_frame, width=4)
        self.quantum_entry.grid(row=0, column=3, padx=2)
        self.quantum_entry.insert(0, "4")
        tk.Button(control_frame, text="Add", command=self.add_process_dialog, width=6).grid(row=0, column=4, padx=2)
        tk.Button(control_frame, text="Random", command=self.generate_random, width=8).grid(row=0, column=5, padx=2)
        tk.Button(control_frame, text="Simulate", command=self.start_simulation, width=8).grid(row=0, column=6, padx=2)
        tk.Button(control_frame, text="Reset", command=self.reset, width=6).grid(row=0, column=7, padx=2)
        tk.Label(control_frame, text="Speed:", bg="#f0f0f0").grid(row=0, column=8, padx=2)
        self.speed_scale = tk.Scale(control_frame, from_=0.1, to=2.0, length=80, bg="#f0f0f0", highlightthickness=0)
        self.speed_scale.set(1.0)
        self.speed_scale.grid(row=0, column=9, padx=2)
        process_frame = tk.Frame(self.root, bg="#f0f0f0")
        process_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("PID", "Arrival", "Burst", "Priority", "Status")
        self.process_table = ttk.Treeview(process_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.process_table.heading(col, text=col)
            self.process_table.column(col, width=80, anchor=tk.CENTER)
        self.process_table.pack(fill=tk.BOTH, expand=True)
        gantt_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        gantt_frame.pack(fill=tk.BOTH, padx=10, pady=(0,10), ipady=5)
        self.gantt_canvas = tk.Canvas(gantt_frame, bg="white", highlightthickness=0)
        self.gantt_canvas.pack(fill=tk.BOTH, expand=True)
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        self.avg_waiting = tk.Label(stats_frame, text="Avg Waiting: --", bg="#f0f0f0", font=('Arial', 9))
        self.avg_waiting.pack(side=tk.LEFT, padx=10)
        self.avg_turnaround = tk.Label(stats_frame, text="Avg Turnaround: --", bg="#f0f0f0", font=('Arial', 9))
        self.avg_turnaround.pack(side=tk.LEFT, padx=10)
        self.total_time = tk.Label(stats_frame, text="Total Time: --", bg="#f0f0f0", font=('Arial', 9))
        self.total_time.pack(side=tk.LEFT, padx=10)
        self.progress_label = tk.Label(stats_frame, text="Progress: 0%", bg="#f0f0f0", font=('Arial', 9))
        self.progress_label.pack(side=tk.RIGHT, padx=10)

    def add_process_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Process")
        dialog.geometry("300x200")
        tk.Label(dialog, text="Arrival Time:").grid(row=0, column=0, padx=5, pady=5)
        arrival_entry = tk.Entry(dialog)
        arrival_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Burst Time:").grid(row=1, column=0, padx=5, pady=5)
        burst_entry = tk.Entry(dialog)
        burst_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
        priority_entry = tk.Entry(dialog)
        priority_entry.grid(row=2, column=1, padx=5, pady=5)
        def add():
            try:
                arrival = int(arrival_entry.get() or 0)
                burst = int(burst_entry.get())
                priority = int(priority_entry.get() or 0)
                pid = len(self.processes) + 1
                self.processes.append(Process(pid, arrival, burst, priority))
                self.update_process_table()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        tk.Button(dialog, text="Add", command=add).grid(row=3, columnspan=2, pady=10)

    def generate_random(self):
        try:
            count = simpledialog.askinteger("Random Processes", "Number of processes:", minvalue=1, maxvalue=20)
            max_arrival = simpledialog.askinteger("Random Processes", "Maximum arrival time:", minvalue=0)
            max_burst = simpledialog.askinteger("Random Processes", "Maximum burst time:", minvalue=1)
            max_priority = simpledialog.askinteger("Random Processes", "Maximum priority (0 for none):", minvalue=0) or 0
            if None in (count, max_arrival, max_burst):
                return
            self.processes = []
            for pid in range(1, count + 1):
                arrival = random.randint(0, max_arrival)
                burst = random.randint(1, max_burst)
                priority = random.randint(0, max_priority)
                self.processes.append(Process(pid, arrival, burst, priority))
            self.update_process_table()
            messagebox.showinfo("Success", f"Generated {count} random processes")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def update_process_table(self):
        self.process_table.delete(*self.process_table.get_children())
        for p in sorted(self.processes, key=lambda x: x.pid):
            status = "Ready" if p.remaining_time == p.burst_time else "Running" if p.remaining_time > 0 else "Completed"
            self.process_table.insert("", "end", values=(f"P{p.pid}", p.arrival_time, p.burst_time, p.priority, status))

    def set_speed(self, value):
        self.simulation_speed = float(value)

    def start_simulation(self):
        if not self.processes:
            messagebox.showerror("Error", "No processes to simulate")
            return
        if self.is_simulating:
            return
        self.is_simulating = True
        self.current_time = 0
        self.simulation_end_time = max(p.arrival_time + p.burst_time for p in self.processes)
        self.gantt_canvas.delete("all")
        algorithm = self.algorithm.get()
        quantum = int(self.quantum_entry.get())
        if algorithm == "FCFS":
            self.simulate_fcfs()
        elif algorithm == "SJF":
            self.simulate_sjf()
        elif algorithm == "Round Robin":
            self.simulate_rr(quantum)
        elif algorithm == "MLFQ":
            self.simulate_mlfq([quantum]*4, [10, 20, 40, 80])

    def simulate_fcfs(self):
        processes = sorted(self.processes.copy(), key=lambda x: x.arrival_time)
        self.animate_simulation(processes)

    def simulate_sjf(self):
        processes = sorted(self.processes.copy(), key=lambda x: x.arrival_time)
        self.animate_simulation(processes, sjf=True)

    def simulate_rr(self, quantum):
        processes = sorted(self.processes.copy(), key=lambda x: x.arrival_time)
        self.animate_simulation(processes, rr=True, quantum=quantum)

    def simulate_mlfq(self, quantums, allotments):
        processes = sorted(self.processes.copy(), key=lambda x: x.arrival_time)
        self.animate_simulation(processes, mlfq=True, quantums=quantums, allotments=allotments)

    def animate_simulation(self, processes, **kwargs):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        if not self.is_simulating or self.current_time > self.simulation_end_time:
            self.is_simulating = False
            self.calculate_stats()
            return
        self.update_simulation_step(processes, **kwargs)
        self.draw_gantt()
        delay = int(1000 / self.simulation_speed)
        self.animation_id = self.root.after(delay, lambda: self.animate_simulation(processes, **kwargs))

    def update_simulation_step(self, processes, **kwargs):
        self.current_time += 1
        for p in processes:
            if p.arrival_time <= self.current_time and p.remaining_time > 0:
                p.remaining_time -= 1
                if p.response_time == -1:
                    p.response_time = self.current_time - p.arrival_time
                if p.remaining_time == 0:
                    p.completion_time = self.current_time
                    p.turnaround_time = p.completion_time - p.arrival_time
                    p.waiting_time = p.turnaround_time - p.burst_time
        self.update_process_table()
        total_burst = sum(p.burst_time for p in self.processes)
        completed = sum(p.burst_time - p.remaining_time for p in self.processes)
        progress = int((completed / total_burst) * 100) if total_burst > 0 else 0
        self.progress_label.config(text=f"Progress: {progress}%")

    def draw_gantt(self):
        self.gantt_canvas.delete("all")
        width = self.gantt_canvas.winfo_width()
        height = self.gantt_canvas.winfo_height()
        max_time = max((p.completion_time for p in self.processes if p.completion_time > 0), default=max((p.arrival_time + p.burst_time for p in self.processes), default=1))
        time_scale = (width - 100) / max(1, max_time)
        row_height = 18
        chart_top = 20
        max_rows = (height - 40) // (row_height + 2)
        self.gantt_canvas.create_line(50, height-15, width-50, height-15, width=1, fill="#888")
        marker_step = max(1, round(max_time / 10))
        for t in range(0, max_time + 1, marker_step):
            x_pos = 50 + t * time_scale
            self.gantt_canvas.create_line(x_pos, height-10, x_pos, height-20, fill="#555")
            self.gantt_canvas.create_text(x_pos, height-8, text=str(t), font=('Arial', 7), anchor=tk.N)
        visible_processes = [p for p in self.processes if p.arrival_time <= self.current_time]
        rows = [[] for _ in range(max_rows)]
        for p in sorted(visible_processes, key=lambda x: x.arrival_time):
            executed = min(p.burst_time, max(0, self.current_time - p.arrival_time))
            if executed <= 0:
                continue
            start_x = 50 + p.arrival_time * time_scale
            end_x = start_x + executed * time_scale
            placed = False
            for row in rows:
                if not row or row[-1][1] <= start_x:
                    row.append((start_x, end_x, p))
                    placed = True
                    break
            if not placed and max_rows > 0:
                rows.append([(start_x, end_x, p)])
        for row_idx, row in enumerate(rows[:max_rows]):
            y_base = chart_top + row_idx * (row_height + 2)
            for start_x, end_x, p in row:
                self.gantt_canvas.create_rectangle(start_x, y_base, end_x, y_base + row_height, fill=p.color, outline="#333", width=0.5)
                if end_x - start_x > 20:
                    self.gantt_canvas.create_text((start_x + end_x)/2, y_base + row_height/2, text=f"P{p.pid}", font=('Arial', 7))
                if p.remaining_time > 0:
                    self.gantt_canvas.create_rectangle(end_x - 3, y_base, end_x, y_base + 3, fill="#ff0", outline="")
        current_x = 50 + min(self.current_time, max_time) * time_scale
        self.gantt_canvas.create_line(current_x, chart_top - 5, current_x, height-15, fill="#f00", width=1, arrow=tk.LAST)
        self.gantt_canvas.create_text(current_x, chart_top - 8, text=f"{self.current_time}", font=('Arial', 7, 'bold'), anchor=tk.S)

    def calculate_stats(self):
        completed = [p for p in self.processes if p.completion_time > 0]
        if not completed:
            return
        avg_wait = sum(p.waiting_time for p in completed) / len(completed)
        avg_turn = sum(p.turnaround_time for p in completed) / len(completed)
        total_time = max(p.completion_time for p in completed)
        self.avg_waiting.config(text=f"Avg Waiting: {avg_wait:.2f}")
        self.avg_turnaround.config(text=f"Avg Turnaround: {avg_turn:.2f}")
        self.total_time.config(text=f"Total Time: {total_time}")

    def reset(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        self.is_simulating = False
        self.current_time = 0
        self.processes = []
        self.process_table.delete(*self.process_table.get_children())
        self.gantt_canvas.delete("all")
        self.avg_waiting.config(text="Avg Waiting: --")
        self.avg_turnaround.config(text="Avg Turnaround: --")
        self.total_time.config(text="Total Time: --")
        self.progress_label.config(text="Progress: 0%")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()