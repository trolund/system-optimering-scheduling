#include "simple_genetic_algorithm.h"
#include "csv_reader.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[]) {
    if(argc != 2) {
        std::cout << "./test_sga <test case>" << std::endl;
        std::cout << "Example: ./test_sga ../testcases_seperation_tested/taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__20__tsk.csv" << std::endl;
        std::cout << "Please provide a file that exists, no check is done" << std::endl;
        exit(0);
    }
  
    CSVReader csvReader = CSVReader(argv[1]);
    csvReader.openFile(); 
    
    std::vector<std::vector<std::string>> rows = csvReader.getRows(';', false);
    std::vector<Task> task_set_all, task_set_TT, task_set_ET;//, taskSetET; 

    for (auto it : rows) {  
        Task task = Task(it);

        if(task.type == TT) {
            task_set_all.push_back(task);
            task_set_TT.push_back(task);
        } else {
            task_set_all.push_back(task);
            task_set_ET.push_back(task);
        }
    }
    std::vector<std::string> test_case = csvReader.splitString(argv[1], '/');
    // kind of weird with the population size arg
    SolutionGenerator solution_generator(&task_set_all); 
    SimpleGeneticAlgorithm sga(&solution_generator, 0.9, 0.05, test_case.at(test_case.size()-1));
    
    sga.perform_sga(2048, 30, cost_function);
    solution best_solution = sga.get_best_solution();

    std::cout << std::endl << "best cost is: " << best_solution.cost << " is schedulable: " << best_solution.is_schedulable << std::endl;
    for (auto it : best_solution.polling_servers) {
        std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
        for(auto et : *it.et_subset) {
            std::cout << et.name << " " << et.separation << " ";
        }
        std::cout << std::endl << std::endl;
    }
}
