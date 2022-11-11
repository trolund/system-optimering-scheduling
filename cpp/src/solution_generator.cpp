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
    for (auto it : this->et_tasks) {
        if(!separation_map.contains(it.separation)) {
            separation_map[it.separation] = std::vector<Task> {it};
        } else {
            separation_map[it.separation].push_back(it);
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
        name = "ttPS" + std::to_string(it.first);
        std::vector<Task> et_subset;
        et_subset = it.second;
        Task polling_server =  Task(name, duration, period, TT, 7, deadline, &et_subset);
        polling_servers.push_back(polling_server);
    }

    return (solution) {.polling_servers = polling_servers, .tt_tasks = &this->tt_tasks, .cost = 0.0};
}