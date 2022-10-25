import unittest

def sumSomething(a,b):
    return a+b

class SATests(unittest.TestCase):
    
    def testFunction(self):
        result = sumSomething(1,2)
        self.assertEqual(result,3)


    
    #temperature lowers
    def tempLowers(self):
        return "Not implemented"
    


    #Saving best solution
    def saveBestSolution(self):
        return "Not implemented"

    #Saving best schedule
    def saveBestSchedule(self):
        return "Not implemented"
    

    #Saving best cost
    def saveBestCost(self):
        return "Not implemented"
    

    #saving best polling server config
    def saveBestPsConfig(self):
        return "Not implemented"
    
    




if __name__ == '__main__':
    unittest.main()