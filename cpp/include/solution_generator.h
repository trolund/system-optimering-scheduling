#include <vector>
#include <random> 
#include "task.h"

typedef struct solution {
    std::vector<std::vector<Task>> *polling_servers;
    std::vector<Task> *tt_tasks;
    double cost;
} solution;


// we need one random number generator for period and deadline and one for duration or just use mod
class SolutionGenerator {
    private:
        std::random_device dev; 
        std::mt19937 rng;
        std::uniform_int_distribution<std::mt19937::result_type> uni_dist; // uniform distribution in range [1, 6] 

    public:
        SolutionGenerator() {
            this-> rng = std::mt19937(dev()); 
            this->uni_dist = std::uniform_int_distribution<std::mt19937::result_type>(1, 20);
        }

        solution generate_solution(); 
};