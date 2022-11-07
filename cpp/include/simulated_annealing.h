#include <vector>
#include <string>
#include <cmath>
#include <chrono>
#include <random> 
#include <cassert>
#include <numeric>
#include <map>
#include <list>
#include <tuple>

#include "city.h"

// would rather not have this and task here
#include "cost_functions.h"
//#include "task.h"


#include <iostream>

//used for neighborhood function

// cost functions and neighborhood function, implemented in cost_functions.cpp 
//std::tuple<std::vector<std::string>, int, bool> edf(std::vector<Task>);
//std::tuple<bool, std::map<std::string, int>> isPollingServerSchedulable(int budget, int period, int deadline, std::vector<Task> etSubset);
//std::list<Task> getReadyList(std::vector<Task>, std::list<Task>, int cycle);
//std::vector<Task> getFromNeighborhood();

// utility used in sa for stop criterion 
uint64_t getTimeNow();

template <class T>
class SimulatedAnnealer {
    private:
        std::vector<T> bestSolution;
        double bestCost;
        int nSolutions = 0; 

        //https://en.cppreference.com/w/cpp/numeric/random/uniform_real_distribution
        // for pseudorandom number generation
        std::default_random_engine re;
        std::uniform_real_distribution<double> unifRealDis;  

    public:
        SimulatedAnnealer() { 
            std::random_device rd;
            this->unifRealDis = std::uniform_real_distribution<double>(0.0, 1.0);
            //this->unifIntDis = std::uniform_int_distribution<>(0, 5); 
            this->re = std::default_random_engine(rd());
        }

        std::vector<T> getBestSolution();

        double getBestCost();

        int getNSolutions();

        long double p(double delta, double t);
        
        // neighbor random stuff find better solution...
        void performSimulatedAnnealing(std::vector<T>* s, long double t, long double a, int stopcriterion_sec, std::vector<T> (*neighborhood_f)(std::vector<T>), double (*cost_f)(std::vector<T>*));

        std::vector<T> get_best_thing();
};


