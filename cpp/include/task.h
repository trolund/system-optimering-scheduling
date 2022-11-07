#include <string>
#include <vector>

#define TT 0
#define ET 1

#define NAME 0
#define DURATION 1
#define PERIOD 2
#define TYPE 3
#define PRIORITY 4
#define DEADLINE 5
#define RELEASE_TIME 6
#define ET_SUBSET 7

class Task {
    public:
        std::string name;
        int duration;
        int period;
        int type;
        int priority;
        int deadline;
        int releaseTime;
        std::vector<Task> *et_subset;

        Task(std::vector<std::string>);
        
        Task(std::string name, std::string duration, std::string period, std::string type, std::string priority, std::string deadline);
        
        Task(std::string name, int duration, int period, int type, int priority, int deadline, int releaseTime);
        
        //std::vector<Task> evictFromSubset(int start, int stop);
        //void addToSubset(std::vector<Task>);

        // https://thispointer.com/c-how-to-sort-a-list-of-objects-with-custom-comparator-or-lambda-function/
        // less than operator operating on deadline
        bool operator< (const Task& otherTask) const {
            return this->deadline < otherTask.deadline;
        }
};



/*

def __init__(self, name: str, duration: int, period: int, type: TaskType, priority: int, deadline: int, et_subset=None):
        self.name = name
        self.duration = duration
        self.period = period
        self.type = type
        self.priority = priority
        self.deadline = deadline
        self.release_time = 0
        if et_subset != None:
            self.et_subset = et_subset


*/
