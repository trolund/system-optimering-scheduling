#include "simulated_annealing.h"

/* 

    TODO:   algorithm 2!! done
            find some way to normalize wcrts based on priotity 

    should operate on list of <T> instead of vector bc we insert and stuff?

*/

uint64_t getTimeNow(){
 return std::chrono::duration_cast<std::chrono::seconds>
    (std::chrono::system_clock::now().time_since_epoch()).count();
}

template <class T>
std::vector<T> SimulatedAnnealer<T>::getBestSolution() { return this->bestSolution; };

template <class T>
double SimulatedAnnealer<T>::getBestCost() { return this->bestCost; };

template <class T>
int SimulatedAnnealer<T>::getNSolutions() { return this->nSolutions; };

// TODO: add some assert statement or handle overflow somehow
template <class T>
long double SimulatedAnnealer<T>::p(double delta, double t) { 
    double val = exp( -delta / t );
    assert(val < 1);
    //std::cout << "val is: " << val << " delta is: " << delta << " t is: " << t << std::endl;
    return val;
}

template <class T>
void SimulatedAnnealer<T>::performSimulatedAnnealing(std::vector<T> *s, long double t, long double a, int stopcriterion_sec, std::vector<T> (*neighborhood_f)(std::vector<T>), double (*cost_f)(std::vector<T>*)) { 
    double delta;
    this->nSolutions = 0;  
    std::vector<T> tmpSolution = *s;
    double tmpCost;
    //std::cout << "before calling cost " << std::endl;
    double cost = cost_f(s); 
    double bestCost = cost;

    std::cout << bestCost <<std::endl;

    uint64_t sec0 = getTimeNow(); 
    
    while (getTimeNow() - sec0 < stopcriterion_sec) { 
        tmpSolution = neighborhood_f(*s);
        tmpCost = cost_f(&tmpSolution);
        delta = tmpCost - cost;

        if(delta > 0) {
            std::cout << "p(delta, t) and t: " << p(delta, t) << " " <<  t << std::endl;
        }
        //std::cout << "tmpcost: " << tmpCost << "curcost: " << cost << std::endl;
        if ( delta <= 0 || p(delta, t) > this->unifRealDis(this->re) ) {
            *s = tmpSolution;
            cost = tmpCost;
            std::cout << cost << std::endl;
            if (cost < bestCost) {
                bestCost = cost;
                bestSolution = *s;
                
                //this->bestCost = cost;
                //std::cout << "new best cost: " << bestCost << std::endl;
            }
        } 
        
        t = t * a;

        this->nSolutions++; 
        
    }

    this->bestSolution = bestSolution;
    this->bestCost = bestCost;
    
}

//class Task;
//template class SimulatedAnnealer<City>;
template class SimulatedAnnealer<Task>;