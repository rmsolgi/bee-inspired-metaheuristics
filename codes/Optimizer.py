#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 21:59:33 2019

@author: mohammad Solgi
"""

import numpy as np
import os
import csv

import copy
import Function
import Algorithm



def run(A_name,F_name,n_run,dim):
    
    
    
        if F_name == "1": Func=Function.Ackley 
        elif F_name == "2": Func=Function.Griewank 
        elif F_name == "3": Func=Function.Michalewicz 
        elif F_name == "4": Func=Function.Restrigin 
        elif F_name == "5": Func=Function.Rosenbrock 
        elif F_name == "6": Func=Function.Schaffer 
        elif F_name == "7": Func=Function.Sphere 
        elif F_name == "8": Func=Function.Schwefel 
        elif F_name == "9": Func=Function.Weierstrass 
        
        
        
            
        if A_name == "1": Al=Algorithm.ABC
        elif A_name == "2": Al=Algorithm.BA
        elif A_name == "3": Al=Algorithm.BCO 
        elif A_name == "4": Al=Algorithm.HBeeGA 
        elif A_name == "5": Al=Algorithm.BS 
        elif A_name == "6": Al=Algorithm.BSO 
        elif A_name == "7": Al=Algorithm.FMBO 
        elif A_name == "8": Al=Algorithm.HBMO 
        elif A_name == "9": Al=Algorithm.MBO 
        elif A_name == "10": Al=Algorithm.QBE 
        
###############################################################################
###############################################################################
        n_run=int(n_run)
        dim=int(dim)
        total_report=[[None]*2]*n_run
        total_best=[[None]*1]*n_run
        total_solution=[[None]*1]*n_run
        function_name=Func.__name__
        algorithm_name=Al.__name__
        fun=Func()
    
###############################################################################
###############################################################################    
        model=Al(function=fun,lower_boundary=fun.L*dim,upper_boundary=fun.U*dim)
        alg_param=model.algorithm_parameters

        for n in range(0,n_run):
                fun.nfe=0
                
            
                model.run()
                NFE=fun.nfe
    
                
###############################################################################
############################################################################### 
                total_report[n][1]=copy.deepcopy(model.report)
                total_report[n][0]=copy.deepcopy(model.nfe)
                total_best[n]=copy.deepcopy(model.best)
                total_solution[n]=copy.deepcopy(model.solution)
                
                
                print("\nRun #"+str(n+1)+" "+str(algorithm_name)+"-"+\
                      str(function_name)+" is done.")

        
        
        bl=copy.deepcopy(total_best)
        bestnp=np.array(bl)
        std=np.std(bestnp)
        mean=np.mean(bestnp)
        thebest=np.min(bestnp)
        theworst=np.max(bestnp)
        
###############################################################################
###############################################################################    
        dirpath = os.getcwd()
        dirpath+='/Temporary'
        os.chdir(dirpath)    
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
        

        with open(dirpath+'/T-Output.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()    
###############################################################################        
        for j in range(0,len(total_report[0][0]),10):
            row=[j+1]
            
            for n in range(0,n_run):
                row.append(total_report[n][0][j])
                row.append(total_report[n][1][j])
        
            with open(dirpath+'/T-Output.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open(dirpath+'/T-Output.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close()    
            
        j = len(total_report[0][0])-1
        row=[j+1]
            
        for n in range(0,n_run):
               row.append(total_report[n][0][j])
               row.append(total_report[n][1][j])
        
        with open(dirpath+'/T-Output.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
        with open(dirpath+'/T-Output.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
        readFile.close()
        writeFile.close()      
###############################################################################        
       
        with open(dirpath+'/T-Output.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            for j in range(0,dim):
                for n in range(0,n_run):
                    lines[j+1].append(total_solution[n][j])
        with open(dirpath+'/T-Output.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()    
                
        with open(dirpath+'/T-Output.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[1].append(thebest)            
            lines[1].append(mean)
            lines[1].append(theworst)
            lines[1].append(std)
            lines[1].append(NFE)
        
        with open(dirpath+'/T-Output.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close() 
       
###############################################################################    
###############################################################################
##########################     CSV_OF_Only_Report     #########################
        csvData=[['']]
        for n in range(0,n_run):
            csvData[0].append('NFE'+str(n+1))
            csvData[0].append('Run'+str(n+1))

        
        with open(dirpath+'/F-Output.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()
        for j in range(0,len(total_report[0][0]),10):
            row=[j+1]
            
            for n in range(0,n_run):
                row.append(total_report[n][0][j])
                row.append(total_report[n][1][j])
        
            with open(dirpath+'/F-Output.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open(dirpath+'/F-Output.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close() 
                      
        j = len(total_report[0][0])-1
        row=[j+1]
            
        for n in range(0,n_run):
                row.append(total_report[n][0][j])
                row.append(total_report[n][1][j])
        
        with open(dirpath+'/F-Output.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
        with open(dirpath+'/F-Output.csv', 'w') as writeFile:
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

        with open(dirpath+'/S-Output.csv', 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()  
        
        
        
dirpath = os.getcwd()
os.chdir(dirpath)    
with open(dirpath+'/Input.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    lines = list(reader)    
run(lines[1][1],lines[2][1],lines[3][1],lines[4][1])

    
    
    
    
    
    
    