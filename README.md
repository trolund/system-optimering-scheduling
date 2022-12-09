# Scheduling optimization

This is a project done as part of the course 02229 - Systems Optimization at DTU

## Running the code

In general the code has the structure: 
    genetic_algorithm
    sa_scheduling


As the Genetics Algorithm has been implemented with C++ and Simulated Annealing has been implemented with Python, there are some prerequsites to the environment in which the code is being run


### Genetics Algorithm:
On windows:
    Prerequsites:
        mingw
        cmake
        make

        This has been installed with the packet manager Chocolatey
            choco install mingw
	        choco install cmake
	        choco install make


    Build and run the code:
        go into the folder "genetic_algorithm"
        cmake . -B Build -G "MinGW Makefiles"
	    cd Build
	    make

        This will now compile the .exe files that can be run
            ./test_sga.exe

On Linux:

    From the folder genetic_algorithms:
    mkdir build
    cd build 
    cmake ..
    cmake --build . 

### Simulated annealing 
Windows:
    Prerequsites:
        python version 3.9
        pip
        Install necessary libraries
            pip install -r requirements.txt
    

    The code has been tested running with **Python 3.9**.

    The code can run by execution the **main.py** located in the **simulated_annealing** folder.

        python main.py <path to test case CSV> <Stop criterion in sec>

    The files in the **test_cases** folder can be run like this:

        python main.py ../test_cases/taskset_small__3__.csv 20

Linux:

    Same as on Windows


### Other notes:
    There has been some issues when running on different environments which has been caused by the code running in several threads. If any issues occur regarding basic_string::_M_create, comment out the following lines:

        pragma omp parallel for num_threads(4)
            in genetic_algorithm/src/simple_genetic_algorithm.cpp:40 and 76 
    
     to only run with one thread which should fix the issue