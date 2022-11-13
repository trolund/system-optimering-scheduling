#include "simple_genetic_algorithm.h"

// do simple genetic algorithm Rothlauf p. 148
void SimpleGeneticAlgorithm::perform_sga(int population_sz, int num_generations, double (*cost_f)(solution*)) {
    sg->set_population_sz(population_sz); // ugly
    std::vector<solution> population = sg->generate_population();



}

solution SimpleGeneticAlgorithm::get_best_solution() { return best_solution; }