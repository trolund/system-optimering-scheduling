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
#include <climits>

#include "task.h"

// used to select what parameters to change in neighboorhood function
#define NUM_PS 0
#define BUDGET 1
#define PERIOD 2
#define DEADLINE 3
#define SUBSET 4
#define PARAMETERS 5 // number of parameters that can be changed 

class Neighborhood {
    private:
        std::default_random_engine re;
        std::uniform_int_distribution<> unif_dis_parameter;
        std::uniform_int_distribution<> unif_dis_change;  


    public:
        Neighborhood() {
            std::random_device rd;
            this->unif_dis_parameter = std::uniform_int_distribution<>(0,4);
            this->unif_dis_change = std::uniform_int_distribution<>(1,300);
            this->re = std::default_random_engine(rd());
        }

    std::vector<Task> getFromNeighborhood(std::vector<Task>);
    void changeNumPs(std::vector<Task>*, int);
    void changeBudget(Task*, int);
    void changePeriod(Task*, int);
    void changeDeadline(Task*, int);
    void changeSubset(Task*, int);
};