from caseLoader import CaseLoader

def load():
    loader = CaseLoader()
    cases = loader.loadAllTestCases()

    print("cases loaded:")
    for case in cases.keys():
        print(case)

    #for task in cases["inf_10_10"]:
    #    print(task.name)

if __name__ == '__main__':
    load()
