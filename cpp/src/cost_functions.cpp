#include "cost_functions.h"
#include <iostream>

/*

    TODO rand thing ....

*/

/*
double cost_function(std::vector<Task> *taskSet) {
    std::list<Task> polling_servers; 
    std::map<std::string, int> wcrts_tt;
    std::tuple<bool, std::map<std::string, int>> is_schedulable_cost = is_schedulable_cost;
    double cost_tt = 0, cost_et = 0, cost = 0;
    bool is_schedulable;

    for (auto it : *taskSet) { 
        if (it.et_subset != NULL) { polling_servers.push_back(it); };        
    }

    for(auto it : polling_servers) {
        is_schedulable_cost = is_polling_server_schedulable(&it);
        double wcrts_et_sum = 0;
        
        if ( std::get<0>(is_schedulable_cost) ) {
            std::map<std::string, int> wcrts = std::get<1>(is_schedulable_cost);
            for (auto it : polling_servers) {
                for(int i = 0; i < it.et_subset->size(); i = i + 1) {// it.et_subset) { 
                    
                    wcrts_et_sum += double(wcrts[it.et_subset->at(i).name]); 
                    } 
                } 
        } else {
            cost_et = double(1);
            is_schedulable = false; 
        } 
    }

    wcrts_tt = edf(taskSet);
    
    if (wcrts_tt.contains("NO")) {
        cost_tt = double(1);
        //std::cout << " helllllooo" << std::endl;
        is_schedulable = false;
    } else {
        for (auto it : *taskSet) { 
            cost_tt +=  double(wcrts_tt[it.name]) / double(it.deadline); 
        }
        cost_tt *= 1/double(taskSet->size());
    }

    //std::cout << "NORMAL: " << cost_tt / taskSet->size() << std::endl;

    cost_et *= 1.0  / double(polling_servers.size());
    cost = cost_tt + cost_et;
    std::cout << "cost function cost is: " << cost << " et: " << cost_et << " tt: " << cost_tt << std::endl;
    return cost; 
}

*/

// release jobs 
void get_ready_list(std::vector<Task> *taskSet, std::list<Task> *readyList, int cycle) {  
    for(auto task : *taskSet) {
        if (cycle % task.period == 0) {
            // release new instance of task with deadline = Di + t and release time = t
            readyList->push_back(Task(task.name, task.duration, task.period, task.type, task.priority, task.deadline + cycle, cycle));
        }
    }    
}

/* deadline used here is relative deadline. section 4.6 hard real time 
   only for t1 = 0 not general case. also assumes that Di <= Ti
*/
int processor_demand(int t2, std::vector<Task> *periodic_tasks) {
    int n = periodic_tasks->size(); 
    int processor_demand=0; 
    double eta_i, period_i, deadline_i;

    // demand for some task is number of times scheduled * duration
    for(int i=0; i<n; i=i+1) {
        period_i = (double) periodic_tasks->at(i).period;
        deadline_i = (double) periodic_tasks->at(i).deadline; // line would be really long if we did this in line below
        eta_i = (t2 + period_i - deadline_i) /  period_i; // we could do without 2nd term but more general here

        processor_demand +=  ((int) eta_i) * periodic_tasks->at(i).duration;
    }

    return processor_demand;
}

//https://www.wolframalpha.com/input?i=lcm%28a%2Cb%2Cc%29+%3D%3D+lcm%28lcm%28a%2Cb%29%2C+c%29
//https://en.cppreference.com/w/cpp/numeric/lcm
//https://www.geeksforgeeks.org/lcm-of-given-array-elements/ 
std::tuple<bool, std::map<std::string, double>, std::vector<std::string>> edf(std::vector<Task> *tt_tasks) { 
    int hyperperiod = tt_tasks->front().period;
    
    // https://stackoverflow.com/questions/4210470/looping-on-c-iterators-starting-with-second-or-nth-item 
    for(auto it = std::next(tt_tasks->begin()); it != tt_tasks->end(); ++it) {
        hyperperiod = std::lcm(hyperperiod, it->period);
    }
    
    //std::cout << "hyperperiod is: " << hyperperiod << std::endl;
    std::map<std::string, double> wcrts;
    std::vector<std::string> schedule;

    if (processor_demand(hyperperiod, tt_tasks) > hyperperiod) {
        return std::tuple(false, wcrts, schedule);
    }  

    std::list<Task> ready_list; 
    int t = 0;

    // TODO: skip if none ready
    while (t < hyperperiod) {
        
        // check for deadline miss
        for (auto job : ready_list) {
            if (job.duration > 0 and job.deadline <= t) {
                return std::tuple(false, wcrts, schedule); 
            }
        }

        // release new task instances 
        get_ready_list(tt_tasks, &ready_list, t);

        // execute task instance with earliest deadline, if there are any ready tasks
        if (ready_list.size() == 0) {
            schedule.push_back("IDLE"); // no tasks instantiated, nothing to do 
        } else {

            // get task instance with earliest deadline https://stackoverflow.com/questions/26766136/how-to-get-min-or-max-element-in-a-vector-of-objects-in-c-based-on-some-field 
            auto ed_task = std::min_element(ready_list.begin(), ready_list.end(), Task::ByDeadline());  
            schedule.push_back(ed_task->name);
            ed_task->duration -= 1;

            // check if current response time larger than than current maximum
            if (ed_task->duration == 0 && ed_task->deadline >= t) {
                ready_list.erase(ed_task); // remove from ready list 
                if (!wcrts.contains(ed_task->name) || t - ed_task->release_time >= wcrts[ed_task->name]) {
                    wcrts[ed_task->name] = t - ed_task->release_time;
                }
            } else if(ed_task->duration == 0 && ed_task->deadline < t) { // this check should be redundant but to be safe. should be caught above if this is the case 
                return std::tuple(false, wcrts, schedule);  
            }
        }

        t = t + 1;
    }

    return std::tuple(true, wcrts, schedule); 
}

// determine if some polling server with a given budget, period, deadline and set of et tasks is schedulable
std::tuple<bool, std::map<std::string, double>> is_polling_server_schedulable(Task* polling_server) {
    
    int budget = polling_server->duration;
    int period = polling_server->period;
    int deadline = polling_server->deadline;
    std::vector<Task>* et_set = polling_server->et_subset;  

    int delta = period + deadline - 2*budget;
    double alpha = double(budget) / double(period);
    double supply, demand, cur_response_time; 
    std::map<std::string, double> response_times;
    

    int hyperperiod = et_set->front().period;
    
    // https://stackoverflow.com/questions/4210470/looping-on-c-iterators-starting-with-second-or-nth-item
    for(auto it = std::next(et_set->begin()); it != et_set->end(); ++it) {
        hyperperiod = std::lcm(hyperperiod, it->period);
    }


    for(auto et_it : *et_set) {
        // initialize response time of current et task to a value exceeding its deadline
        cur_response_time = et_it.deadline + 1;
        
        for(int t = 0; t <= hyperperiod; t = t + 1) {
            supply = alpha * (double(t) - double(delta));
            demand = 0;

            for(auto et_it_j : *et_set) {

                // compute maximum demand at time t
                if (et_it_j.priority >= et_it.priority) { 
                    demand = demand + std::ceil(double(t) / double(et_it_j.period)) * double( et_it_j.duration);
                }
            } // end of traversal of other ets

            if (supply >= demand) { 
                cur_response_time = t;
                response_times[et_it.name] = cur_response_time; 
                break; 
            }
        } // end of inner for

        if (cur_response_time >= et_it.deadline) { 
            return std::tuple<bool, std::map<std::string, double>>(false, response_times);
        }    

    } // end of outer for

    return std::tuple<bool, std::map<std::string, double>>(true, response_times);

}
