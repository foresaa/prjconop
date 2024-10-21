# tests/test_optimization.py

import unittest
from apps.optimization import optimize_schedule

class TestOptimization(unittest.TestCase):

    def test_optimize_schedule(self):
        # Example task input
        tasks = [
            {'ID': 1, 'Duration': '5', 'Predecessors': ''},
            {'ID': 2, 'Duration': '3', 'Predecessors': '1'},
            {'ID': 3, 'Duration': '2', 'Predecessors': '2'}
        ]

        result = optimize_schedule(tasks)

        # Assert result is not None and contains optimized start/finish times
        self.assertIsNotNone(result)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)

if __name__ == "__main__":
    unittest.main()
