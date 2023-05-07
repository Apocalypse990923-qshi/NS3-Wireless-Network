#! /usr/bin/env python3
import sys
from optparse import OptionParser
import os
from xml.dom import minidom as dom
import shlex
import matplotlib.pyplot as plt
import numpy as np
import csv

#import constants
#from util import run_command, fatal, CommandError

# def variance():
#     throughput = []
#     with open('pernode.csv','a+') as f:
#         data_reader = csv.reader(f)
#         for row in data_reader:
#             throughput.append(float(row[0]))
#         f.truncate(0)
#     var = np.var(throughput)
#     # return var
def calculate_per_node_throughput(throughput):
	with open('pernode.csv','r') as f:
		data_reader = csv.reader(f)
		node = 0
		for row in data_reader:
			print(row[0])
			throughput[node].append(float(row[0]))
			node += 1
	with open('pernode.csv','a+') as f:
		f.truncate(0)

                
def Ae1():
    num = list(range(1,21))
    numR = [float(i*1.0/2) for i in num]
    with open('CaseA_E1.csv','a+') as f:
        f.truncate(0)
    for i in range(1,21):
        os.system("./waf --run \"Lab1.cc -file_name=CaseA_E1.csv -case=1 -nWifi=" + str(i)+"\"")
    avgThroughpput_Ae1 = []
    totalThroughput_Ae1 = []
    avgBackoff_Ae1 = []
    collisionRate_Ae1 = []
    variance_Ae1=[]
    # var = variance()
    with open('CaseA_E1.csv','r') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            totalThroughput_Ae1.append(float(row[0]))
            avgThroughpput_Ae1.append(float(row[1]))
            avgBackoff_Ae1.append(float(row[2]))
            collisionRate_Ae1.append(float(row[3]))
            variance_Ae1.append(float(row[4]))
    plt.figure(1)
    plt.plot(num, avgThroughpput_Ae1)
    plt.title("Throughput per node Vs transmitter Nodes in Case A E1")
    plt.xlabel('N (Number of Nodes)')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("AE1_NVsAvgThroughput.png")


    plt.figure(2)
    plt.plot(num, totalThroughput_Ae1)
    plt.title("Total Throughput Vs transmitter Nodes in Case A E1")
    plt.xlabel('N (Number of Nodes)')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("AE1_NVsTotalThroughput.png")

    plt.figure(3)
    plt.scatter(numR, avgBackoff_Ae1)
    plt.title("Avg backoff Vs N/R in Case A E1")
    plt.xlabel("N/R")
    plt.ylabel("Average Backoff")
    plt.savefig("AE1_NR_VS_AvgBackoff.png")


    plt.figure(4)
    plt.scatter(numR, collisionRate_Ae1)
    plt.title("collision rate Vs N/R in Case A E1")
    plt.xlabel("N/R")
    plt.ylabel("collision rate")
    plt.savefig("AE1_NR_VS_collision.png")

    plt.figure(5)
    plt.scatter(numR,variance_Ae1)
    plt.title("Variance of backoff time slots Vs N/R in Case A E1")
    plt.xlabel("N/R")
    plt.ylabel("V[backoff]")
    plt.savefig("AE1_NR_VS_var.png")
    # return var

def Be1():
    num = list(range(1,21))
    numR = [float(i*1.0/2) for i in num]
    with open('CaseB_E1.csv','a+') as f:
        f.truncate(0)
    for i in range(1,21):
        os.system("./waf --run \"Lab1.cc -file_name=CaseB_E1.csv -nWifi=" + str(i)+"\"")
    avgThroughpput_Be1 = []
    totalThroughput_Be1 = []
    avgBackoff_Be1 = []
    collisionRate_Be1 = []
    variance_Be1=[]
    # var = variance()
    with open('CaseB_E1.csv','r') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            totalThroughput_Be1.append(float(row[0]))
            avgThroughpput_Be1.append(float(row[1]))
            avgBackoff_Be1.append(float(row[2]))
            collisionRate_Be1.append(float(row[3]))
            variance_Be1.append(float(row[4]))
    plt.figure(6)
    plt.plot(num, avgThroughpput_Be1)
    plt.title("Throughput per node Vs transmitter Nodes in Case B E1")
    plt.xlabel('N (Number of Nodes)')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("BE1_NVsAvgThroughput.png")

    plt.figure(7)
    plt.plot(num, totalThroughput_Be1)
    plt.title("Total Throughput Vs transmitter Nodes in Case B E1")
    plt.xlabel('N (Number of Nodes)')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("BE1_NVsTotalThroughput.png")


    plt.figure(8)
    plt.scatter(numR, avgBackoff_Be1)
    plt.title("Avg backoff Vs N/R in Case B E1")
    plt.xlabel("N/R")
    plt.ylabel("Average Backoff")
    plt.savefig("BE1_NR_VS_AvgBackoff.png")

    plt.figure(9)
    plt.scatter(numR, collisionRate_Be1)
    plt.title("collision rate Vs N/R in Case B E1")
    plt.xlabel("N/R")
    plt.ylabel("collision rate")
    plt.savefig("BE1_NR_VS_collision.png")

    plt.figure(10)
    plt.scatter(numR,variance_Be1)
    plt.title("Variance of backoff time slots Vs N/R in Case B E1")
    plt.xlabel("N/R")
    plt.ylabel("V[backoff]")
    plt.savefig("BE1_NR_VS_var.png")
    # return var

    

def Ae2():
    num = np.linspace(0.01,2,50)
    numR = [float(20/i) for i in num]
    node_throughput = []
    with open('CaseA_E2.csv','a+') as f:
        f.truncate(0)
    for i in range(20):
	    node_throughput.append([])
    for i in num:
        os.system("./waf --run \"Lab1.cc -file_name=CaseA_E2.csv -case=1 -dataRate=" + str(i)+"\"")
        calculate_per_node_throughput(node_throughput)
        # print("The data rate is ",i,"Mbps")
    avgThroughpput_Ae2 = []
    totalThroughput_Ae2 = []
    avgBackoff_Ae2 = []
    collisionRate_Ae2 = []
    variance_Ae2 = []
    
    
    # var = variance()
    with open('CaseA_E2.csv','r') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            totalThroughput_Ae2.append(float(row[0]))
            avgThroughpput_Ae2.append(float(row[1]))
            avgBackoff_Ae2.append(float(row[2]))
            collisionRate_Ae2.append(float(row[3]))
            variance_Ae2.append(float(row[4]))
    plt.figure(11)
    plt.plot(num, avgThroughpput_Ae2,label="Average throughput",linewidth=5)
    for i in range(20):
		plt.plot(num, node_throughput[i],label="Throughput of node "+str(i))
	plt.legend()
    plt.title("Throughput per node Vs transmitter Nodes in Case A E2")
    plt.xlabel('DataRate/Mbps')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("AE2_R_VS_AvgThroughput.png")

    plt.figure(12)
    plt.plot(num, totalThroughput_Ae2)
    plt.title("Total Throughput Vs transmitter Nodes in Case A E2")
    plt.xlabel('DataRate/Mbps')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("AE2_R_VS_TotalThroughput.png")

    plt.figure(13)
    plt.scatter(numR[3:], avgBackoff_Ae2[3:])
    plt.title("Avg backoff Vs N/R in Case A E2")
    plt.xlabel("N/R")
    plt.ylabel("Average Backoff")
    plt.savefig("AE2_NR_VS_AvgBackoff.png")

    plt.figure(14)
    plt.scatter(numR[3:], collisionRate_Ae2[3:])
    plt.title("collision rate Vs N/R in Case A E2")
    plt.xlabel("N/R")
    plt.ylabel("collision rate")
    plt.savefig("AE2_NR_VS_collision.png")

    plt.figure(15)
    plt.scatter(numR[3:],variance_Ae2[3:])
    plt.title("Variance of backoff time slots Vs N/R in Case A E2")
    plt.xlabel("N/R")
    plt.ylabel("V[backoff]")
    plt.savefig("AE2_NR_VS_var.png")
    # return var


def Be2():
    num = np.linspace(0.01,2,50)
    numR = [float(20/i) for i in num]
    node_throughput=[]
    with open('CaseB_E2.csv','a+') as f:
        f.truncate(0)
	for i in range(20):
		node_throughput.append([])
    for i in num:
        os.system("./waf --run \"Lab1.cc -file_name=CaseB_E2.csv -dataRate=" + str(i)+"\"")
        calculate_per_node_throughput(node_throughput)
        # print("The data rate is ",i,"Mbps")
    avgThroughpput_Be2 = []
    totalThroughput_Be2 = []
    avgBackoff_Be2 = []
    collisionRate_Be2 = []
    variance_Be2 = []
    # var = variance()
    with open('CaseB_E2.csv','r') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            totalThroughput_Be2.append(float(row[0]))
            avgThroughpput_Be2.append(float(row[1]))
            avgBackoff_Be2.append(float(row[2]))
            collisionRate_Be2.append(float(row[3]))
            variance_Be2.append(float(row[4]))
    plt.figure(16)
    plt.plot(num, avgThroughpput_Be2,label="Average throughput",linewidth=5)
    for i in range(20):
		plt.plot(num, node_throughput[i],label="Throughput of node "+str(i))
	plt.legend()
    plt.title("Throughput per node Vs transmitter Nodes in Case B E2")
    plt.xlabel('DataRate/Mbps')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("BE2_R_VS_AvgThroughput.png")

    plt.figure(17)
    plt.plot(num, totalThroughput_Be2)
    plt.title("Total Throughput Vs transmitter Nodes in Case B E2")
    plt.xlabel('DataRate/Mbps')
    plt.ylabel('Throughput/Mbps',rotation=0)
    plt.savefig("BE2_R_VS_TotalThroughput.png")

    plt.figure(18)
    plt.scatter(numR[3:], avgBackoff_Be2[3:])
    plt.title("Avg backoff Vs N/R in Case B E2")
    plt.xlabel("N/R")
    plt.ylabel("Average Backoff")
    plt.savefig("BE2_NR_VS_AvgBackoff.png")

    plt.figure(19)
    plt.scatter(numR[3:], collisionRate_Be2[3:])
    plt.title("collision rate Vs N/R in Case B E2")
    plt.xlabel("N/R")
    plt.ylabel("collision rate")
    plt.savefig("BE2_NR_VS_collision.png")
    
    plt.figure(20)
    plt.scatter(numR[3:],variance_Be2[3:])
    plt.title("Variance of backoff time slots Vs N/R in Case B E2")
    plt.xlabel("N/R")
    plt.ylabel("V[backoff]")
    plt.savefig("BE2_NR_VS_var.png")
    # return var

def runAll():
    Ae1()
    Ae2()
    Be1()
    Be2()



def main(argv):
    print(argv)
    if argv[1] == 'CaseA':
        if argv[2] == 'E1':
            Ae1()
        elif argv[2] == 'E2':
            Ae2()
        else:
            print("Wrong syntax,  please instert ./sh.py CaseX En, where X and n are the number of case")
    elif argv[1] == 'CaseB':
        if argv[2] == 'E1':
            Be1()
        elif argv[2] == 'E2':
            Be2()
        else:
            print("Wrong syntax,  please instert ./sh.py CaseX En, where X and n are the number of case")
    elif argv[1] == 'runall':
        runAll()
    else:
        print("Wrong syntax!")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
