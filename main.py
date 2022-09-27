from caseLoader import CaseLoader

def load():
    loader = CaseLoader()
    cases = loader.load_test_case("inf_30_30", 1)

    print("cases loaded:")

    for t in cases:
        print(t.name, t.deadline)
    #for case in cases.keys():
    #    print(case)

    #for task in cases["inf_10_10"]:
    #    print(task.name)

if __name__ == '__main__':
    load()
