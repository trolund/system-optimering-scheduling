#include "csv_reader.h"
#include "simulated_annealing.h"
//#include "cost_functions.h"


void usage(char* s) {
    printf("<%s> <temperature> <cooling factor> <seconds to run sa>\n", s);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        usage(argv[0]);
        exit(0);
    }    
    
    srand(time(NULL));

    CSVReader csvReader = CSVReader("../test_cases/inf_70_10/taskset__1643188594-a_0.7-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__99__tsk.csv");
    
    //CSVReader csvReader = CSVReader("../../sa_tsp/cities.csv");
    SimulatedAnnealer<Task> sa; 
    std::vector<Task> taskSetAll, taskSetTT;//, taskSetET; 
    std::vector<Task>* taskSetET = new std::vector<Task>;
    std::vector<City> cities;
    long double temperature = std::stold(argv[1]);
    long double a = std::stold(argv[2]);
    int seconds = std::stoi(argv[3]);

    std::cout << "t: " << temperature << " a: " << a << " sec: " << seconds << std::endl;

    csvReader.openFile(); 
    std::vector<std::vector<std::string>> rows = csvReader.getRows(';', false);
    
    for (auto it : rows) { 
        //std::cout << typeid(it).name() << std::endl; 
        Task task = Task(it);

        if(task.type == TT) {
            taskSetAll.push_back(task);
            taskSetTT.push_back(task);
        } else {
            taskSetAll.push_back(task);
            taskSetET->push_back(task);
        }
    }

    /*for (auto task : taskSetTT) {
        std::cout << task.name << " " << task.duration << std::endl;
    }*/

    /*sa.performSimulatedAnnealing(&cities, temperature, a, seconds, swapCities, costTour);

    std::cout << sa.getBestCost() << std::endl;
    std::cout << sa.getNSolutions() << std::endl;

    std::vector<City> bestS = sa.getBestSolution();

    for (auto it : bestS) {
        std::cout << "'" << it.getName() << "',";
    }
    std::cout << std::endl;
    */

   //std::tuple<std::vector<std::string>, int, bool> returnValue; 
   //returnValue = edf(&taskSetTT);
   
   /*for (auto it : std::get<0>(returnValue)) {
        std::cout << it << std::endl;
   }*/

   //std::cout << std::endl << std::get<1>(returnValue) << " " << std::get<2>(returnValue) << std::endl;


    
   std::tuple<bool, std::map<std::string, int>> returnValue1;
   //good configuration
   //returnValue1 = isPollingServerSchedulable(250, 550, 650, taskSetET);
   //Task polling_server = Task("polling_server", 10, 20, ET, 7, 20, 0);
   
   Task polling_server = Task("polling_server", 250, 550, ET, 7, 650, 0);
   polling_server.et_subset = taskSetET;
   //returnValue1 = isPollingServerSchedulable(&polling_server);
   
   //std::string isSchedulable = std::get<0>(returnValue1) ? "True" : "False";
   //std::cout << "isSchedulable: " <<  isSchedulable << std::endl;

   /*for (auto it : std::get<1>(returnValue1)) {
        std::cout << it.first << " " << it.second << std::endl;
   }*/
   taskSetTT.push_back(polling_server);

   sa.performSimulatedAnnealing(&taskSetTT, temperature, a, seconds, getFromNeighborhood, costFunction);
   std::cout << "best cost: " << sa.getBestCost() << std::endl;
   std::cout << "number of generated solutions: " << sa.getNSolutions() << std::endl;
   std::vector<Task> best_solution = sa.getBestSolution();

   for (auto it : best_solution) {
    if(it.et_subset != NULL) {
        std::cout << "deadline: " << it.deadline << " period: " << it.period << " duration: " << it.duration << std::endl;
    }
   }
}   


/*

SimulatedAnnealer<Task>::performSimulatedAnnealing(std::vector<Task, std::allocator<Task> >*, long double, long double, int, std::vector<Task, std::allocator<Task> > (*)(std::vector<Task, std::allocator<Task> >), int (*)(std::vector<Task, std::allocator<Task> > const*))'
void performSimulatedAnnealing(std::vector<T>* s, long double t0, long double a, int stopcriterion_sec, std::vector<T> (*neighborhood_f)(std::vector<T>), int (*cost_f)(const std::vector<T>*));

void performSimulatedAnnealing(std::vector<T> *s, long double t, long double a, int stopcriterion_sec, std::vector<T> (*neighborhood_f)(std::vector<T>), int (*cost_f)(const std::vector<T>*)) { 
*/