#include "solution_generator.h"

SolutionGenerator::SolutionGenerator(std::vector<Task> *task_set, int population_size) {
        population_sz = population_size;
        rng = std::mt19937(dev()); // https://stackoverflow.com/questions/686353/random-float-number-generation 
        uni_dist = std::uniform_int_distribution<std::mt19937::result_type>(1, 20);
        uni_real_dist = std::uniform_real_distribution<>(0, 1); // random double in [0, 1)
        uni_dist_select = std::uniform_int_distribution<std::mt19937::result_type>(0, population_sz - 1);
        
        for (auto it : *task_set) {
            if (it.type == TT) { tt_tasks.push_back(it); } 
            else { et_tasks.push_back(it); } 
        }

        separate_et_tasks();

    }

void SolutionGenerator::set_population_sz(int sz) {
    population_sz = sz;
    uni_dist_select = uni_dist_select = std::uniform_int_distribution<std::mt19937::result_type>(0, population_sz - 1);
}

void SolutionGenerator::separate_et_tasks(){
    std::set<int> separation_set;
    
    for (auto it : et_tasks) {
        if(!separation_map.contains(it.separation)) {
            std::vector<Task> *et_separated = new std::vector<Task>(); // we would like to only instantiate these tasks once keep on heap. wont work if 0s that we swap around present though... 
            et_separated->push_back(it);
            separation_map.insert({it.separation, et_separated});
        } else { 
            separation_map.at(it.separation)->push_back(it);
        }
    } 
}

// generate a solution
solution SolutionGenerator::generate_solution() {
    std::vector<Task> polling_servers; 
    int duration;
    int period;
    int deadline;
    std::string name; // naming not that important, but we give one for debugging purposes
     
    for(auto it : separation_map) {
        //duration = uni_dist(rng);
        period = uni_dist(rng) * 10;
        //deadline = ((uni_dist(rng) * 10) % period) + duration;
        deadline = ((uni_dist(rng) * 10) % period);
        duration = uni_dist(rng);
        duration = std::min(duration, deadline);
        //deadline = (uni_dist(rng) * 10);
        while(deadline > period) { deadline = uni_dist(rng) * 10; }; // deadlines may not be greater than period. if so create instance t_i+1 before t_i has finished possibly  
        Task polling_server =  Task(name, duration, period, TT, 7, deadline, it.second);
        polling_servers.push_back(Task(name, duration, period, TT, 7, deadline, it.second));
    }

    return (solution) {.polling_servers = polling_servers, .tt_tasks = &this->tt_tasks, .cost = 0.0};
}

// generate a population of size sz
std::vector<solution> SolutionGenerator::generate_population() {
    std::vector<solution> population;
    for(int i = 0; i < population_sz; i = i + 1) {
        population.push_back(generate_solution());
    }

    return population;
}

// https://en.cppreference.com/w/cpp/algorithm/swap
// use the fact that switch statements 'fall through' without a break in case 2 and 1
// no need for default case so far...
void swap(solution& lhs, solution& rhs, int crossover_point) {
    std::cout << "crossover point: " << crossover_point << std::endl;
    switch(crossover_point) {
        case 2:
            std::swap(lhs.polling_servers[0].deadline, rhs.polling_servers[0].deadline); 
            std::swap(lhs.polling_servers[1].deadline, rhs.polling_servers[1].deadline);
            std::swap(lhs.polling_servers[2].deadline, rhs.polling_servers[2].deadline);
        case 1:
            std::swap(lhs.polling_servers[0].period, rhs.polling_servers[0].period);  
            std::swap(lhs.polling_servers[1].period, rhs.polling_servers[1].period); 
            std::swap(lhs.polling_servers[2].period, rhs.polling_servers[2].period);  
        case 0:
            std::swap(lhs.polling_servers[0].duration, rhs.polling_servers[0].duration); 
            std::swap(lhs.polling_servers[1].duration, rhs.polling_servers[1].duration);
            std::swap(lhs.polling_servers[2].duration, rhs.polling_servers[2].duration);
            break;  
    }

}

/* 
 * generate two child solutions from two parent solutions if random() <= p crossover else children = parents
 * crossover_point = n means 'line' between index n and n+1 
 * four parameter to change: duration, period, deadline, et_subset
 * represented as three possibilities for crossover point: 0, 1, 2
 *  
 * TODO: multiple crossover points
 *
 */
std::vector<solution> SolutionGenerator::recombine(solution* solution1, solution* solution2, double pc) {
    std::vector<solution> offspring = {*solution1, *solution2};
    if (uni_real_dist(rng) <= pc) {
        // shuffle polling servers? try. change ordering of vector. but offspring might be too dissimilar from parents then  
        std::shuffle(std::begin(offspring[0].polling_servers), std::end(offspring[0].polling_servers), rng); 
        std::shuffle(std::begin(offspring[1].polling_servers), std::end(offspring[1].polling_servers), rng); 
        int crossover_point = uni_dist(rng) % 3;
        swap(offspring[0], offspring[1], crossover_point); 
    } 
 
    return offspring; 
} 

// perform tournament. compete n times. return best. with replacement 
solution SolutionGenerator::select(std::vector<solution>* population, int k) {
    // we do not need rand here bc we shuffle no wait
    int selection_i = uni_dist_select(rng); 
    int selection_j;
    //std::cout << "sel i: " << selection_i << std::endl;
    
    for(int i = 0; i < k; i = i + 1) {
    
        selection_j = uni_dist_select(rng);
        //std::cout << "sel j: " << selection_j << std::endl;
        // do not let solutions compete against themselves in this round
        while (selection_i == selection_j) { selection_j = uni_dist_select(rng); } 

        // update if better use compare function instead
        if (population->at(selection_j).cost < population->at(selection_i).cost) {
            selection_i = selection_j;
        } 
    }
 
    return population->at(selection_i);

}

// perform tournament. compete n times. return best. with replacement 
solution* SolutionGenerator::select_(std::vector<solution>* population, int k) {
    // we do not need rand here bc we shuffle no wait
    int selection_i = uni_dist_select(rng); 
    int selection_j;
    //std::cout << "sel i: " << selection_i << std::endl;
    
    for(int i = 0; i < k; i = i + 1) {
    
        selection_j = uni_dist_select(rng);
        //std::cout << "sel j: " << selection_j << std::endl;
        // do not let solutions compete against themselves in this round
        while (selection_i == selection_j) { selection_j = uni_dist_select(rng); } 

        // update if better use compare function instead
        if (population->at(selection_j).cost < population->at(selection_i).cost) {
            selection_i = selection_j;
        } 
    }
 
    return &population->at(selection_i);

}

// mutate solution
// a bit of freestyle. we go through each possible mutate. we could also check once for each parameter and apply 
// mutation to parameter in each polling server. for each parameter.
void SolutionGenerator::mutate(solution* sol, double mutation_rate) {
    int sign;
    for (int i = 0; i < sol->polling_servers.size(); i = i + 1) {
        
        if(uni_real_dist(rng) <= mutation_rate) {
            sign = (uni_dist(rng) % 2 == 0) ? 1 : -1;
            sol->polling_servers[i].duration += sign;
        }
        if(uni_real_dist(rng) <= mutation_rate) {
            sign = (uni_dist(rng) % 2 == 0) ? 1 : -1;
            sol->polling_servers[i].period += sign * uni_dist(rng); // add/sub a value in [1, 20]
        }
        if(uni_real_dist(rng) <= mutation_rate) {
            sign = (uni_dist(rng) % 2 == 0) ? 1 : -1;
            sol->polling_servers[i].deadline += sign * uni_dist(rng);
            sol->polling_servers[i].deadline = std::min(sol->polling_servers[i].deadline, sol->polling_servers[i].period);
        }
    }

}

// get solution with minimum cost from a vector of solutions
solution SolutionGenerator::get_min_cost(std::vector<solution> *solutions) {
    std::vector<solution>::iterator result = std::min_element(solutions->begin(), solutions->end(), cmp_solution());
    return *result;
}
//void check_separation(solution*); // check that separation requirement is met 
//void check_param_sol(solution*); // check that parameters are ok deadline <= period etc. 