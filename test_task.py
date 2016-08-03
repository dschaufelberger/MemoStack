from unittest import TestCase
from PyMemo import Task


class TestTask(TestCase):

    def setUp(self):
        self.task = Task("Test Task")

    def tearDown(self):
        del self.task

    def test_complete_open_task(self):
        is_done_before = self.task.is_completed
        self.task.complete()

        self.assertTrue(self.task.is_completed)
        self.assertNotEqual(is_done_before, self.task.is_completed)

    def test_complete_completed_task(self):
        self.task.is_completed = True
        self.task.complete()

        self.assertTrue(self.task.is_completed)
