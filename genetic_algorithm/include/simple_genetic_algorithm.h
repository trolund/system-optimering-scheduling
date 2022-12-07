#include <vector>
#include <chrono>
#include <omp.h>
#include "solution_generator.h"

class SimpleGeneticAlgorithm {
    private:
        SolutionGenerator *sg;
        solution best_solution; 
        double crossover_rate;
        double mutation_rate;
        std::random_device dev; 
        std::mt19937 rng;
        std::vector<double> avg_costs;
        int gen_best_solution = 0;
        std::string test_case;

    public:
        SimpleGeneticAlgorithm(SolutionGenerator *sg, double crossover_rate, double mutation_rate, std::string test_case) : sg(sg), crossover_rate(crossover_rate), mutation_rate(mutation_rate) , test_case(test_case) { rng = std::mt19937(dev()); };  
        void perform_sga(int population_sz, int num_generations, std::tuple<double,bool> (*cost_f)(std::vector<Task>*));
        solution get_best_solution();
        void apply_cost_function(solution*, double (*cost_f)(std::vector<Task>*));
        void apply_cost_function1(solution*, std::tuple<double,bool> (*cost_f)(std::vector<Task>*));
        solution get_min_cost(std::vector<solution> *solutions);
        void fill_mating_pool(std::vector<solution*>& mating_pool, std::vector<solution>* population);
        double avg_cost_population(std::vector<solution>);
        void print_run_summary(double);
};