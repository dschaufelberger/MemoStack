import math


class Task:
    def __init__(self, description):
        self.description = description
        self.is_completed = False

    def complete(self):
        self.is_completed = True


class Memo:
    def __init__(self, name, tasks=None):
        if tasks is None:
            tasks = []

        self.name = name
        self.__tasks = tasks

    def add_task(self, task):
        if task is not None and task not in self.__tasks:
            self.__tasks.append(task)

    def remove_task(self, task):
        if task in self.__tasks:
            self.__tasks.remove(task)

    def complete_task(self, task_id):
        if 0 < task_id <= len(self.__tasks):
            self.__tasks[task_id - 1].complete()
        else:
            raise InvalidTaskId(task_id)

    def list_id_task_tuples(self):
        tuples = []

        for index, task in enumerate(self.__tasks):
            tuples.append((index + 1, task))

        return tuples

    def _get_number_of_task(self):
        return len(self.__tasks)

    def get_task(self, task_id):
        if 0 < task_id <= len(self.__tasks):
            return self.__tasks[task_id - 1]
        else:
            return InvalidTaskId(task_id)

    def is_completed(self):
        for task in self.__tasks:
            if not task.is_completed:
                break
        else:
            return True

        return False

    def __str__(self):
        memo_formatter = MemoFormatter(self)
        return memo_formatter.format()


class MemoStack:
    def __init__(self):
        self.memos = []

    def push(self, memo):
        if memo is not None:
            self.memos.append(memo)

    def pop(self):
        memo = self.peek()

        if memo.is_completed():
            return self.memos.pop()
        else:
            raise MemoNotCompleted(memo)

    def peek(self):
        if not self.is_empty():
            return self.memos[len(self.memos) - 1]
        else:
            raise MemoStackIsEmpty()

    def is_empty(self):
        return len(self.memos) == 0


class MemoFormatter:
    __border = "**"
    __padding = "  "
    __id_marker = "[]"
    __reserved_space = len(__border) + len(__padding) + len(__id_marker)

    def __init__(self, memo):
        self.memo = memo
        self.__memo_width = max(len(memo.name) + self.__reserved_space, 25)
        self.__task_count = len(memo.list_id_task_tuples())

    def format(self):
        string_list = []
        decoration = "*" * self.__memo_width

        string_list.append(decoration)
        self.__append_memo_title(string_list)
        string_list.append(decoration)

        for task_tuple in self.memo.list_id_task_tuples():
            self.__append_task_tuple(task_tuple, string_list)

        string_list.append(decoration)

        return "\n".join(string_list)

    def __append_memo_title(self, string_list):
        text_template = "*{0}{1}{2}*"
        spaces = self.__memo_width - len(self.memo.name) - 2
        text_line = text_template.format(" " * math.floor(spaces / 2),
                                         self.memo.name,
                                         " " * math.ceil(spaces / 2))
        string_list.append(text_line)

    def __append_task_tuple(self, task_tuple, string_list):
        text_line_length = self.__compute_task_description_length()
        sliced_description = self.__slice_task_description(
            task_tuple[1].description, text_line_length
        )
        for index, sliced_text in enumerate(sliced_description):
            string_list.append(
                self.__prepare_text_line(task_tuple[0], sliced_text,
                                         index == 0))

    def __compute_task_description_length(self):
        return self.__memo_width - len(str(self.__task_count)) \
               - self.__reserved_space - 1

    @staticmethod
    def __slice_task_description(task_description, length):
        return [task_description[i:i + length] for i in
                range(0, len(task_description), length)]

    def __prepare_text_line(self, task_id, description_sub_string,
                            is_new_task):
        leading_spaces = self.__compute_leading_spaces(task_id, is_new_task)

        if is_new_task:
            prefix_length = len(leading_spaces) \
                            + len(str(task_id)) \
                            + len(self.__id_marker)
            trailing_spaces = self.__compute_trailing_spaces(
                prefix_length, len(description_sub_string))
            return "* {0}[{1}] {2}{3} *".format(
                leading_spaces, task_id, description_sub_string,
                trailing_spaces)
        else:
            trailing_spaces = self.__compute_trailing_spaces(
                len(leading_spaces), len(description_sub_string))
            return "* {0} {1}{2} *".format(
                leading_spaces, description_sub_string, trailing_spaces)

    def __compute_leading_spaces(self, task_id, is_new_task=False):
        space_count = len(str(self.__task_count))

        if is_new_task:
            space_count -= len(str(task_id))
        else:
            space_count += len(self.__id_marker)

        return " " * space_count

    def __compute_trailing_spaces(self, prefix_length, text_length):
        space_count = self.__memo_width \
                      - prefix_length \
                      - text_length \
                      - len(self.__padding) \
                      - len(self.__border) \
                      - 1
        return " " * space_count


class MemoConsole:
    __prompt = "PyMemo> "

    def __init__(self):
        self.__reset()

    def start(self):
        self.__reset()
        self.__run_input_loop()

    def quit(self):
        self.__is_running = False

    def __reset(self):
        self.__stack = MemoStack()
        self.__is_running = True

    def __run_input_loop(self):
        print("Started the PyMemo application.\n"
              "Type 'h' or 'help' to list all commands.")

        while self.__is_running:
            self.__receive_user_input()
        else:
            self.quit()

    def __receive_user_input(self):
        user_input = input(MemoConsole.__prompt).lower()

        if self.__input_matches_any(user_input, "q", "quit"):
            self.quit()
        elif self.__input_matches_any(user_input, "h", "help"):
            self.__print_help()
        elif self.__input_matches_any(user_input, "m", "memo"):
            self.__read_memo()
        elif self.__input_matches_any(user_input, "t", "task"):
            self.__read_task()
        elif self.__input_matches_any(user_input, "p", "print"):
            self.__print_memo_stack()
        elif user_input == "pop":
            self.__pop_memo()
        elif user_input.startswith("c") or user_input.startswith("complete"):
            task_id = self.__extract_task_id(user_input)
            self.__complete_task(task_id)
        else:
            self.__print_unknown_input()

    @staticmethod
    def __print_help():
        print("Available commands:\n"
              "\thelp (or h): Print this command list.\n"
              "\tquit (or q): Quit the application.\n"
              "\tprint (or p): Print the top memo if the stack is not empty\n"
              "\tmemo (or m): "
              "Creates a memo and puts it at the top of the stack\n"
              "\ttask (or t): Creates a new task for the top memo.\n"
              "\tcomplete (or c) <task id>: Completes the task with the "
              "given task id of the top memo, i.e. 'complete 1'.")

    def __complete_task(self, task_id):
        if task_id is None:
            return

        if self.__stack.is_empty():
            print("The memo stack is empty.")
        else:
            try:
                memo = self.__stack.peek()
                memo.complete_task(task_id)
            except InvalidTaskId:
                print("The task id you entered does not exist!\n"
                      "Please enter a valid task id. You'll find them next "
                      "to the task you want to complete.")

    def __pop_memo(self):
        if self.__stack.is_empty():
            print("The memo stack is empty.")
            return

        memo = self.__stack.peek()
        if memo.is_completed():
            memo = self.__stack.pop()
            print("Well done! You just finished the following memo. "
                  "Keep up the good work!")
            print(memo)
        else:
            print("You cannot remove this memo - it is not complete! "
                  "You must finish all tasks of the memo first.")

    def __print_memo_stack(self):
        if self.__stack.is_empty():
            print("The memo stack is empty.")
        else:
            memo = self.__stack.peek()
            print(memo)

    def __extract_task_id(self, user_input):
        command_and_id = str(user_input).split(" ")

        if len(command_and_id) != 2:
            self.__print_unknown_input()
            return

        if command_and_id[0] == "c" or command_and_id[0] == "complete":
            try:
                task_id = int(command_and_id[1])
                return task_id
            except ValueError:
                print("The task id you entered is no number!\n"
                      "Please pick the task you want to finish and enter "
                      "'complete' followed by the task id displayed next "
                      "to the task you want to finish, i.e. 'complete 1'.")
        else:
            self.__print_unknown_input()

    def __read_task(self):
        if self.__stack.is_empty():
            print("The memo stack is empty! Please create a memo first.")
        else:
            task_description = input(
                "{0}Please enter a new task description: ".format(
                    MemoConsole.__prompt))

            memo = self.__stack.peek()
            task = Task(task_description)
            memo.add_task(task)

    def __read_memo(self):
        memo_name = input("{0}Please enter the new memo\'s name: ".format(
            MemoConsole.__prompt))

        memo = Memo(memo_name)
        self.__stack.push(memo)
        print(
            "Your memo \"{0}\" was created successfully. ".format(memo_name),
            "You may now add tasks to it.")

    @staticmethod
    def __input_matches_any(user_input, *allowed_values):
        return user_input in allowed_values

    @staticmethod
    def __print_unknown_input():
        print("We're sorry. But the command you entered is unknown.")


class MemoNotCompleted(Exception):
    def __init__(self, memo):
        self.memo = memo

    def __str__(self):
        return "Oops! The memo '{0}' is not completed," \
               " and therefore cannot be removed!".format(self.memo.name)


class MemoStackIsEmpty(Exception):
    def __str__(self):
        return "The memo stack is empty!"


class InvalidTaskId(Exception):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "There is no task with id '{0}'.".format(self.index)


if __name__ == '__main__':
    console = MemoConsole()
    console.start()
