import os
import shutil
import sys

from task import Task

class CaseLoader:

    def loadAllTestCases(self):
        print("Searching for test cases at:")
        path = "./test cases"
        print(path)
        tasks = []

        for root, dirs, files in os.walk(path):
            for fileName in files:
                path = os.path.join(root, fileName)
                file = open(path, "r")
                lines = file.readlines()
                for line in lines:
                    values = line.split(";")
                    task = Task(values[1], values[2], values[3], values[4], values[5], values[6])
                    tasks.append(task)

        print("Loaded " + str(len(tasks)) + " test cases.")

        return tasks
