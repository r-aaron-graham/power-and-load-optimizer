from datetime import datetime, timedelta
import unittest
from optimizer import Task, schedule_tasks

class SchedulerTests(unittest.TestCase):
    def test_partial_slot_and_remaining_capacity(self):
        start = datetime.fromisoformat("2026-04-01T00:00:00")
        tasks = [Task("a", 1, "2026-04-01T02:00:00"), Task("b", 1, "2026-04-01T02:00:00")]
        schedule = schedule_tasks(tasks, [(start, 0.1, timedelta(hours=4))])
        self.assertEqual(schedule["a"], (start, start + timedelta(hours=1)))
        self.assertEqual(schedule["b"], (start + timedelta(hours=1), start + timedelta(hours=2)))

    def test_duplicate_ids_are_rejected(self):
        start = datetime.fromisoformat("2026-04-01T00:00:00")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            schedule_tasks([Task("a", 1, "2026-04-01T04:00:00")] * 2,
                           [(start, 0.1, timedelta(hours=4))])
