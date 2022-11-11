#include "solution_generator.h"

solution SolutionGenerator::generate_solution() {
    return (solution) {.polling_servers = NULL, .tt_tasks = NULL, .cost = 0.0};
}