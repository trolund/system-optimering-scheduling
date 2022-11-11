#include "solution_generator.h"

SolutionGenerator::SolutionGenerator(std::vector<Task> *task_set) {
        this->rng = std::mt19937(dev()); 
        this->uni_dist = std::uniform_int_distribution<std::mt19937::result_type>(1, 50);
        
        for (auto it : *task_set) {
            if (it.type == TT) { tt_tasks.push_back(it); } 
            else { et_tasks.push_back(it); } 
        }

        separate_et_tasks();

    }

void SolutionGenerator::separate_et_tasks(){
    std::set<int> separation_set;
    
    for (auto it : this->et_tasks) {
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
        duration = uni_dist(rng);
        period = uni_dist(rng) * 10;
        deadline = uni_dist(rng) * 10;
        while(deadline > period) { deadline = uni_dist(rng) * 10; }; // deadlines may not be greater than period. if so create instance t_i+1 before t_i has finished possibly  
        Task polling_server =  Task(name, duration, period, TT, 7, deadline, it.second);
        polling_servers.push_back(Task(name, duration, period, TT, 7, deadline, it.second));
    }

    return (solution) {.polling_servers = polling_servers, .tt_tasks = &this->tt_tasks, .cost = 0.0};
}

// generate a population of size sz
std::vector<solution> SolutionGenerator::generate_population(int sz) {
    std::vector<solution> population;
    for(int i = 0; i < sz; i = i + 1) {
        population.push_back(generate_solution());
    }

    return population;
}