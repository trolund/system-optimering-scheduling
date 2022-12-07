# Scheduling optimization

This is a project done as part of the course 02229 Systems Optimization at DTU

The following will be instructions on how to run the code.

In general the code has the structure: 
XXX



As the Genetics Algorithm has been implemented with C++ and Simulated Annealing has been implemented with Python, there are some prerequsites to the environment in which the code is being run


On Windows:
The following has been done to run genetics on Windows environment
Genetics Algorithm
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

Simulated Annealing:
    Prerequsites:
        python
    

    Build and run the code
        go into the folder "sa_scheduling"
        python main.py [options]
