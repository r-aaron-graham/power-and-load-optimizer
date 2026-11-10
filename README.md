# Power and load optimizer

A greedy scheduler that assigns compute tasks to price windows in ascending
price order. Each task has a unique ID, positive duration, and deadline.
Tasks share one worker and run entirely within one price window.

## Run the example

```bash
python -m pip install -r requirements.txt
python optimizer.py --tasks tasks.json --prices prices.json --output schedule.json
```

The bundled historical scenario produces three scheduled tasks in
`schedule.json`. The scheduler reuses the unoccupied part of a window and
checks the task's actual finish against its deadline.

The price metadata guides ordering. The model does not calculate energy
consumption, enforce grid power limits, or guarantee a globally optimal
schedule. Use consistent timestamp conventions across tasks and price slots.

## Verify

```bash
python -m pip install pytest
python -m pytest -q
```

The regression case fits two one-hour tasks before a two-hour deadline inside
one four-hour price window. Duplicate task IDs are rejected.
