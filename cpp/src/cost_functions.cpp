#include "cost_functions.h"
#include <iostream>

/*

    TODO rand thing ....

*/


double costFunction(std::vector<Task> *taskSet) {
    std::list<Task> polling_servers; 
    std::map<std::string, int> wcrts_tt;
    std::tuple<bool, std::map<std::string, int>> is_schedulable_cost = is_schedulable_cost;
    double cost_tt = 0, cost_et = 0, cost = 0;
    bool is_schedulable;

    for (auto it : *taskSet) { 
        if (it.et_subset != NULL) { polling_servers.push_back(it); };        
    }

    for(auto it : polling_servers) {
        is_schedulable_cost = isPollingServerSchedulable(&it);
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

// release jobs 
void getReadyList(std::vector<Task> *taskSet, std::list<Task> *readyList, int cycle) {
    
    for(auto task : *taskSet) {
        if (cycle % task.deadline == 0) {
            readyList->push_back(Task(task.name, task.duration, task.period, task.type, task.priority, task.deadline + cycle, cycle));

        }
    }

    // sort on deadline
    readyList->sort();
    // do not sort and get min element how bout dat !!! linear time instead of whatever sorting is 
    //return readyList;
}

//https://www.wolframalpha.com/input?i=lcm%28a%2Cb%2Cc%29+%3D%3D+lcm%28lcm%28a%2Cb%29%2C+c%29
//https://en.cppreference.com/w/cpp/numeric/lcm
//https://www.geeksforgeeks.org/lcm-of-given-array-elements/ 
//std::tuple<std::vector<std::string>, int, bool> 
std::map<std::string, int> edf(std::vector<Task> *taskSet) { 
    int hyperperiod = taskSet->front().period;//.period;
    // https://stackoverflow.com/questions/4210470/looping-on-c-iterators-starting-with-second-or-nth-item
    
    for(auto it = std::next(taskSet->begin()); it != taskSet->end(); ++it) {
        hyperperiod = std::lcm(hyperperiod, it->period);
    }

    //std::cout << "hyperperiod is: " << hyperperiod << std::endl;
    
    std::vector<std::string> schedule;
    std::list<Task> readyList; // (taskSet.begin(), taskSet.end()); 
    std::map<std::string, int> wcrts;

    //std::cout << "Hyperperiod: " << hyperperiod << std::endl; 
    //std::cout << &taskSet << " " << &readyList << std::endl; 
    
    for(int t = 0; t < hyperperiod; t = t + 1) {
        getReadyList(taskSet, &readyList, t);

        // iterate like this to erase while iterating 
        for (auto it = readyList.begin(); it != readyList.end();) {

            // return and indicate not feasible if some job is not done but exceeded deadline 
            if (it->duration > 0 && it->deadline <= t) {
                
                wcrts["NO"] = -1;
                return wcrts;
                
            }

            if(it->duration == 0 && it->deadline >= t) {
                int responseTime = t - it->releaseTime;

                if (!wcrts.contains(it->name) || responseTime > wcrts[it->name]) {
                    wcrts[it->name] = responseTime;
                    //std::cout << "HELLO: " << responseTime << std::endl; 
                }

                // erase returns iterator pointing to element that followed erased item
                it = readyList.erase(it);
            } else {
                ++it;
            }
        }

        if (readyList.size() == 0) {
            schedule.push_back("IDLE");
            continue;
        } else {
            schedule.push_back(readyList.front().name);
            readyList.front().duration -= 1; 
        }
    }

    if (readyList.size() > 0) {         
        wcrts["false"] = -1;
        return wcrts;
        
       
    }  
    return wcrts;

 
}

// determine if some polling server with a given budget, period, deadline and set of et tasks is schedulable
std::tuple<bool, std::map<std::string, double>> isPollingServerSchedulable(Task* polling_server) {
    
    int budget = polling_server->duration;
    int period = polling_server->period;
    int deadline = polling_server->deadline;
    std::vector<Task>* et_set = polling_server->et_subset;  

    int delta = period + deadline - 2*budget;
    double alpha = double(budget) / double(period);
    double supply, demand, curResponseTime; 
    std::map<std::string, double> responseTimes;
    

    int hyperperiod = et_set->front().period;
    
    // https://stackoverflow.com/questions/4210470/looping-on-c-iterators-starting-with-second-or-nth-item
    for(auto it = std::next(et_set->begin()); it != et_set->end(); ++it) {
        hyperperiod = std::lcm(hyperperiod, it->period);
    }


    for(auto et_it : *et_set) {
        // initialize response time of current et task to a value exceeding its deadline
        curResponseTime = et_it.deadline + 1;
        
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
                curResponseTime = t;
                responseTimes[et_it.name] = curResponseTime; 
                break; 
            }
        } // end of inner for

        if (curResponseTime >= et_it.deadline) { 
            return std::tuple<bool, std::map<std::string, double>>(false, responseTimes);
        }    

    } // end of outer for

    return std::tuple<bool, std::map<std::string, double>>(true, responseTimes);

}
