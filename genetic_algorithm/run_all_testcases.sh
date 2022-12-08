#!/bin/bash

#testCases=("../testcases_seperation_tested/taskset__1643188013-a_0.1-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv" "../testcases_seperation_tested/taskset_small.csv")
#taskset__1643188013-a_0.1-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv   taskset__1643188175-a_0.2-b_0.3-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv  taskset_small.csv
#taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__20__tsk.csv  taskset__1643188539-a_0.6-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv

#testCases=("../testcases_seperation_tested/taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__20__tsk.csv" "../testcases_seperation_tested/taskset__1643188175-a_0.2-b_0.3-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv" "../testcases_seperation_tested/taskset__1643188539-a_0.6-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv" "../testcases_seperation_tested/taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__99__tsk.csv")
#testCases=("../testcases_seperation_tested/taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__99__tsk.csv")
testCases=("../testcases_seperation_tested/taskset__1643188613-a_0.7-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__99__tsk.csv")
for i in ${!testCases[@]}; do
    echo testing ${testCases[$i]} 10 times
    for j in {1..10}; do
        ./test_sga ${testCases[$i]} >> $i$i$i.csv
	echo iteration $j finished
    done
done

shutdown now 

