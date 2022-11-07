#include "neighborhood.h"

// should only accept polling servers or extract these from TT ? for instance by checking if et subset is not empty
// rn we GO THROUGH task set and mark polling servers. all this to keep sa class separate from task
// which is like why is that even a goal?
// consider changing all vectors to lists because we want to change them often
// also consider changing int to just store the pointers  
std::vector<Task> Neighborhood::getFromNeighborhood(std::vector<Task> taskSet) {
   std::vector<int> polling_servers;

   // get indexes of polling servers.....
   for(int i = 0; i < taskSet.size(); i = i + 1) {
    if(taskSet[i].et_subset != NULL) { polling_servers.push_back(i); }
   }

   int parameter = this->unif_dis_parameter(this->re);
   int target = polling_servers[this->unif_dis_change(this->re) % polling_servers.size()];
   int sign = this->unif_dis_change(this->re) % 2 == 0 ? 1 : -1; // fine to use the rng for changing parameters here i guess

   switch (parameter)
   {
   case NUM_PS:
    changeBudget(&taskSet[target], sign); 
    break;
   
   case BUDGET:
    changeBudget(&taskSet[target], sign);
    break;  
   
   case PERIOD:
    changePeriod(&taskSet[target], sign);
    break;  
   
   case DEADLINE:
    changeDeadline(&taskSet[target], sign);
    break;  
   
   case SUBSET:
    changeDeadline(&taskSet[target], sign);
    break;  
    
   default:
    break;
   }
   
   return taskSet; 
}

void Neighborhood::changeNumPs(std::vector<Task>*, int sign) {
   return; 
};

void Neighborhood::changeBudget(Task* target, int sign) {
    target->duration = std::max(1, target->duration + sign);
    target->duration = std::min(target->duration, target->deadline);
}

void Neighborhood::changePeriod(Task* target, int sign) {
    target->period = std::max(1, target->period + sign*5);
    target->period = std::max(target->deadline, target->period);
}
void Neighborhood::changeDeadline(Task* target, int sign) {
    target->deadline = std::max(1, target->deadline + sign*5);
    target->deadline = std::min(target->deadline, target->period);
}
void Neighborhood::changeSubset(Task* target, int sign) {
    
}