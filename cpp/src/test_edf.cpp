#include "cost_functions.h"
//#include "task.h"
#include <iostream>

int main() {
    Task tt0 = Task("tTT0", 2, 5, TT, 7, 5, 0);
    Task tt1 = Task("tTT1", 4, 7, TT, 7, 7, 0);
    std::vector<Task> *task_set = new std::vector<Task>;
    task_set->push_back(tt0);
    task_set->push_back(tt1); 

    std::vector<std::string> reference_schedule = {"tTT0", "tTT0", "tTT1", "tTT1", "tTT1", "tTT1", "tTT0", 
            "tTT0", "tTT1", "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", 
            "tTT0", "tTT0", "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", 
            "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", "tTT1", "tTT1", 
            "tTT1", "tTT0", "tTT0", "IDLE"};

    std::tuple<bool, std::map<std::string, double>, std::vector<std::string>> thing;

    thing = edf(task_set);
    
    bool is_schedulable = std::get<0>(thing);
    assert(is_schedulable); 
    std::cout << is_schedulable << std::endl;
    
    std::vector<std::string> schedule = std::get<2>(thing);
    
    assert(reference_schedule.size() == schedule.size());
    bool equals;
    for(int i = 0; i < schedule.size(); i = i + 1) {
        if(reference_schedule.at(i).compare(schedule.at(i)) == 0) { equals = true; } 
        else { equals=false;break; }
    }

    assert(equals);
    delete(task_set);  
    tt0 = Task("tTT0", 2, 3, TT, 7, 3, 0); 
    tt1 = Task("tTT1", 2, 4, TT, 7, 4, 0);
    task_set = new std::vector<Task>;
    task_set->push_back(tt0);
    task_set->push_back(tt1); 


    thing = edf(task_set);
    is_schedulable = std::get<0>(thing);
    assert(!is_schedulable); 
    std::cout << is_schedulable << std::endl; 

    std::cout << "all good passed tests" << std::endl;
    
}