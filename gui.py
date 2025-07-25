import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
import fcfs, sjf, srtf, round_robin, mlfq
from utils import generate_random_processes
import random

class CPUSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler GUI")
        self.geometry("1000x700")

        self.processes = []
        self.pid_colors = {"CS": "#cccccc"}
        self.animation_speed = 50

        self._build_input_frame()
        self._build_button_frame()
        self._build_gantt_frame()
        self._build_metrics_frame()

    def _build_input_frame(self):
        frame = ttk.LabelFrame(self, text="Add Process / Randomize", padding=8)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="PID:").grid(row=0, column=0)
        self.pid_var = tk.IntVar(value=0)
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

        ttk.Label(frame, text="RR/MLFQ Quantum:").grid(row=1, column=0, padx=(10,0), pady=5)
        self.mlfq_quantum = tk.IntVar(value=4)
        ttk.Entry(frame, textvariable=self.mlfq_quantum, width=6).grid(row=1, column=1)

        ttk.Label(frame, text="Time Allotment:").grid(row=1, column=2, padx=(20,0))
        self.mlfq_allotment = tk.IntVar(value=6)
        ttk.Entry(frame, textvariable=self.mlfq_allotment, width=6).grid(row=1, column=3)

        self.listbox = tk.Listbox(self, height=6)
        self.listbox.pack(fill="x", padx=10, pady=(0,10))

    def _build_button_frame(self):
        frame = ttk.Frame(self, padding=8)
        frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame, text="Choose Algorithm:").pack(side="left", padx=(0,10))
        ttk.Button(frame, text="FCFS", command=self.run_fcfs).pack(side="left", padx=4)
        ttk.Button(frame, text="SJF",  command=self.run_sjf).pack(side="left", padx=4)
        ttk.Button(frame, text="SRTF", command=self.run_srtf).pack(side="left", padx=4)
        ttk.Button(frame, text="RR",   command=self.run_rr).pack(side="left", padx=4)
        ttk.Button(frame, text="MLFQ", command=self.run_mlfq).pack(side="left", padx=4)
        ttk.Button(frame, text="Export Results", command=self.export_results).pack(side="left", padx=4)

    def _build_gantt_frame(self):
        frame = ttk.LabelFrame(self, text="Gantt Chart", padding=8)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas_frame = tk.Frame(frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, height=120, bg="white", scrollregion=(0, 0, 3000, 120))
        self.canvas.pack(side="top", fill="both", expand=True)

        self.h_scroll = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.h_scroll.set)

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

    def _assign_colors(self):
        for p in self.processes:
            if p.pid not in self.pid_colors:
                r = int((random.random() + 1) * 127)
                g = int((random.random() + 1) * 127)
                b = int((random.random() + 1) * 127)
                self.pid_colors[p.pid] = f'#{r:02x}{g:02x}{b:02x}'

    # Assign gray color to IDLE
        self.pid_colors["IDLE"] = "#A9A9A9"
        
    def _add_context_switches(self, gantt):
        full = []
        for i, (dur, pid) in enumerate(gantt):
            if i > 0 and gantt[i-1][1] != pid:
                full.append((0, "CS"))
            full.append((dur, pid))
        return full

    def _show_metrics(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in sorted(self.processes, key=lambda x: x.pid):
            self.tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time,
                                                p.completion_time, p.turnaround_time, p.response_time))
        if self.processes:
            avg_tat = sum(p.turnaround_time for p in self.processes) / len(self.processes)
            avg_rt  = sum(p.response_time   for p in self.processes) / len(self.processes)
            self.avg_tat_var.set(f"{avg_tat:.2f}")
            self.avg_rt_var.set(f"{avg_rt:.2f}")

    def animate_gantt(self, gantt):
        self.canvas.delete("all")
        full = self._add_context_switches(gantt)
        self._assign_colors()
        self._draw_segment(full, idx=0, x=10, elapsed=0)  # Always start at 0


    def _draw_segment(self, full, idx, x, elapsed):
        if idx >= len(full):
            self._show_metrics()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
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

    def add_process(self):
        pid, at, bt = self.pid_var.get(), self.at_var.get(), self.bt_var.get()
        if any(p.pid == pid for p in self.processes):
            messagebox.showerror("Error", f"PID {pid} already exists.")
            return
        self.processes.append(Process(pid, at, bt))
        self._assign_colors()
        self.listbox.insert("end", f"P{pid}  AT={at}  BT={bt}")

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

    def generate_processes(self):
        n = self.random_n.get()
        self.processes = generate_random_processes(n)
        self._assign_colors()
        self.listbox.delete(0, tk.END)
        for p in self.processes:
            self.listbox.insert("end", f"P{p.pid}  AT={p.arrival_time}  BT={p.burst_time}")
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_tat_var.set("0.00")
        self.avg_rt_var.set("0.00")

    def run_fcfs(self):
        for p in self.processes:
            p.remaining_time, p.first_execution = p.burst_time, -1
        gantt = fcfs.fcfs(self.processes)
        self.animate_gantt(gantt)

    def run_sjf(self):
        for p in self.processes:
            p.remaining_time, p.first_execution = p.burst_time, -1
        gantt = sjf.sjf(self.processes)
        self.animate_gantt(gantt)

    def run_srtf(self):
        for p in self.processes:
            p.remaining_time   = p.burst_time
            p.first_execution  = -1
            p.completion_time  = 0
            p.response_time    = -1
            p.turnaround_time  = 0
        gantt = srtf.srtf(self.processes)
        self.animate_gantt(gantt)

    def run_rr(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        for p in self.processes:
            p.remaining_time   = p.burst_time
            p.first_execution  = -1
            p.completion_time  = 0
            p.response_time    = -1
            p.turnaround_time  = 0
        tq = self.mlfq_quantum.get()
        try:
            gantt = round_robin.rr(self.processes, tq)
        except Exception as e:
            messagebox.showerror("RR Error", str(e))
            return
        if not gantt:
            messagebox.showinfo("RR", "No scheduling steps generated.")
            return
        self.animate_gantt(gantt)

    def run_mlfq(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add or generate processes first.")
            return
        for p in self.processes:
            p.remaining_time   = p.burst_time
            p.first_execution  = -1
            p.completion_time  = 0
            p.response_time    = -1
            p.turnaround_time  = 0
            p.priority         = 0
            p.remaining_quantum = 0
            p.allotment = 0

        quantum = self.mlfq_quantum.get()
        allotment = self.mlfq_allotment.get()
        queues_config = [
            (0, quantum, allotment),
            (1, quantum * 2, allotment * 2),
            (2, None, 1000)
        ]
        try:
            gantt = mlfq.mlfq(self.processes, queues_config)
        except Exception as e:
            messagebox.showerror("MLFQ Error", str(e))
            return
        if not gantt:
            messagebox.showinfo("MLFQ", "No scheduling steps generated.")
            return
        self.animate_gantt(gantt)

    def export_results(self):
        if not self.processes:
            messagebox.showwarning("No Data", "No process data to export.")
            return

        try:
            with open("scheduling_results.txt", "w") as f:
                f.write("PID\tAT\tBT\tCT\tTAT\tRT\n")
                for p in sorted(self.processes, key=lambda x: x.pid):
                    f.write(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t"
                            f"{p.completion_time}\t{p.turnaround_time}\t{p.response_time}\n")
                avg_tat = sum(p.turnaround_time for p in self.processes) / len(self.processes)
                avg_rt = sum(p.response_time for p in self.processes) / len(self.processes)
                f.write(f"\nAverage Turnaround Time: {avg_tat:.2f}\n")
                f.write(f"Average Response Time: {avg_rt:.2f}\n")

            messagebox.showinfo("Export Successful", "Results saved to 'scheduling_results.txt'")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))


if __name__ == "__main__":
    CPUSchedulerGUI().mainloop()
