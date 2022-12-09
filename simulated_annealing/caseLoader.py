import os
import re

# print(sys.path)
# rel_path = os.path.join(os.path.dirname(__file__), "") # if we use just "..", the path will be based on cwd (which is my download/ folder but might also be anything else)
# abs_path = os.path.abspath(rel_path)
# sys.path.insert(1, abs_path)
# print(sys.path)
from task import Task
from taskType import TaskType


class CaseLoader:

    def get_filename_id(self, filename):
        # lots of assumptions about filename, fx always have this __.__ or __..__ format
        filename_id = re.findall("__(.?.?)__", filename)[
            -1]  # assuming that the character (.) is in [0,2,3,4,5,6,7,8,9] and last occurence of pattern is what we use

        return filename_id

    def safe_lookup(self, a, i):
        try:
            return a[i]
        except:
            return None

    def load_test_case(self, path):
        print("Searching for test case at:")

        cwd = os.getcwd()
        print(cwd)

        with open(path, "r") as file:
            lines = file.readlines()
            lines.pop(0)

            case = []

            for line in lines:
                # map line to a object
                values = line.split(";")
                event_type = TaskType.TIME if values[4] == "TT" else TaskType.EVENT
                if len(values) == 7:
                    task = Task(str(values[1]), int(values[2]), int(values[3]), event_type, int(values[5]),
                                int(values[6]), None, 0)
                elif len(values) == 8:
                    task = Task(str(values[1]), int(values[2]), int(values[3]), event_type, int(values[5]),
                                int(values[6]), None, int(values[7]))

                case.append(task)

        return case
