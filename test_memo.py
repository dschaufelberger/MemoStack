from unittest import TestCase
from PyMemo import Memo
from PyMemo import Task
from PyMemo import InvalidTaskId


class TestMemo(TestCase):
    def setUp(self):
        self.memo = Memo("Test Memo")

    def tearDown(self):
        del self.memo
     
    def test_fail():
        self.fail()
    
    def test_add_new_task(self):
        task = Task("Test Task")

        memo_count_before = len(self.memo.__tasks)
        self.memo.add_task(task)
        memo_count_after = len(self.memo.__tasks)

        self.assertEqual(memo_count_after, memo_count_before + 1)

    def test_add_existing_task(self):
        task = Task("Test Task")
        self.memo.add_task(task)

        memo_count_before = len(self.memo.__tasks)
        self.memo.add_task(task)
        memo_count_after = len(self.memo.__tasks)

        self.assertEqual(memo_count_after, memo_count_before)

    def test_add_none_should_not_change_the_task_list(self):
        memo_count_before = len(self.memo.__tasks)
        self.memo.add_task(None)
        memo_count_after = len(self.memo.__tasks)

        self.assertEqual(memo_count_after, memo_count_before)

    def test_is_completed_with_single_open_task(self):
        tasks = []
        for task_count in range(1, 6):
            task = Task("Completed Test Task" + str(task_count))
            task.complete()
            tasks.append(task)

        uncompleted_task = Task("Uncompleted Test Task")
        uncompleted_task.is_completed = False
        tasks.append(uncompleted_task)

        self.memo = Memo("Test Memo", tasks)

        self.assertFalse(self.memo.is_completed())

    def test_is_completed_with_multiple_open_tasks(self):
        tasks = []
        for task_count in range(1, 6):
            uncompleted_task = Task("Uncompleted Test Task" + str(task_count))
            tasks.append(uncompleted_task)

        completed_task = Task("Completed Test Task")
        completed_task.complete()
        tasks.append(completed_task)

        self.memo = Memo("Test Memo", tasks)

        self.assertFalse(self.memo.is_completed())

    def test_is_completed_with_all_tasks_completed(self):
        tasks = []
        for task_count in range(1, 6):
            completed_task = Task("Completed Test Task" + str(task_count))
            completed_task.complete()
            tasks.append(completed_task)

        self.memo = Memo("Test Memo", tasks)

        self.assertTrue(self.memo.is_completed())

    def test_is_completed_with_empty_task_list(self):
        self.assertTrue(self.memo.is_completed())

    def test_remove_existing_task(self):
        task = Task("Test Task")

        self.memo = Memo("Test Memo", [task])

        task_count_before = len(self.memo.__tasks)
        self.memo.remove_task(task)
        task_count_after = len(self.memo.__tasks)

        self.assertEqual(task_count_after, task_count_before - 1)

    def test_remove_non_existing_task(self):
        task = Task("Test Task")

        task_count_before = len(self.memo.__tasks)
        self.memo.remove_task(task)
        task_count_after = len(self.memo.__tasks)

        self.assertEqual(task_count_after, task_count_before)

    def test_complete_single_task_and_ensure_it_is_completed(self):
        tasks = []

        for task_count in range(1, 6):
            task = Task("Uncompleted Test Task" + str(task_count))
            tasks.append(task)

        self.memo = Memo("Test Memo", tasks)

        task_is_completed_before = self.memo.get_task(4).is_completed
        self.memo.complete_task(4)
        task_is_completed_after = self.memo.get_task(4).is_completed

        self.assertNotEqual(task_is_completed_after, task_is_completed_before)
        self.assertTrue(task_is_completed_after)

    def test_complete_single_task_and_ensure_it_is_the_only_completed(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 5, "Test Task")
        self.memo.complete_task(4)

        for task_tuple in self.memo.list_id_task_tuples():
            if task_tuple[0] != 4 and task_tuple[1].is_completed:
                self.fail()

    def test_complete_single_task_with_invalid_positive_id(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 5, "Test Task")

        with self.assertRaises(InvalidTaskId):
            self.memo.complete_task(100)

    def test_complete_single_task_with_empty_memo(self):
        with self.assertRaises(InvalidTaskId):
            self.memo.complete_task(1)

    def test_list_task_tuples(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")
        task_tuples = self.memo.list_id_task_tuples()

        self.assertEqual(10, len(task_tuples))

    def test_list_task_tuples_with_empty_memo(self):
        task_tuples = self.memo.list_id_task_tuples()

        self.assertEqual(0, len(task_tuples))

    def test_get_task_by_id(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")

        task_seven = self.memo.get_task(7)

        self.assertEqual("Test Task 7", task_seven.description)

    def test_get_task_by_lowest_id(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")

        task_seven = self.memo.get_task(1)

        self.assertEqual("Test Task 1", task_seven.description)

    def test_get_task_by_highest_id(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")

        task_seven = self.memo.get_task(10)

        self.assertEqual("Test Task 10", task_seven.description)

    def test_get_task_by_id_out_of_lower_bounds(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")

        with self.assertRaises(InvalidTaskId):
            self.memo.get_task(0)

    def test_get_task_by_id_out_of_higher_bounds(self):
        self.memo = TestMemo.prepare_memo_with_tasks("Test Memo", 10, "Test Task")

        with self.assertRaises(InvalidTaskId):
            self.memo.get_task(11)

    @staticmethod
    def prepare_memo_with_tasks(memo_label, number_of_tasks, task_label,
                                complete_tasks=False):
        tasks = []

        for task_count in range(1, number_of_tasks + 1):
            task = Task(task_label + " " + str(task_count))

            if complete_tasks:
                task.complete()

            tasks.append(task)

        return Memo(memo_label, tasks)
