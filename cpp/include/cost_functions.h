#include <vector>
#include <string>
#include <cmath>
#include <chrono>
#include <random> 
#include <cassert>
#include <numeric>
#include <map>
#include <list>
#include <tuple>
#include <climits>

#include "task.h"

std::tuple<bool, std::map<std::string, double>, std::vector<std::string>> edf(std::vector<Task>*); 
void get_ready_list(std::vector<Task>*, std::list<Task>*, int cycle);
int processor_demand(int t2, std::vector<Task>* periodic_tasks);
std::tuple<bool, std::map<std::string, double>> is_polling_server_schedulable(Task*);
double cost_function(std::vector<Task>*);

