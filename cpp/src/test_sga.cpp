#include "simple_genetic_algorithm.h"
#include "csv_reader.h"
#include <iostream>

using namespace std;

int main() {
    CSVReader csvReader = CSVReader("../testcases_seperation_tested/taskset__1643188539-a_0.6-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv");
    csvReader.openFile(); 
    std::vector<std::vector<std::string>> rows = csvReader.getRows(';', false);
    std::vector<Task> task_set_all, task_set_TT, task_set_ET;//, taskSetET; 

    for (auto it : rows) { 
        //std::cout << typeid(it).name() << std::endl; 
        Task task = Task(it);

        if(task.type == TT) {
            task_set_all.push_back(task);
            task_set_TT.push_back(task);
        } else {
            task_set_all.push_back(task);
            task_set_ET.push_back(task);
        }
    }

    // kind of weird with the population size arg
    SolutionGenerator solution_generator(&task_set_all, 32); 
    SimpleGeneticAlgorithm sga(&solution_generator, 0.9, 0.05);
    sga.perform_sga(32, 10, cost_function);

    solution best_solution = sga.get_best_solution();
    for (auto it : best_solution.polling_servers) {
        std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
        for(auto et : *it.et_subset) {
            std::cout << et.name << " " << et.separation << " ";
        }
        std::cout << std::endl << std::endl;
    }
}