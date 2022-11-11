#include <vector>
#include <random> 
#include <map>
#include "task.h"

typedef struct solution {
    std::vector<Task> polling_servers;
    std::vector<Task> *tt_tasks;
    double cost;
} solution;

/*
    Solution is vector of polling servers and pointer to vector of tt tasks also store cost in this struct

    solution generate_solution()
    vector<solution> generate_population(int size)

*/

class SolutionGenerator {
    private:
        std::random_device dev; 
        std::mt19937 rng;
        std::uniform_int_distribution<std::mt19937::result_type> uni_dist; // uniform distribution in range [1, 6] 
        std::vector<Task> tt_tasks;
        std::vector<Task> et_tasks;
        std::map<int, std::vector<Task>> separation_map;
    
    public:
        SolutionGenerator(std::vector<Task>*); 

        void separate_et_tasks();
        solution generate_solution();
        std::vector<solution> generate_population(); 
};