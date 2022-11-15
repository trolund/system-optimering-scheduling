import unittest

from sa_scheduling import simulated_annealer


def sumSomething(a,b):
    return a+b

class SATests(unittest.TestCase):
    
    def testFunction(self):
        result = sumSomething(1,2)
        self.assertEqual(result,3)



    #temperature reduced correct amount
    def testTempExact(self):
        self.assertEqual(simulated_annealer.SimulatedAnnealer.update_temp(self, 1000, 0.5), 500)

    #temperature lowers
    def testTempLowers(self):
        temps = [1, 10, 100, 50, 35.5, 594.4, 0.01, 10000]
        alphas = [0.1, 0.99, 0.999, 0.5, 0.2, 0.001, 0.02, 0.99995]
        for temp in temps:
            for alpha in alphas:
                self.assertLess(simulated_annealer.SimulatedAnnealer.update_temp(self, temp, alpha), temp)
            self.assertGreater(simulated_annealer.SimulatedAnnealer.update_temp(self, temp, 1.01), temp)
            self.assertEqual(simulated_annealer.SimulatedAnnealer.update_temp(self, temp, 1.0), temp)
    


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