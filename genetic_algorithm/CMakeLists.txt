cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#set(CMAKE_C_COMPILER "gcc")
#set(CMAKE_CXX_COMPILER "g++")
set (CMAKE_CXX_STANDARD 20)

# set the project name
project(sa_schedule_test)

include_directories(
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/src
)

set(CMAKE_BUILD_TYPE Debug)

# add libraries
add_library(CSVReader src/csv_reader.cpp)
set_property(TARGET CSVReader PROPERTY CXX_STANDARD 20)

add_library(Solutions src/solution_generator.cpp src/cost_functions.cpp src/task.cpp src/simple_genetic_algorithm.cpp)
set_property(TARGET Solutions PROPERTY CXX_STANDARD 20)
set( CMAKE_CXX_FLAGS "-fopenmp" )

#target_compile_features(Solutions PRIVATE cxx_std_20)# include src and include directories

# add the executable
add_executable(test_edf src/test_edf.cpp)
target_link_libraries(test_edf PUBLIC CSVReader Solutions)

add_executable(test_solution src/test_solution_generator.cpp)
target_link_libraries(test_solution PUBLIC CSVReader Solutions)

add_executable(test_cost src/test_cost.cpp)
set_property(TARGET test_cost PROPERTY CXX_STANDARD 20)
target_link_libraries(test_cost PUBLIC CSVReader Solutions)

add_executable(test_sga src/test_sga.cpp)
set_property(TARGET test_sga PROPERTY CXX_STANDARD 20)
target_link_libraries(test_sga PUBLIC CSVReader Solutions)

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(test_edf PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}"
                          )
# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(test_solution PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}"
                          )

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(test_sga PUBLIC
                        "${PROJECT_BINARY_DIR}"
                        "${PROJECT_SOURCE_DIR}"
)

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(test_cost PUBLIC
                        "${PROJECT_BINARY_DIR}"
                        "${PROJECT_SOURCE_DIR}"
)

