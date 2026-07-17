"""
Shortest Remaining Time First (SRTF) CPU Scheduling — Preemptive SJF
At every time unit, the process with the smallest remaining burst is executed.
A newly arrived process preempts the current one if it has a shorter remaining time.
"""


def srtf_scheduling(processes):
    """
    processes: list of dicts -> {"pid": str, "arrival": int, "burst": int}
    returns same shape as fcfs_scheduling (gantt has one entry per contiguous run)
    """
    if not processes:
        return {"table": [], "gantt": [],
                "avg_waiting": 0, "avg_turnaround": 0,
                "avg_response": 0, "cpu_utilization": 0, "throughput": 0}

    procs = sorted([dict(p) for p in processes], key=lambda p: (p["arrival"], p["pid"]))
    n = len(procs)

    remaining = {p["pid"]: p["burst"] for p in procs}
    arrival   = {p["pid"]: p["arrival"] for p in procs}
    burst     = {p["pid"]: p["burst"] for p in procs}

    finish_time = {}
    first_start = {}   # for response time: first moment the process touches the CPU

    time = 0
    gantt = []          # list of {pid, start, end} for contiguous segments
    current_pid = None
    seg_start = 0

    # Run until every process has finished
    while len(finish_time) < n:
        # Collect processes that have arrived and still have remaining burst
        available = [p for p in procs
                     if p["arrival"] <= time and remaining[p["pid"]] > 0]

        if not available:
            # CPU is idle — jump to the next arrival
            if current_pid is not None:
                # flush any in-progress segment (shouldn't happen but guard it)
                if time > seg_start:
                    gantt.append({"pid": current_pid, "start": seg_start, "end": time})
                current_pid = None

            next_arrival = min(p["arrival"] for p in procs if remaining[p["pid"]] > 0)
            time = next_arrival
            continue

        # Pick the process with the shortest remaining time;
        # tie-break: earliest arrival, then lexicographic PID
        chosen = min(available,
                     key=lambda p: (remaining[p["pid"]], p["arrival"], p["pid"]))
        pid = chosen["pid"]

        # Record first start (response time anchor)
        if pid not in first_start:
            first_start[pid] = time

        # If the running process changes, flush the previous Gantt segment
        if pid != current_pid:
            if current_pid is not None and time > seg_start:
                gantt.append({"pid": current_pid, "start": seg_start, "end": time})
            current_pid = pid
            seg_start = time

        # Execute for exactly 1 time unit
        remaining[pid] -= 1
        time += 1

        # Check if the process just finished
        if remaining[pid] == 0:
            finish_time[pid] = time
            # Flush the completed segment
            gantt.append({"pid": pid, "start": seg_start, "end": time})
            current_pid = None
            seg_start = time

    # Build per-process result table (preserve original input order)
    completed = []
    for p in procs:
        pid = p["pid"]
        ft = finish_time[pid]
        arr = arrival[pid]
        b   = burst[pid]
        turnaround = ft - arr
        waiting    = turnaround - b
        response   = first_start[pid] - arr
        completed.append({
            "pid":        pid,
            "arrival":    arr,
            "burst":      b,
            "start":      first_start[pid],
            "finish":     ft,
            "waiting":    waiting,
            "turnaround": turnaround,
            "response":   response,
        })

    avg_wait       = sum(r["waiting"]    for r in completed) / n
    avg_turnaround = sum(r["turnaround"] for r in completed) / n
    avg_response   = sum(r["response"]   for r in completed) / n

    total_sim_time = max(r["finish"]  for r in completed) - min(r["arrival"] for r in completed)
    cpu_busy       = sum(r["burst"]   for r in completed)
    cpu_utilization = (cpu_busy / total_sim_time * 100) if total_sim_time > 0 else 0.0
    throughput      = n / max(r["finish"] for r in completed) if max(r["finish"] for r in completed) > 0 else 0.0

    return {
        "table":           completed,
        "gantt":           gantt,
        "avg_waiting":     avg_wait,
        "avg_turnaround":  avg_turnaround,
        "avg_response":    avg_response,
        "cpu_utilization": cpu_utilization,
        "throughput":      throughput,
    }
