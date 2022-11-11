cmake_minimum_required(VERSION 3.10)

# set the project name
project(sa_schedule_test)

# include src and include directories
include_directories(
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/src
)

set(CMAKE_BUILD_TYPE Debug)

# add libraries
add_library(CSVReader src/csv_reader.cpp)
#add_library(SimulatedAnnealing src/simulated_annealing.cpp)
add_library(CostFunctions src/cost_functions.cpp)
#add_library(City src/city.cpp)
add_library(Task src/task.cpp)
add_library(Solutions src/solution_generator.cpp)
#set_property(TARGET SimulatedAnnealing PROPERTY CXX_STANDARD 20)
set_property(TARGET CostFunctions PROPERTY CXX_STANDARD 20)
set_property(TARGET Solutions PROPERTY CXX_STANDARD 20)

# add the executable
#add_executable(test src/main.cpp)
#set_property(TARGET test PROPERTY CXX_STANDARD 20)

add_executable(test_edf src/test_edf.cpp)
target_link_libraries(test_edf PUBLIC CSVReader Task CostFunctions)

add_executable(test_solution src/test_solution_generator.cpp)
target_link_libraries(test_solution PUBLIC CSVReader Task Solutions)


# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(test_edf PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}"
                          )
