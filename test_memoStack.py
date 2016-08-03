from unittest import TestCase

from PyMemo import MemoStack
from PyMemo import MemoNotCompleted
from PyMemo import Memo
from PyMemo import MemoStackIsEmpty
from PyMemo import Task


class TestMemoStack(TestCase):
    def setUp(self):
        self.memo_stack = MemoStack()

    def test_push_on_empty_stack(self):
        memo = Memo("Test Memo")

        stack_count_before = len(self.memo_stack.memos)
        self.memo_stack.push(memo)
        stack_count_after = len(self.memo_stack.memos)

        self.assertEqual(stack_count_after, 1)
        self.assertEqual(stack_count_after, stack_count_before + 1)

    def test_push_on_non_empty_stack(self):
        for memo_count in range(1, 6):
            memo = Memo("Existing Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        memo = Memo("New Test Memo")

        stack_count_before = len(self.memo_stack.memos)
        self.memo_stack.push(memo)
        stack_count_after = len(self.memo_stack.memos)

        self.assertEqual(stack_count_after, stack_count_before + 1)

    def test_pop_from_empty_stack(self):
        with self.assertRaises(MemoStackIsEmpty):
            self.memo_stack.pop()

    def test_pop_results_in_decreased_size(self):
        for memo_count in range(1, 5):
            memo = Memo("Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        top_memo = Memo("Top Test Memo")
        self.memo_stack.push(top_memo)

        memo_count_before = len(self.memo_stack.memos)
        popped_memo = self.memo_stack.pop()
        memo_count_after = len(self.memo_stack.memos)

        self.assertEqual(memo_count_after, memo_count_before - 1)

    def test_pop_returns_top_memo(self):
        for memo_count in range(1, 5):
            memo = Memo("Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        top_memo = Memo("Top Test Memo")
        self.memo_stack.push(top_memo)

        popped_memo = self.memo_stack.pop()

        self.assertIs(top_memo, popped_memo)

    def test_pop_with_the_top_memo_not_completed(self):
        for memo_count in range(1, 5):
            memo = Memo("Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        top_memo = Memo("Top Test Memo")
        top_memo.add_task(Task("Incomplete Task"))
        self.memo_stack.push(top_memo)

        with self.assertRaises(MemoNotCompleted):
            popped_memo = self.memo_stack.pop()

    def test_peek_from_empty_stack(self):
        with self.assertRaises(MemoStackIsEmpty):
            self.memo_stack.peek()

    def test_peek_does_not_change_stack_size(self):
        for memo_count in range(1, 5):
            memo = Memo("Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        top_memo = Memo("Top Test Memo")
        self.memo_stack.push(top_memo)

        memo_count_before = len(self.memo_stack.memos)
        peeked_memo = self.memo_stack.peek()
        memo_count_after = len(self.memo_stack.memos)

        self.assertEqual(memo_count_after, memo_count_before)

    def test_peek_returns_top_memo(self):
        for memo_count in range(1, 5):
            memo = Memo("Test Memo" + str(memo_count))
            self.memo_stack.push(memo)

        top_memo = Memo("Top Test Memo")
        self.memo_stack.push(top_memo)

        peeked_memo = self.memo_stack.peek()

        self.assertIs(top_memo, peeked_memo)

    def test_is_empty_on_non_empty_stack(self):
        memo = Memo("Test Memo")

        self.memo_stack.push(memo)

        self.assertFalse(self.memo_stack.is_empty())

    def test_is_empty_on_empty_stack(self):
        self.assertTrue(self.memo_stack.is_empty())
