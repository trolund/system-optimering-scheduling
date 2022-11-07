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

std::map<std::string, int> edf(std::vector<Task>*);
std::tuple<bool, std::map<std::string, double>> isPollingServerSchedulable(Task*);
double costFunction(std::vector<Task>*);
void getReadyList(std::vector<Task>*, std::list<Task>*, int cycle);
