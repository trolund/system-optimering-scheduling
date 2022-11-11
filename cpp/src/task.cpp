#include "task.h"

Task::Task(std::vector<std::string> values) {
    this->name = values[0];
    this->duration = stoi(values[1]);
    this->period = stoi(values[2]);
    this->type = values[3].compare("TT") == 0 ? TT : ET;
    this->priority = stoi(values[4]);
    this->deadline = stoi(values[5]);
    this->release_time = 0;
}


Task::Task(std::string name, std::string duration, std::string period, std::string type, std::string priority, std::string deadline) {
    this->name = name;
    this->duration = stoi(duration);
    this->period = stoi(period);
    this->type = type.compare("TT") == 0 ? TT : ET;
    this->priority = stoi(priority);
    this->deadline = stoi(deadline);
    this->release_time = 0;
    this->et_subset = NULL;
}


Task::Task(std::string name, int duration, int period, int type, int priority, int deadline, int release_time) {
    this->name = name;
    this->duration = duration;
    this->period = period;
    this->type = type;
    this->priority = priority;
    this->deadline = deadline;
    this->release_time = release_time;
    this->et_subset = NULL;
}

Task::Task(std::string name, int duration, int period, int type, int priority, int deadline, std::vector<Task>* et_subset) {
    this->name = name;
    this->duration = duration;
    this->period = period;
    this->type = type;
    this->priority = priority;
    this->deadline = deadline;
    this->release_time = 0;
    this->et_subset = et_subset;
}