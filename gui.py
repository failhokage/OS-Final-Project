import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
import fcfs, sjf, srtf
from utils import generate_random_processes
import random

class CPUSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler GUI")
        self.geometry("900x650")

        self.processes = []
        self.pid_colors = {"CS": "#cccccc"}   
        self.animation_speed = 300            

        self._build_input_frame()
        self._build_button_frame()
        self._build_gantt_frame()
        self._build_metrics_frame()

    def _build_input_frame(self):
        frame = ttk.LabelFrame(self, text="Add Process / Randomize", padding=8)
        frame.pack(fill="x", padx=10, pady=5)


        ttk.Label(frame, text="PID:").grid(row=0, column=0)
        self.pid_var = tk.IntVar()
        ttk.Entry(frame, textvariable=self.pid_var, width=6).grid(row=0, column=1)

        ttk.Label(frame, text="Arrival Time:").grid(row=0, column=2)
        self.at_var = tk.IntVar()
        ttk.Entry(frame, textvariable=self.at_var, width=6).grid(row=0, column=3)

        ttk.Label(frame, text="Burst Time:").grid(row=0, column=4)
        self.bt_var = tk.IntVar()
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
        ttk.Label(frame, text="Choose Algorithm:").pack(side="left")
        ttk.Button(frame, text="FCFS", command=self.run_fcfs).pack(side="left", padx=8)
        ttk.Button(frame, text="SJF",  command=self.run_sjf).pack(side="left", padx=8)
        ttk.Button(frame, text="SRTF", command=self.run_srtf).pack(side="left", padx=8)

    def _build_gantt_frame(self):
        frame = ttk.LabelFrame(self, text="Gantt Chart", padding=8)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(frame, height=120, bg="white")
        self.canvas.pack(fill="x", expand=True)

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
                # pastel random color
                r = int((random.random()+1)*127)
                g = int((random.random()+1)*127)
                b = int((random.random()+1)*127)
                self.pid_colors[p.pid] = f'#{r:02x}{g:02x}{b:02x}'

    def _add_context_switches(self, gantt):
        """Return a new gantt list with (1,'CS') between pid changes."""
        full = []
        for i, (dur, pid) in enumerate(gantt):
            if i>0 and gantt[i-1][1] != pid:
                full.append((1, "CS"))
            full.append((dur, pid))
        return full

    def _show_metrics(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in sorted(self.processes, key=lambda x: x.pid):
            vals = (
                p.pid, p.arrival_time, p.burst_time,
                p.completion_time, p.turnaround_time, p.response_time
            )
            self.tree.insert("", "end", values=vals)

        if self.processes:
            avg_tat = sum(p.turnaround_time for p in self.processes) / len(self.processes)
            avg_rt  = sum(p.response_time   for p in self.processes) / len(self.processes)
            self.avg_tat_var.set(f"{avg_tat:.2f}")
            self.avg_rt_var.set(f"{avg_rt:.2f}")

    def animate_gantt(self, gantt):
        """Animate each block (including CS) in sequence."""
        self.canvas.delete("all")
        full = self._add_context_switches(gantt)
        self._assign_colors()
        self._draw_segment(full, idx=0, x=10, elapsed=0)

    def _draw_segment(self, full, idx, x, elapsed):
        if idx >= len(full):
            self._show_metrics()
            return

        dur, pid = full[idx]
        color = self.pid_colors.get(pid, "#87CEEB")
        scale = 25
        width = dur * scale


        self.canvas.create_rectangle(x, 20, x+width, 100, fill=color, outline="black")
        label = "CS" if pid=="CS" else f"P{pid}"
        self.canvas.create_text(x + width/2, 60, text=label, font=("Arial",10,"bold"))


        self.canvas.create_text(x, 105, text=str(elapsed), anchor="n")


        new_elapsed = elapsed + dur
        delay = self.animation_speed * dur
        self.after(delay,
            lambda: self._draw_segment(full, idx+1, x+width, new_elapsed)
        )


        if idx == len(full)-1:
            self.after(delay,
                lambda: self.canvas.create_text(x+width, 105,
                                                text=str(new_elapsed),
                                                anchor="n")
            )

    def add_process(self):
        pid, at, bt = self.pid_var.get(), self.at_var.get(), self.bt_var.get()
        if any(p.pid==pid for p in self.processes):
            messagebox.showerror("Error", f"PID {pid} already exists.")
            return
        self.processes.append(Process(pid, at, bt))
        self._assign_colors()
        self.listbox.insert("end", f"P{pid}  AT={at}  BT={bt}")

    def clear_processes(self):
        self.processes.clear()
        self.pid_colors = {"CS": "#cccccc"}
        self.listbox.delete(0, "end")
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_tat_var.set("0.00")
        self.avg_rt_var.set("0.00")

    def generate_processes(self):
        n = self.random_n.get()
        self.processes = generate_random_processes(n)
        self._assign_colors()
        self.listbox.delete(0, "end")
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

if __name__ == "__main__":
    CPUSchedulerGUI().mainloop()
