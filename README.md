# EE597 Lab 1
NS-3 Simulation\
Wireless Network Topology(Multiple Transmission devices and one Base station)\
Evaluation on how Number of nodes and Data Rate affect the Wifi Backoff Window size and Total Throughput of network\

accomplished by Qiushi Xu and Yiyi Li

## File Structure
- Lab1.cc --> this is the main program containing NS-3 code where we calculate throughput and per-node throughput based on the input values of node number and data rate. The output of this programm will be saved in data.csv.
- Lab1Run.py --> this script can execute Lab1.cc for several times, and read the data from data.csv, generating the corresponding figures for each case.
- data.csv --> this is the file for saving data from Lab1.cc, and the data will be cleared once we run the script.



## Environment requirement
- NS-3
- We provide a script called `Lab1Run.py`. In this shell, we import `matplotlib` package to generate figures based on the data from lab1. In this way, `matplotlib` package needs to be installed before running the shell. You can install it by using the following command.
```
sudo apt-get install python3-matplotlib
```

## How to run
To run different cases in Lab 1, you can use different argument when run `Lab1Run.py`. 


- For Case A E1, use the command `./Lab1Run.py CaseA E1`
- For Case A E2, use the command `./Lab1Run.py CaseA E2`
- For Case B E1, use the command `./Lab1Run.py CaseB E1`
- For Case B E2, use the command `./Lab1Run.py CaseB E2`
- To run all cases together, use the command `./Lab1Run.py runall`

You can also directly call `./waf --run "Lab1.cc --dataRate=R --nWifi=N -case="`  where case = 1 or 2.
