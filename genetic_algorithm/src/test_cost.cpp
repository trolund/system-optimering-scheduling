#include "simple_genetic_algorithm.h"
//#include "cost_functions.h"
#include "csv_reader.h"

int main() {

    //CSVReader csvReader = CSVReader("../testcases_seperation_tested/taskset__1643188013-a_0.1-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv");

    //CSVReader csvReader = CSVReader("../testcases_seperation_tested/taskset__1643188175-a_0.2-b_0.3-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv");
    
    CSVReader csvReader = CSVReader("../testcases_seperation_tested/taskset_small.csv");
    csvReader.openFile(); 
    std::vector<std::vector<std::string>> rows = csvReader.getRows(';', false);
    std::vector<Task> task_set_all, task_set_TT, task_set_ET;//, taskSetET; 
    std::vector<Task> et1, et2, et3;
    std::vector<std::vector<Task>> separated(3);
    separated[0] = et1;
    separated[1] = et2;
    separated[2] = et3;
    std::vector<Task> *ets_1 = new std::vector<Task>; 
    std::vector<Task> *ets_2 = new std::vector<Task>;  
    std::vector<Task> *ets_3 = new std::vector<Task>; 
    //Task ps1 = Task("ps1", 47, 150, TT, 7, 145, 0);
    //Task ps2 = Task("ps2", 19, 500, TT, 7, 480, 0);//, &separated.at(1));
    //Task ps3 = Task("ps3", 2, 150, TT, 7, 145, 0);//, &separated.at(2));
    for (auto it : rows) { 
        //std::cout << typeid(it).name() << std::endl; 
        Task task = Task(it);

        if(task.type == TT) {
            task_set_all.push_back(task);
            task_set_TT.push_back(task);
        } else {
            task_set_all.push_back(task);
            task_set_ET.push_back(task);
            if (task.separation == 1) {
                ets_1->push_back(task);
            } else if(task.separation == 2) {
                ets_2->push_back(task);
            } else if(task.separation == 3) {
                ets_3->push_back(task);
            }
            //std::cout << task.separation << std::endl; 
            //separated.at(task.separation-1).push_back(task);
        }
    }

    Task ps1 = Task("ps1", 47, 150, TT, 7, 145, ets_1);
    Task ps2 = Task("ps2", 19, 500, TT, 7, 480, ets_2);
    Task ps3 = Task("ps3", 2, 150, TT, 7, 145, ets_3);
    task_set_TT.push_back(ps1);
    task_set_TT.push_back(ps2);
    task_set_TT.push_back(ps3);
    std::tuple<double, bool> cost = cost_function(&task_set_TT);
    std::cout << "cost: " << std::get<0>(cost) << " is sched: " << std::get<1>(cost) << std::endl;

    //Task::Task(std::string name, int duration, int period, int type, int priority, int deadline, std::vector<Task>* et_subset) {
    /*Task ps1 = Task("ps1", 1, 24, TT, 7, 1, &separated.at(1));
    Task ps2 = Task("ps2", 3, 60, TT, 7, 10, &separated.at(0));
    Task ps3 = Task("ps3", 1, 32, TT, 7, 5, &separated.at(2));

    task_set_TT.push_back(ps1);
    task_set_TT.push_back(ps2);
    task_set_TT.push_back(ps3);

    std::tuple<bool, std::map<std::string, double>, std::vector<std::string>> thing;

    thing = edf(&task_set_TT);

    bool is_schedulable = std::get<0>(thing);
    //assert(!is_schedulable);
    std::tuple<double, bool> cost = cost_function(&task_set_TT);
    
    is_schedulable = std::get<1>(cost); 
    std::cout << is_schedulable << std::endl; 
    //double expected_cost = (3 + 100 + 4 + 100) / 2.0;
    //assert(cost == expected_cost);
    std::cout << std::get<0>(cost) << std::endl;*/
    


}