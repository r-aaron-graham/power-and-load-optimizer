"""Greedy scheduler to optimize power consumption for compute tasks."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
import math
from typing import Dict, List, Tuple

import click


class Task:
    def __init__(self, task_id: str, duration_hours: float, deadline: str) -> None:
        if not math.isfinite(duration_hours) or duration_hours <= 0:
            raise ValueError("Task duration must be finite and positive")
        self.task_id = task_id
        self.duration = timedelta(hours=duration_hours)
        self.deadline = datetime.fromisoformat(deadline)

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, duration={self.duration}, deadline={self.deadline})"


def load_tasks(path: Path) -> List[Task]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    tasks = [Task(item["id"], item["duration_hours"], item["deadline"]) for item in data]
    # Sort tasks by deadline to schedule urgent tasks first
    tasks.sort(key=lambda t: t.deadline)
    return tasks


def load_prices(path: Path) -> List[Tuple[datetime, float, timedelta]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # Each entry: {"start": iso_datetime, "price": float, "duration_hours": float}
    prices = []
    for entry in data:
        start = datetime.fromisoformat(entry["start"])
        price = float(entry["price"])
        duration = timedelta(hours=float(entry.get("duration_hours", 1)))
        prices.append((start, price, duration))
    # Sort ascending by price
    prices.sort(key=lambda x: x[1])
    return prices


def schedule_tasks(tasks: List[Task], prices: List[Tuple[datetime, float, timedelta]]) -> Dict[str, Tuple[datetime, datetime]]:
    schedule: Dict[str, Tuple[datetime, datetime]] = {}
    for task in tasks:
        if task.task_id in schedule:
            raise ValueError(f"Duplicate task ID: {task.task_id}")
        scheduled = False
        for slot_start, price, slot_duration in prices:
            slot_end = slot_start + slot_duration
            candidate_start = slot_start
            for start, end in sorted(schedule.values()):
                if candidate_start + task.duration <= start:
                    break
                if candidate_start < end:
                    candidate_start = end
            candidate_end = candidate_start + task.duration
            if candidate_end <= min(slot_end, task.deadline):
                schedule[task.task_id] = (candidate_start, candidate_end)
                scheduled = True
                break
        if not scheduled:
            raise ValueError(f"Could not schedule task {task.task_id} before its deadline")
    return schedule


@click.command()
@click.option("--tasks", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True, help="JSON file of tasks.")
@click.option(
    "--prices", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True, help="JSON file of price slots."
)
@click.option(
    "--output", type=click.Path(dir_okay=False, path_type=Path), default="schedule.json", show_default=True, help="Output schedule file."
)
def main(tasks: Path, prices: Path, output: Path):
    tasks_list = load_tasks(tasks)
    prices_list = load_prices(prices)
    try:
        schedule = schedule_tasks(tasks_list, prices_list)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    # Serialize schedule to JSON
    result = []
    for task_id, (start, end) in schedule.items():
        result.append({"task_id": task_id, "start": start.isoformat(), "end": end.isoformat()})
    with output.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    click.echo(f"Wrote schedule for {len(schedule)} tasks to {output}")


if __name__ == "__main__":  # pragma: no cover
    main()