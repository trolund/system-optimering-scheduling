from caseLoader import CaseLoader

def load():
    loader = CaseLoader()
    cases = loader.load_test_case()

    print("cases loaded:")
    for case in cases.keys():
        print(case)

    #for task in cases["inf_10_10"]:
    #    print(task.name)

if __name__ == '__main__':
    load()
