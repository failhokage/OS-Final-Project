from collections import deque

def mlfq(processes, queues_config):
    n = len(processes)
    gantt = []
    time = 0
    completed = 0
    ready_queues = [deque() for _ in queues_config]
    active = [False] * n
    processes.sort(key=lambda p: p.arrival_time)

    def enqueue(proc, level):
        proc.priority = level
        tq = queues_config[level][1]
        allot = queues_config[level][2]
        proc.remaining_quantum = tq if tq else 9999
        proc.allotment = allot
        ready_queues[level].append(proc)

    def check_arrivals(curr_time):
        for proc in processes:
            if not active[proc.pid] and proc.arrival_time <= curr_time:
                enqueue(proc, 0)
                active[proc.pid] = True

    current_proc = None
    current_level = None

    while completed < n:
        check_arrivals(time)

        for level, queue in enumerate(ready_queues):
            if queue:
                current_proc = queue.popleft()
                current_level = level
                break
        else:
            time += 1
            continue

        if current_proc.first_execution == -1:
            current_proc.first_execution = time
            current_proc.response_time = time - current_proc.arrival_time

        tq = queues_config[current_level][1]
        exec_time = min(current_proc.remaining_time, current_proc.remaining_quantum)

        for _ in range(exec_time):
            gantt.append((1, current_proc.pid))
            time += 1
            current_proc.remaining_time -= 1
            current_proc.remaining_quantum -= 1
            current_proc.allotment -= 1
            check_arrivals(time)
            if current_proc.remaining_time == 0:
                break

        if current_proc.remaining_time == 0:
            current_proc.completion_time = time
            current_proc.turnaround_time = time - current_proc.arrival_time
            completed += 1
        else:
            if current_proc.allotment <= 0 and current_level + 1 < len(queues_config):
                enqueue(current_proc, current_level + 1)
            elif tq and current_proc.remaining_quantum == 0:
                enqueue(current_proc, current_level)
            else:
                enqueue(current_proc, current_level)

    return merge_gantt(gantt)


def merge_gantt(gantt):
    if not gantt:
        return []

    merged = []
    prev_pid = gantt[0][1]
    dur = 0

    for time_unit in gantt:
        if time_unit[1] == prev_pid:
            dur += 1
        else:
            merged.append((dur, prev_pid))
            prev_pid = time_unit[1]
            dur = 1

    merged.append((dur, prev_pid))
    return merged
