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
    

    





if __name__ == '__main__':
    unittest.main()