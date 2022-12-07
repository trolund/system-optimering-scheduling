# Scheduling optimization

This is a project done as part of the course 02229 Systems Optimization at DTU

The following will be instructions on how to run the code.

In general the code has the structure: 
    genetic_algorithm
    sa_scheduling


As the Genetics Algorithm has been implemented with C++ and Simulated Annealing has been implemented with Python, there are some prerequsites to the environment in which the code is being run


On Windows:
Genetics Algorithm:
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

Simulated Annealing:
    Prerequsites:
        python version 3.9
        pip
        Install necessary libraries
            pip install -r requirements.txt
    

    Build and run the code
        go into the folder "sa_scheduling"
        python main.py [options]
            e.g python main.py testcases_seperation_tested 1 2000 0.99 5 or python3.9 main.py testcases_seperation_tested 1 2000 0.99 5


On Linux:
    Genetics:
        XXX

    Simulated Annealing:
        Same procedure as on Windows


Other notes:
    There has been some issues when running on different environments which has been caused by the code running in several threads. If any issues occur regarding basic_string::_M_create, comment out the following lines:

        pragma omp parallel for num_threads(4)
            in genetic_algorithm/src/simple_genetic_algorithm.cpp:40 and 76 
    
     to only run with one thread which should fix the issue
