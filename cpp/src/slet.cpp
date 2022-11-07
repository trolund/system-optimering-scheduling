/*
constexpr auto lcm(auto x, auto y) {
    return std::lcm(x,y);
}

constexpr auto lcm(auto head, auto...tail) {
    return std::lcm(head, lcm(tail...));
}
*/

/*
// release jobs 
std::list<Task> getReadyList(std::vector<Task> taskSet, std::list<Task> readyList, int cycle) {
    
    for(auto task : taskSet) {
        if (cycle % task.deadline == 0) {
            readyList.push_back(Task(task.name, task.duration, task.period, task.type, task.priority, task.deadline + cycle, cycle));

        }
    }

    // sort on deadline
    readyList.sort();

    return readyList;
}

//https://www.wolframalpha.com/input?i=lcm%28a%2Cb%2Cc%29+%3D%3D+lcm%28lcm%28a%2Cb%29%2C+c%29
//https://en.cppreference.com/w/cpp/numeric/lcm 
std::tuple<std::vector<std::string>, int, bool> edf(std::vector<Task> taskSet) {
    int hyperperiod = std::lcm(std::lcm(2000, 3000), 4000);
    std::vector<std::string> schedule;
    std::list<Task> readyList; // (taskSet.begin(), taskSet.end()); 
    std::map<std::string, int> wcrts;

    std::cout << "Hyperperiod: " << hyperperiod << std::endl; 
    std::cout << &taskSet << " " << &readyList << std::endl; 
    
    for(int t = 0; t < hyperperiod; t = t + 1) {
        readyList = getReadyList(taskSet, readyList, t);

        // iterate like this to erase while iterating 
        for (auto it = readyList.begin(); it != readyList.end();) {

            // return and indicate not feasible if some job is not done but exceeded deadline 
            if (it->duration > 0 && it->deadline <= t) {
                
                
                // accumulate worst case response times 
                //https://stackoverflow.com/questions/31354947/adding-all-values-of-map-using-stdaccumulate 
                int wcrtsSum = std::accumulate(wcrts.begin(), wcrts.end(), 0, 
                    [] (int value, const std::map<std::string, int>::value_type& p)
                    { return value + p.second; });

                return std::tuple<std::vector<std::string>, int, bool>(schedule, wcrtsSum, false);
            }

            if(it->duration == 0 && it->deadline >= t) {
                int responseTime = t - it->releaseTime;

                if (!wcrts.contains(it->name) || responseTime > wcrts[it->name]) {
                    wcrts[it->name] = responseTime;   
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
        int wcrtsSum = std::accumulate(wcrts.begin(), wcrts.end(), 0, 
            [] (int value, const std::map<std::string, int>::value_type& p)
            { return value + p.second; });
        
        return std::tuple<std::vector<std::string>, int, bool>(schedule, wcrtsSum, false);
    }
    
    int wcrtsSum = std::accumulate(wcrts.begin(), wcrts.end(), 0, 
            [] (int value, const std::map<std::string, int>::value_type& p)
            { return value + p.second; });
    

    return std::tuple<std::vector<std::string>, int, bool>(schedule, wcrtsSum, true);
 
}

// determine if some polling server with a given budget, period, deadline and set of et tasks is schedulable
std::tuple<bool, std::map<std::string, int>> isPollingServerSchedulable(int budget, int period, int deadline, std::vector<Task> etSet) {
    int delta = period + deadline - 2*budget;
    double alpha = budget / period;
    double supply, demand, curResponseTime; // do not really understand why responseTime is interesting when it is just overwritten each iteration
    std::map<std::string, int> responseTimes;
    // should response time be a list or map as in other??

    int hyperperiod = etSet[0].period;

    // https://stackoverflow.com/questions/4210470/looping-on-c-iterators-starting-with-second-or-nth-item
    for(auto it = std::next(etSet.begin()); it != etSet.end(); ++it) {
        hyperperiod = std::lcm(hyperperiod, it->period);
    }

    std::cout << "hyperperiod for ets is: " << hyperperiod << std::endl;

    for(auto et_it : etSet) {

        // initialize response time of current et task to a value exceeding its deadline
        curResponseTime = et_it.deadline + 1;
        
        for(int t = 0; t <= hyperperiod; t = t + 1) {
            supply = alpha * (t - delta);
            demand = 0;

            for(auto et_it_j : etSet) {

                // compute maximum demand at time t
                if (et_it_j.priority >= et_it.priority) { 
                    demand = demand + std::ceil(t / et_it_j.period) * et_it_j.duration;
                }
            } // end of traversal of other ets

            if (supply >= demand) {
                std::cout << "current et is: " << et_it.name << " t is: " << t << std::endl;
                curResponseTime = t;
                responseTimes[et_it.name] = curResponseTime;
                break; 
            }
        } // end of inner for

        if (curResponseTime >= et_it.deadline) {
            return std::tuple<bool, std::map<std::string, int>>(false, responseTimes);
        }    

    } // end of outer for

    return std::tuple<bool, std::map<std::string, int>>(true, responseTimes);

}
*/