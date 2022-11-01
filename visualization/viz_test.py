from shared.caseLoader import CaseLoader
from shared.cost_functions import edf
from shared.models.taskType import TaskType
from visualization.scheduling_visualizer import SchedulingVisualizer


def do():
    loader = CaseLoader()
    cases = loader.load_test_case("inf_30_30", 0, filePath="../test_cases/")
    cases = [c for c in cases if c.type == TaskType.TIME]
    s, wcrts = edf(cases)

    viz = SchedulingVisualizer()

    viz.draw_plot(s, "first")



if __name__ == '__main__':
    do()