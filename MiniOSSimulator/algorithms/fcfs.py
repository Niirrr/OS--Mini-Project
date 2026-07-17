"""
First Come First Serve (FCFS) CPU Scheduling
Non-preemptive. Processes run strictly in order of arrival time.
"""


def fcfs_scheduling(processes):
    """
    processes: list of dicts -> {"pid": str, "arrival": int, "burst": int}
    returns: list of dicts with scheduling results + gantt chart segments
             gantt segment: {"pid": str, "start": int, "end": int}
    """
    procs = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))
    time = 0
    result = []
    gantt = []

    for p in procs:
        start = max(time, p["arrival"])
        finish = start + p["burst"]
        waiting = start - p["arrival"]
        turnaround = finish - p["arrival"]

        response = start - p["arrival"]
        result.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response,
        })
        gantt.append({"pid": p["pid"], "start": start, "end": finish})
        time = finish

    n = len(result)
    avg_wait = sum(r["waiting"] for r in result) / n
    avg_turnaround = sum(r["turnaround"] for r in result) / n
    avg_response = sum(r["response"] for r in result) / n

    total_sim_time = max(r["finish"] for r in result) - min(r["arrival"] for r in result)
    cpu_busy = sum(r["burst"] for r in result)
    cpu_utilization = (cpu_busy / total_sim_time * 100) if total_sim_time > 0 else 0.0
    throughput = n / max(r["finish"] for r in result) if max(r["finish"] for r in result) > 0 else 0.0

    return {"table": result, "gantt": gantt,
            "avg_waiting": avg_wait, "avg_turnaround": avg_turnaround,
            "avg_response": avg_response, "cpu_utilization": cpu_utilization,
            "throughput": throughput}
