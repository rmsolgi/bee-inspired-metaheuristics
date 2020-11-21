#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 23:47:40 2019

@author: Mohammad Solgi
"""



import numpy as np
import os
import csv
import time
import statistics

import copy
import Function
import Algorithm





nfe_intervals=[]
for i in range(100,500000,2000):
    nfe_intervals.append(i)






II=False
while II==False:


    Input= input("Enter a list of algorithms as below: "+\
                         "\nFor ABC     enter 1"
                         "\nFor BA      enter 2"
                         "\nFor BCO     enter 3"
                         "\nFor HBeeGA  enter 4"
                         "\nFor BS      enter 5"
                         "\nFor BSO     enter 6"
                         "\nFor FMBO    enter 7"
                         "\nFor HBMO    enter 8"
                         "\nFor MBO     enter 9"
                         "\nFor QBE     enter 10"
                         "\nEnter your list here (separate entries by space): ")
    A_list = Input.split(" ")
    Algorithm_list=[]
    for i in A_list:
        if i == "1": Algorithm_list.append(Algorithm.ABC) 
        if i == "2": Algorithm_list.append(Algorithm.BA) 
        if i == "3": Algorithm_list.append(Algorithm.BCO) 
        if i == "4": Algorithm_list.append(Algorithm.HBeeGA) 
        if i == "5": Algorithm_list.append(Algorithm.BS) 
        if i == "6": Algorithm_list.append(Algorithm.BSO) 
        if i == "7": Algorithm_list.append(Algorithm.FMBO) 
        if i == "8": Algorithm_list.append(Algorithm.HBMO) 
        if i == "9": Algorithm_list.append(Algorithm.MBO) 
        if i == "10": Algorithm_list.append(Algorithm.QBE) 
    
    
    
    print("Algorithm list is ", str(Algorithm_list))
    Input= input("Enter a list of problems as below: "+\
                         "\nFor Ackley          enter 1"+\
                         "\nFor Griewank        enter 2"
                         "\nFor Michalewicz     enter 3"
                         "\nFor Rastrigin       enter 4"
                         "\nFor Rosenbrock      enter 5"
                         "\nFor Schaffer        enter 6"
                         "\nFor Sphere          enter 7"
                         "\nFor Schwefel        enter 8"
                         "\nFor Weierstrass     enter 9"
                         "\nFor Constrained     enter 10"
                         "\nEnter your list here (separate entries by space): ")    
    P_list = Input.split()
    Problem_list=[]
    for i in P_list:
        if i == "1": Problem_list.append(Function.Ackley) 
        if i == "2": Problem_list.append(Function.Griewank) 
        if i == "3": Problem_list.append(Function.Michalewicz) 
        if i == "4": Problem_list.append(Function.Rastrigin) 
        if i == "5": Problem_list.append(Function.Rosenbrock) 
        if i == "6": Problem_list.append(Function.Schaffer) 
        if i == "7": Problem_list.append(Function.Sphere) 
        if i == "8": Problem_list.append(Function.Schwefel) 
        if i == "9": Problem_list.append(Function.Weierstrass) 
        if i == "10": Problem_list.append(Function.Constrained) 
    
    Input=False
    while (Input==False):
        dim=input("\n"+"Enter dimension of the problem (integer): ")
        try:
                dim = int(dim)
                Input=True
        except ValueError:
                print("\n"+"That's not an int!")
                Input=False
    Input=False
    while (Input==False):
        n_run=input("\n"+"Enter number of runs (integer): ")
        try:
                n_run = int(n_run)
                Input=True
        except ValueError:
                print("\n"+"That's not an int!")
                Input=False
    print("\n*********************************")
    pr=""      
    for k in Algorithm_list:
        pr+=str(k.__name__)+" "
        
    print("\nAlgorithm list is ", pr)
    pr=""
    for k in Problem_list:
        pr+=str(k.__name__)+" "
    print("\nProblem list is ", pr)
    print("\nDimension is ", str(dim))
    print("\nNumber of run is ", str(n_run))
    
    while True:
        dec=input("\n"+"Do you want to continue? (y/n)_")
        if dec == "y":
            II=True
            break
        if dec == "n":
            II=False
            break    

dirpath = os.getcwd()
os.chdir(dirpath)
csvData=[['']]
for n in Problem_list:
    csvData[0].append(n.__name__)
for n in Algorithm_list:
    csvData.append([n.__name__])
with open(dirpath+'/All_ave.csv', 'w') as csvFile:
    writer=csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()


csvData=[['']]
for n in Problem_list:
    csvData[0].append(n.__name__)
for n in Algorithm_list:
    csvData.append([n.__name__])
with open(dirpath+'/All_std.csv', 'w') as csvFile:
    writer=csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()
    
csvData=[['']]
for n in Problem_list:
    csvData[0].append(n.__name__)
for n in Algorithm_list:
    csvData.append([n.__name__])
with open(dirpath+'/All_time.csv', 'w') as csvFile:
    writer=csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()

csvData=[]
#for n in Algorithm_list:
#    for p in Problem_list:
#        csvData[0].append(n.__name__+'_'+p.__name__+'_nfe')
#        csvData[0].append(n.__name__+'_'+p.__name__+'_OF')
with open(dirpath+'/All_OF.csv', 'w') as csvFile:
    writer=csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()
###############################################################################

###############################################################################
counter=0
for m in Algorithm_list:
    for f in Problem_list:
###############################################################################

        total_report=[]
        total_report_interped=[]
        total_nfe=[]
        total_best=[[None]*1]*n_run
        total_solution=[[None]*1]*n_run
        total_runtime=[[None]*1]*n_run
###############################################################################
        counter+=2
        
        function_name=f.__name__
        algorithm_name=m.__name__
        
        problem=f()

#        model=m(function=problem,lower_boundary=problem.L*dim,upper_boundary=problem.U*dim)
#        alg_param=model.algorithm_parameters
        for n in range(0,n_run):
            model=m(function=problem,lower_boundary=problem.L*dim,upper_boundary=problem.U*dim)
            alg_param=model.algorithm_parameters
            
            problem.nfe=0
            start_time=time.perf_counter()
        
            cost=model.run()
            
            run_time=time.perf_counter()-start_time
            NFE=problem.nfe

            
###############################################################################
###############################################################################

            modified_report=[copy.deepcopy(model.report[0])]
            for y in range(1,len(model.report)):
                if model.report[y]<modified_report[y-1]:
                    modified_report.append(model.report[y])
                else:
                    modified_report.append(modified_report[y-1])
            
            report_interped=np.interp(nfe_intervals,model.nfe,modified_report)
            
            total_report_interped.append(report_interped)
            total_report.append(report_interped)
            total_nfe.append(nfe_intervals)
                        
            index=model.report.index(min(model.report))
            total_best[n]=copy.deepcopy(model.report[index])
            total_solution[n]=copy.deepcopy(model.report_solution[index])
            total_runtime[n]=run_time
            
#            print(model.nfe)
#            print(model.report)
#            print("interped")
#            print(report_interped)
            
            


            
            print("\nRun #"+str(n+1)+" "+str(algorithm_name)+"-"+\
                  str(function_name)+" is done.")
        ave_rep=[]
        for jj in range (0,len(nfe_intervals)):
            temp_rep=[]
            for n in range(0,n_run):
                temp_rep.append(total_report_interped[n][jj])
            ave_rep.append(statistics.mean(temp_rep))
           
            
            
        bl=copy.deepcopy(total_best)
        runtime=np.array(total_runtime)
        bestnp=np.array(bl)
        std=np.std(bestnp)
        mean=np.mean(bestnp)
        thebest=np.min(bestnp)
        theworst=np.max(bestnp)
        avetime=np.mean(runtime)
        
        
        with open(dirpath+'/All_ave.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            for z in range (0,len(lines)):
                if lines[z][0]==m.__name__:
                    
                    lines[z].append(mean)
            
        with open(dirpath+'/All_ave.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()
             
        with open(dirpath+'/All_std.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            for z in range (0,len(lines)):
                if lines[z][0]==m.__name__:
                    
                    lines[z].append(std)
            
        with open(dirpath+'/All_std.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()       
        
        with open(dirpath+'/All_time.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            for z in range (0,len(lines)):
                if lines[z][0]==m.__name__:
                    
                    lines[z].append(avetime)
            
        with open(dirpath+'/All_time.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()  
        

        
        with open(dirpath+'/All_OF.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines.append([])
            lines[counter-2].append(m.__name__+'_'+f.__name__+'_nfe')
            for z in range(0, len(nfe_intervals)):
                lines[counter-2].append(nfe_intervals[z])
            
            lines.append([])
            lines[counter-1].append(m.__name__+'_'+f.__name__+'_OF')
            for z in range(0, len(ave_rep)):
                lines[counter-1].append(ave_rep[z])
           
            
        with open(dirpath+'/All_OF.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()  
###############################################################################
###############################################################################
#############################     OF REPRORT     ##############################
        
##########################       CSV_Full_Report      #########################
        dirpath = os.getcwd()
        os.chdir(dirpath)
        
        
        try:
            os.mkdir(dirpath+"/S-Output")
        except OSError:
            pass

        try:
            os.mkdir(dirpath+"/T-Output")
        except OSError:
            pass
        try:
            os.mkdir(dirpath+"/F-Output")
        except OSError:
            pass

        
        
        csvData=[['']]
        for n in range(0,n_run):
            csvData[0].append('NFE'+str(n+1))
            csvData[0].append('Run'+str(n+1))
        for n in range(0,n_run):
            csvData[0].append('Solution-Run'+str(n+1))
        csvData[0].append('Best')
        csvData[0].append('Mean')
        csvData[0].append('Worst')
        csvData[0].append('STD')
        csvData[0].append('NFE')
        
        file_name=os.path.basename(__file__)
        file_name=file_name.replace('.py','')
        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'+'.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()
               
###############################################################################        
#        for j in range(0,len(total_report[0]),10):
#            row=[j+1]
#            
#            for n in range(0,n_run):
#                row.append(total_nfe[n][j])
#                row.append(total_report[n][j])
#        
#            with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                      +'.csv', 'r') as readFile:
#                reader = csv.reader(readFile)
#                lines = list(reader)
#                lines.append(row)
#            with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                      +'.csv', 'w') as writeFile:
#                writer = csv.writer(writeFile)
#                writer.writerows(lines)
#            readFile.close()
#            writeFile.close()    
#            
#        
#            
#        for n in range(0,n_run):
#               j = len(total_report[0])-1
#               row=[j+1]
#               row.append(total_nfe[n][j])
#               row.append(total_report[n][j])
#        
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                      +'.csv', 'r') as readFile:
#                reader = csv.reader(readFile)
#                lines = list(reader)
#                lines.append(row)
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                     +'.csv', 'w') as writeFile:
#                writer = csv.writer(writeFile)
#                writer.writerows(lines)
#       readFile.close()
#        writeFile.close()        
#       
###############################################################################        
       
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                  +'.csv', 'r') as readFile:
#            reader = csv.reader(readFile)
#            lines = list(reader)
#           for j in range(0,dim):
#                for n in range(0,n_run):
#                   lines[j+1].append(total_solution[n][j])
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                  +'.csv', 'w') as writeFile:
#            writer = csv.writer(writeFile)
#           writer.writerows(lines)
#       readFile.close()
#       writeFile.close()    
#               
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                 +'.csv', 'r') as readFile:
#            reader = csv.reader(readFile)
#            lines = list(reader)
#            lines[1].append(thebest)            
#            lines[1].append(mean)
#            lines[1].append(theworst)
#            lines[1].append(std)
#            lines[1].append(NFE)
#        
#        with open(dirpath+"/T-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
#                  +'.csv', 'w') as writeFile:
#            writer = csv.writer(writeFile)
#            writer.writerows(lines)
#        readFile.close()
#        writeFile.close() 
       
###############################################################################
###############################################################################
##########################     CSV_OF_Only_Report     #########################
        csvData=[['']]
        for n in range(0,n_run):
            csvData[0].append('NFE'+str(n+1))
            csvData[0].append('Run'+str(n+1))

        
        with open(dirpath+"/F-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
                  +'-OF.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()
        for j in range(0,len(total_report[0]),10):
            row=[j+1]
            
            for n in range(0,n_run):
                row.append(total_nfe[n][j])
                row.append(total_report[n][j])
        
            with open(dirpath+"/F-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
                      +'-OF.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open(dirpath+"/F-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
                      +'-OF.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close() 
                      
        j = len(total_report[0])-1
        row=[j+1]
            
        for n in range(0,n_run):
                row.append(total_nfe[n][j])
                row.append(total_report[n][j])
        
        with open(dirpath+"/F-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
                      +'-OF.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
        with open(dirpath+"/F-Output"+'/'+str(algorithm_name)+'-'+str(function_name)+'-'+str(dim)+'D'\
                      +'-OF.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
        readFile.close()
        writeFile.close()         
###############################################################################
###############################################################################
##########################     CSV_Summary_Report     #########################
        csvData=[[''],['']]

        csvData[0].append('Best')
        csvData[0].append('Mean')
        csvData[0].append('Worst')
        csvData[0].append('STD')
        csvData[0].append('NFE')
        for p in alg_param:
            csvData[0].append(p[0])
        csvData[1].append(thebest)
        csvData[1].append(mean)
        csvData[1].append(theworst)
        csvData[1].append(std)
        csvData[1].append(NFE)
        for p in alg_param:
            csvData[1].append(p[1])

        with open(dirpath+'/S-Output'+'/'+str(algorithm_name)+'-'+\
                  str(function_name)+'-'+str(dim)+'D'+'-S.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()        
        









