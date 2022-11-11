#include "solution_generator.h"
#include "csv_reader.h"

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
    SolutionGenerator sg(&task_set_all);

    solution s = sg.generate_solution();

    for (auto it : s.polling_servers) {
        std::cout << it.name << " " << it.duration << " " << it.period << " " << " " << it.deadline << " " << std::endl;
        for(auto et : *it.et_subset) {
            std::cout << et.name << " " << et.separation << " ";
        }
        std::cout << std::endl << std::endl;
    }

    std::vector<solution> population = sg.generate_population(10);

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
}