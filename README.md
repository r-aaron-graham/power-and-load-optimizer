# Power and Load Optimizer

This repository contains a simple scheduler that assigns compute tasks
to time slots based on grid power constraints and dynamic pricing.
The goal is to minimize electricity costs while ensuring tasks are
completed before their deadlines.  The optimizer uses a greedy
algorithm to schedule tasks during low‑cost periods.

## Task Model

Each task is defined by a unique ID, duration (in hours), and
deadline (timestamp).  The scheduler receives a forecast of power
prices over a planning horizon and produces a schedule mapping tasks
to time intervals.

## Usage

Install dependencies and run the optimizer on a JSON file of tasks:

```bash
pip install -r requirements.txt
python optimizer.py --tasks tasks.json --prices prices.json
```

The script will output a schedule.json describing when each task
should run.

## Extending

Enhance the scheduler by implementing more sophisticated algorithms
(e.g., dynamic programming, linear programming), adding support for
task priority, preemption, or heterogeneous compute resources.