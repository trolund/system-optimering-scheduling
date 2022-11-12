#include "solution_generator.h"
#include "csv_reader.h"

//#ifndef __TASK_H
//#define __TASK_H
//#endif

// content


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
    SolutionGenerator sg(&task_set_all, 2);

    /*solution s = sg.generate_solution();

    for (auto it : s.polling_servers) {
        std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
        for(auto et : *it.et_subset) {
            std::cout << et.name << " " << et.separation << " ";
        }
        std::cout << std::endl << std::endl;
    }*/

    std::vector<solution> population = sg.generate_population();

    for(auto sol : population) {
        for (auto it : sol.polling_servers) {
            std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
            for(auto et : *it.et_subset) {
                std::cout << et.name << " " << et.separation << " ";
            }
            std::cout << std::endl << std::endl;
        }
        std::cout << "__________" << std::endl << std::endl << std::endl;
    } 
    int x = 0;

    std::cout << &population[0] << " " << &population[1] << std::endl;
    population = sg.recombine(&population[0], &population[1], 1.0);

    for(auto sol : population) {
        for (auto it : sol.polling_servers) {
            std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
            for(auto et : *it.et_subset) {
                std::cout << et.name << " " << et.separation << " ";
            }
            std::cout << std::endl << std::endl;
        }
        std::cout << "__________" << std::endl << std::endl << std::endl;
    }

    for(int i = 0; i < population.size(); i = i + 1) {
        std::vector<Task> task_set = *population[i].tt_tasks;
        // do not think this works?? wait yeah yeah pollling servers is vector of task
        task_set.insert(task_set.end(), population[i].polling_servers.begin(), population[i].polling_servers.end());
        double cost = cost_function(&task_set);
        population[i].cost = cost;
        std::cout << "cost for this solution is: " << population[i].cost << " solution is: " << std::endl;
        for (auto itt : population[i].polling_servers) {
            std::cout << itt.name << " " << itt.duration << " " << itt.period << " " << " " << itt.deadline << " " << std::endl;
            for(auto et : *itt.et_subset) {
                std::cout << et.name << " " << et.separation << " ";
            }
            std::cout << std::endl << std::endl;
        }


    }

    for(auto it : population) { 
        std::cout << "cost for this solution is: " << it.cost << " solution is: " << std::endl;
        for (auto itt : it.polling_servers) {
            std::cout << itt.name << " " << itt.duration << " " << itt.period << " " << " " << itt.deadline << " " << std::endl;
            for(auto et : *itt.et_subset) {
                std::cout << et.name << " " << et.separation << " ";
            }
            std::cout << std::endl << std::endl;
        }


    }

    solution best_solution = sg.select(&population, 10);

    std::cout << "found best ____ cost is: " << best_solution.cost << std::endl;
    for (auto it : best_solution.polling_servers) {
            std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
            for(auto et : *it.et_subset) {
                std::cout << et.name << " " << et.separation << " ";
            }
            std::cout << std::endl << std::endl;
        }
        std::cout << "__________" << std::endl << std::endl << std::endl;
}