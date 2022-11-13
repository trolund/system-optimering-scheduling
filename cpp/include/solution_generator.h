#include <vector>
#include <random> 
#include <map>
#include <set>
#include <iostream>
#include <algorithm> 
#include "cost_functions.h" // includes kind of messy....

typedef struct solution {
    std::vector<Task> polling_servers;
    std::vector<Task> *tt_tasks;
    double cost; // store cost in solution to make selection easier
} solution;

// cost of solution a < cost of solution b ? https://stackoverflow.com/questions/34248336/min-value-and-index-from-elements-of-array-of-structure-in-c 
struct cmp_solution {
  bool operator()(const solution& a, const solution& b) const {
    return a.cost < b.cost;
  }
};

/*  For generating initial solution. Recombiner recombines and creates subsquent generations. 
    Solution is vector of polling servers and pointer to vector of tt tasks also store cost in this struct

    solution generate_solution()
    vector<solution> generate_population(int size)

*/

class SolutionGenerator {
    private:
        std::random_device dev; 
        std::mt19937 rng;
        std::uniform_int_distribution<std::mt19937::result_type> uni_dist; // uniform distribution in range [n, m] 
        std::uniform_real_distribution<> uni_real_dist; 
        std::uniform_int_distribution<std::mt19937::result_type> uni_dist_select; // uniform distribution in range [n, m] used for tournament selecting solutions 
        std::vector<Task> tt_tasks;
        std::vector<Task> et_tasks;
        int population_sz; 
        // these two do the same thing but trying to make things work here
        std::map<int, std::vector<Task>*> separation_map; 

    public:
        SolutionGenerator(std::vector<Task>*, int); 
        void separate_et_tasks(); // separate et tasks based on the separation field. store in map
        solution generate_solution(); // generate a random solution
        std::vector<solution> generate_population(); // generate sz random solutions
        std::vector<solution> recombine(solution*, solution*, double); // generate two child solutions from two parent solutions      
        solution select(std::vector<solution>*, int); // perform tournament. compete n times. return best. with replacement 
        void mutate(solution*, double); // mutate solution
        void check_separation(solution*); // check that separation requirement is met 
        void check_param_sol(solution*); // check that parameters are ok deadline <= period etc. 
        void set_population_sz(int sz); // convenient
        solution get_min_cost(std::vector<solution>*);  
 
        friend void swap(solution& lhs, solution& rhs, int crossover_point); // swap parameters to generate offspring. couldnt make it work with references.
};