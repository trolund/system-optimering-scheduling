#include "simple_genetic_algorithm.h"

// do simple genetic algorithm Rothlauf p. 148
void SimpleGeneticAlgorithm::perform_sga(int population_sz, int num_generations, double (*cost_f)(std::vector<Task>*)) {
    sg->set_population_sz(population_sz); // ugly
    std::vector<solution> population = sg->generate_population(); // generate initial population
    std::vector<solution> new_population; // we could have just cleard pop and filled again. but would rather have mating pool as ptrs and keep old pop and then reassign
    std::vector<solution> offspring;
    std::vector<solution*> mating_pool; // consider whether we should use ptrs to solution
    solution candidate_best;
    int chunk_sz = population_sz / 8;
    uint64_t sec0 = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count();
 
    #pragma omp parallel for num_threads(8)
    for(int i = 0; i < population_sz; i = i + 1) {
        apply_cost_function(&population[i], cost_f);
        std::cout << "solution " << i << " cost: " << population[i].cost << std::endl;
    }

    best_solution = get_min_cost(&population); // we could find in loop above but... one time cost below we have to do it separately...  
    std::cout << "best cost is: " << best_solution.cost << std::endl;
    
    // main loop 
    for(int gen = 0; gen <  num_generations; gen = gen + 1) {
        mating_pool.clear();
        
        fill_mating_pool(mating_pool, &population); 
        std::shuffle(mating_pool.begin(), mating_pool.end(), rng); // should already be shuffled bc random selection but do it anyway 
        
        new_population.clear();
        
        for (int i = 0; i < population_sz; i = i + 2) {
            offspring = sg->recombine(mating_pool[i], mating_pool[i+1], crossover_rate);
            sg->mutate(&offspring[0], mutation_rate); // perform mutation now instead of in loop afterwards
            sg->mutate(&offspring[1], mutation_rate); 
            new_population.insert(new_population.end(), offspring.begin(), offspring.end()); 
        }
        std::cout << "size of new population: " << new_population.size() << std::endl; 
        
        population = new_population;
        
        // update population. parallelize. guided or static. some overhead with guided.. but if population size is large it might be good
        #pragma omp parallel for num_threads(8) schedule(guided) 
        for(int i = 0; i < population_sz; i = i + 1) {
            apply_cost_function(&population[i], cost_f);
            std::cout << "solution " << i << " cost: " << population[i].cost << std::endl;
        }

        candidate_best = get_min_cost(&population);
        best_solution = candidate_best.cost < best_solution.cost ? candidate_best : best_solution;

        std::cout << "generation is: " << gen << " best solution cost is: "  << best_solution.cost << std::endl;

    }

    uint64_t sec_end = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    std::cout << "ran for: " << sec_end - sec0 << " seconds" << std::endl;
}

solution SimpleGeneticAlgorithm::get_best_solution() { return best_solution; }

// apply cost function to a solution and store cost in solution. find a way where we do not have to instantiate a vector
void SimpleGeneticAlgorithm::apply_cost_function(solution* s, double (*cost_f)(std::vector<Task>*)) { 
        std::vector<Task> task_set = *s->tt_tasks;
        task_set.insert(task_set.end(), s->polling_servers.begin(), s->polling_servers.end());
        double cost = cost_function(&task_set);
        s->cost = cost; 
}

// get solution with minimum cost from a vector of solutions
solution SimpleGeneticAlgorithm::get_min_cost(std::vector<solution> *solutions) {
    std::vector<solution>::iterator result = std::min_element(solutions->begin(), solutions->end(), cmp_solution());
    return *result;
}

// fill mating pool. mating pool should be empty when calling
void SimpleGeneticAlgorithm::fill_mating_pool(std::vector<solution*>& mating_pool, std::vector<solution>* population) {
    int population_sz = population->size();
    for(int i = 0; i < population_sz; i= i + 1) {
        mating_pool.push_back(sg->select_(population, 3));
    }
}

