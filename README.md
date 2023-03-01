# Bandits

## Problem Statement

# Bandit Algorithm Exploration

For this assignment, we will be exploring bandits. You have been provided with two CSV files, each of which presents different sets of arms and rewards. The rewards in one file are boolean (0 or 1), while the rewards in the other range from 0 to 100. 

Your task is to implement three types of bandit algorithms: 
1. Basic stationary 
2. Rolling average which scales the weight by the data 
3. Exponential recency-weighted average or the pseudostationary algorithm with a window size of 10. 

As your code is run, it should print out: the current step, the decision made, the current reward, and the cumulative reward. 

Your code should be called as follows: 

``` java -jar Bandit.jar <alg> <exp> <dist> <decay> <rwt> <w0> <infile> ``` 

Where: 

- `alg` is one of "STAT" "ROLL" and "REC" for the three types.
- `exp` is the exploration rate. 
- `dist` is the uniform distribution parameter, use the same distribution for all values a.
- `decay` is the decay rate f. For the nonstationary REC or nonstationary version, we use this for v.
- `rwt` is the reward weight function w.
- `w0` is the initial weight value for the arms w0a.
- `infile` is the appropriate ad data file.

Having implemented the bandits, you will need to call them on the files using several different parameter values and report how each bandit type performed under different parameter settings. Your goal in this is to assess whether the parameter values have a significant impact on the performance of the algorithms.

Note: For the purposes of this assignment, you may make use of the Apache Commons CSV library in your code. 

As always, your code should be clear, readable, and well-documented.

