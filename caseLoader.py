import os
import sys
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
        # lots of assumptions about filename, fx always have this __.__ format
        # print(filename[-10:-9])
        # try:
        #     int(filename[-11:-10])
        #     two_digit = filename[-11:-10]
        # except:
        #     two_digit = ""
        # filename_id = two_digit + filename[-10:-9]
        filename_id = re.findall("__(.)__", filename)[-1]# assuming that the character (.) is in [0,2,3,4,5,6,7,8,9] and last occurence of pattern is what we use
     
        return filename_id

    def safe_lookup(self, a, i):
        try:
            return a[i]
        except:
            return None

    def load_test_case(self, test_case_name="", id: int = -1, filePath=""):
        # print(sys.path)
        try:
            print("Searching for test cases at:")
            file_path = filePath if len(filePath) > 0 else "test_cases\\"
            path = file_path + test_case_name if len(test_case_name) > 0 else file_path
            print(path)
            cases = {}

            if not os.path.exists(path):
                print(path + " does not exist.")
                raise Exception("Failed loading file using \\.")

            for root, dirs, files in os.walk(path):
                for fileName in files:
                    # print(root.split("\\"))
                    # print(root.split("\\")[-1])
                    case_name = root.split("\\")[-1]
                    path = os.path.join(root, fileName)
                    with open(path, "r") as file:
                        lines = file.readlines()
                        lines.pop(0)

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

                            # make sure the case array is initialized
                            case_group = cases.get(case_name)
                            if case_group is None:
                                cases[case_name] = {}

                            # add task to case
                            file_id = int(self.get_filename_id(fileName))

                            if cases.get(case_name).get(file_id) is None:
                                cases[case_name][file_id] = []

                            cases[case_name][file_id].append(task)

            print("Loaded " + str(len(cases)) + " test case(s).")

            if id != -1:
                print("Loaded case_group: " + str(test_case_name) + " - case: " + str(id) + " test case(s).")
                return cases[test_case_name][id]

            print("Loaded " + str(len(cases)) + " test case(s).")
        except Exception as e:
            print(e, "Trying with /.")
            print("Searching for test cases at:")
            file_path = filePath if len(filePath) > 0 else "test_cases/"
            path = file_path + test_case_name if len(test_case_name) > 0 else file_path
            print(path)
            cases = {}

            if not os.path.exists(path):
                print(path + " does not exist.")
                return

            for root, dirs, files in os.walk(path):
                for fileName in files:
                    # print(root.split("\\"))
                    # print(root.split("\\")[-1])
                    case_name = root.split("/")[-1]
                    path = os.path.join(root, fileName)
                    with open(path, "r") as file:
                        lines = file.readlines()
                        lines.pop(0)

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

                            # make sure the case array is initialized
                            case_group = cases.get(case_name)
                            if case_group is None:
                                cases[case_name] = {}

                            # add task to case
                            file_id = int(self.get_filename_id(fileName))

                            if cases.get(case_name).get(file_id) is None:
                                cases[case_name][file_id] = []

                            cases[case_name][file_id].append(task)

            print("Loaded " + str(len(cases)) + " test case(s).")

            if id != -1:
                print("Loaded case_group: " + str(test_case_name) + " - case: " + str(id) + " test case(s).")
                return cases[test_case_name][id]

            print("Loaded " + str(len(cases)) + " test case(s).")

        return cases
