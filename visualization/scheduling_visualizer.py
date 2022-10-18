import random
import matplotlib.pyplot as plt
from sortedcontainers import SortedSet
from caseLoader import CaseLoader
from sa_scheduling.cost_functions import edf
from taskType import TaskType


def get_bounds(solution):
    curr_task = ""
    start_point = -1
    end_point = -1
    bounds = []
    max_end = 0

    for idx, x in enumerate(solution):
        if x != curr_task:
            prev_task = curr_task
            curr_task = x

            if start_point == -1:
                start_point = idx
            elif end_point == -1:
                end_point = idx
            else:
                time = end_point - start_point
                bounds.append((prev_task, (start_point, end_point), time))

                if end_point > max_end:
                    max_end = end_point

                start_point = -1
                end_point = -1

    return [c for c in bounds if c[0] != "IDLE"], max_end


class SchedulingVisualizer:
    """Returns a list of boundaries of each task execution and 'biggest' x cor"""

    def draw_plot(self, sol, name="plot", grid=False):
        servers = SortedSet([c for c in sol if c.__contains__("TT")])
        data, max_end = get_bounds(sol)

        # print(len(servers), data, max_end)

        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, len(servers))

        # Setting X-axis limits
        gnt.set_xlim(0, max_end)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Ticks since start')
        gnt.set_ylabel('Polling servers')

        # Setting ticks on y-axis
        def y_ticks(servers):
            list = []
            dic = {}

            for idx, x in enumerate(s):
                placement = (idx + 1) * 70
                list.append(placement)
                dic[x] = placement

            return list, dic

        y, dic = y_ticks(servers)

        gnt.set_yticks(y)
        # Labelling tickes of y-axis
        gnt.set_yticklabels(servers)

        # Setting graph attribute
        gnt.grid(grid)

        height_of_jobs = 70

        # iterate servers
        for sol in servers:
            exeutions = [c for c in data if c[0] == sol]
            to_print = []
            for e in exeutions:
                job_dif = (e[1][0], e[2])
                to_print.append(job_dif)

            gnt.broken_barh(to_print, (dic[sol] - height_of_jobs, height_of_jobs),
                            facecolors=(random.uniform(0, 1), random.uniform(0, 1), 0.5))

        # Declaring a bar in schedule
        # gnt.broken_barh([(80, 1500)], (dic["tTT26"] - 20, height_of_jobs), facecolors =('tab:orange'))

        # Declaring multiple bars in at same level and same width
        # gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
        #                         facecolors ='tab:blue')

        # gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
        #                                  facecolors =('tab:red'))

        plt.savefig(f"{name}.png")


if __name__ == '__main__':
    loader = CaseLoader()
    cases = loader.load_test_case("inf_30_30", 0, filePath="../test_cases/")
    cases = [c for c in cases if c.type == TaskType.TIME]
    s, wcrts = edf(cases)

    viz = SchedulingVisualizer()

    viz.draw_plot(s, "first")

