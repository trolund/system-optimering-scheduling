#include <vector>
#include "solution_generator.h"

class SimpleGeneticAlgorithm {
    private:
        SolutionGenerator *sg;
        solution best_solution; 
        double crossover_rate;
        double mutation_rate;

    public:
        SimpleGeneticAlgorithm(SolutionGenerator *sg, double crossover_rate, double mutation_rate) : sg(sg), crossover_rate(crossover_rate), mutation_rate(mutation_rate) {}; 

        void perform_sga(int population_sz, int num_generations, double (*cost_f)(solution*));
        solution get_best_solution();

};