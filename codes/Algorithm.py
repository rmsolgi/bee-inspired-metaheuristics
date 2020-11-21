#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 00:51:29 2019

@author: Mohammad Solgi
"""

import random
import copy
import sys
import math



# ////////////////////////////////////////////////////////////////////////////            
#                                  ABC
# //////////////////////////////////////////////////////////////////////////// 
class ABC(object):
    

    def __init__(self,function,lower_boundary,upper_boundary,\
                 algorithm_parameters=[['num_iterate',10000],\
                                            ['num_bees',100],\
                                            ['limit',None],\
                                            ['employee',50],\
                                            ['scout',1]]):
        
        
        self.algorithm_parameters=algorithm_parameters

        self.__name__=ABC
        
        self.num_bees = self.algorithm_parameters[1][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        self.num_itt=self.algorithm_parameters[0][1]
        self.num_employees=int((self.algorithm_parameters[3][1]*self.num_bees)/100)
        self.num_onlookers=self.num_bees-self.num_employees
        self.num_scouts=self.algorithm_parameters[4][1]
        

        if (self.algorithm_parameters[2][1] == None):
            self.limit = self.num_employees * self.num_parameter
        else:
            self.limit = self.algorithm_parameters[2][1]
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upper boundary must be a list of the same length."
        
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        
        assert self.num_employees >= 2, \
        "Number of employees must be at least two."
        
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        

    def run(self):
        
        self.report=[]  
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_employees)
        self.objectives = [[None]*1]*(self.num_employees)
        self.normobj=[[None]*1]*(self.num_employees)
        self.cumprob=[[None]*1]*(self.num_employees)
        self.best = sys.float_info.max
        self.counter=[0]*self.num_employees
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# //////////////////////////////////////////////////////////////////////////// 
        for i in range(0, self.num_employees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.population[i]=v
#///////evaluate objective functions 
            self.objectives[i]=self.f.f(self.population[i])


# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):                  

            
 #///////select the best solution               
            index=self.objectives.index(min(self.objectives))
            self.solution=copy.deepcopy(self.population[index])
            self.best=copy.deepcopy(self.objectives[index])
            self.report.append(self.best)                 
            self.nfe.append(self.f.nfe)
            self.report_solution.append(self.solution)
            
        
            

# ////////////////////////////////////////////////////////////////////////////            
#                             Send employees
# ////////////////////////////////////////////////////////////////////////////
            for b in range (0,self.num_employees):
                employee=copy.deepcopy(self.population[b])
                j=random.randint(0,self.num_parameter-1)
                
                index=b
                while (index == b): index = random.randint(0, self.num_employees-1)

                employee[j]=self.population[b][j]+(random.random()-0.5)*2*\
                abs(self.population[b][j]-self.population[index][j])
                employee=self.check_violation(employee,j)

#///////evaluate objective functions                
                fit=self.f.f(employee)
                if fit<self.objectives[b]:
                    self.population[b]=copy.deepcopy(employee)
                    self.objectives[b]=copy.deepcopy(fit)
                    self.counter[b]=0
                else:
                    self.counter[b]+=1



# ////////////////////////////////////////////////////////////////////////////            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
            minobj=min(self.objectives)
            if minobj<0:
                for i in range(0,self.num_employees):
                    self.normobj[i]=self.objectives[i]+abs(minobj)
            else:
                for i in range(0,self.num_employees):
                    self.normobj[i]=self.objectives[i]
            maxnorm=max(self.normobj)
            for i in range(0,self.num_employees):
                self.normobj[i]=maxnorm-self.normobj[i]+1

# ////////////////////////////////////////////////////////////////////////////            
#                           Calculate probability
# ////////////////////////////////////////////////////////////////////////////                
                
            sum_normobj=sum(i for i in self.normobj)
            prob=0
            for i in range(0,self.num_employees):
                prob+=self.normobj[i]/sum_normobj
                self.cumprob[i]=prob

# ////////////////////////////////////////////////////////////////////////////            
#                             Send onlookers
# ////////////////////////////////////////////////////////////////////////////                    

            self.employees=copy.deepcopy(self.population)
            self.employees_fit=copy.deepcopy(self.objectives)

            for k in range (0,self.num_onlookers):
                rand=random.random()
                if rand <= self.cumprob[0]:
                    b=0
                else:
                    for i in range(1,self.num_employees):
                        if rand <= self.cumprob[i] and rand> self.cumprob[i-1]:
                            b=i
                
                onlooker=copy.deepcopy(self.population[b])
                j=random.randint(0,self.num_parameter-1)
                index=b
                while (index == b): index = random.randint(0, self.num_employees-1)
                onlooker[j]=self.population[b][j]+(random.random()-0.5)*2*\
                abs(self.population[b][j]-self.population[index][j])
                onlooker=self.check_violation(onlooker,j)
#///////evaluate objective functions
                fit=self.f.f(onlooker)
                if fit<self.employees_fit[b]:
                    self.employees[b]=copy.deepcopy(onlooker)
                    self.employees_fit[b]=copy.deepcopy(fit)
                    self.counter[b]=0
                else:
                    self.counter[b]+=1
            self.population=copy.deepcopy(self.employees)
            self.objectives=copy.deepcopy(self.employees_fit)



# ////////////////////////////////////////////////////////////////////////////            
#                             Send scout
# ////////////////////////////////////////////////////////////////////////////
            for k in range (0, self.num_scouts):
                index=self.counter.index(max(self.counter))
                if self.counter[index] > self.limit:
                    v=[]
                    for j in range(0,self.num_parameter):
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        v.append(r)
                    self.population[index]=v
    #///////evaluate objective functions
                    self.objectives[index]=self.f.f(self.population[index])
                    self.counter[index]=0

# ////////////////////////////////////////////////////////////////////////////            
#                                The End
# ////////////////////////////////////////////////////////////////////////////                
                
    def check_violation(self,solution,parameter):
        i=parameter
        if solution[i] > self.U[i]:
            solution[i]=copy.deepcopy(self.U[i])
        elif solution[i] < self.L[i]:
            solution[i]=copy.deepcopy(self.L[i])
        return solution
                
                
# ////////////////////////////////////////////////////////////////////////////            
#                                  BA
# ////////////////////////////////////////////////////////////////////////////             
            
class BA(object):
    def __init__(self,function,lower_boundary, upper_boundary,\
                         algorithm_parameters=[['num_iterate',500],\
                              ['population',500],\
                              ['elite_site',5],\
                              ['selected_sites',15],\
                              ['neighborhood_spread',0.01],\
                              ['bees_around_elite_points',50],\
                              ['bees_around_selected_points',30]]):
        
        self.__name__=BA

        
        self.algorithm_parameters=algorithm_parameters
         
        self.num_itt=self.algorithm_parameters[0][1]
        self.num_bees=self.algorithm_parameters[1][1]
        self.num_e=self.algorithm_parameters[2][1]
        self.num_b=self.algorithm_parameters[3][1]
        self.s=self.algorithm_parameters[4][1]
        self.num_en=self.algorithm_parameters[5][1]
        self.num_bn=self.algorithm_parameters[6][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upper boundary must be a list of the same length."
        
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        
        assert (self.num_e<=self.num_b), \
        "number of elits must be less than or equal to number of bests"
        
        
    def run(self):
        
        
        self.report=[] 
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)
        self.enbr=[[None]*1]*(self.num_en)
        self.obj_e=[[None]*1]*(self.num_en)
        self.bnbr=[[None]*1]*(self.num_bn)
        self.obj_b=[[None]*1]*(self.num_bn)        
        self.best = sys.float_info.max
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# ////////////////////////////////////////////////////////////////////////////        
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
            self.population[i]=v
#///////evaluate objective functions 
            self.objectives[i]=self.f.f(self.population[i])
            
        
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):
            
# ////////////////////////////////////////////////////////////////////////////            
#                        Sort population 
# ////////////////////////////////////////////////////////////////////////////           

            z = [self.population for _,self.population in \
             sorted(zip(self.objectives,self.population), key=lambda pair: pair[0])]
            self.population=copy.deepcopy(z)
       
            self.objectives.sort()
            
            self.best=self.objectives[0]
            self.solution=self.population[0]
            self.report.append(self.best)
            self.nfe.append(self.f.nfe)
            self.report_solution.append(self.solution)

# ////////////////////////////////////////////////////////////////////////////            
#                          Local search
# ////////////////////////////////////////////////////////////////////////////             
            for i in range(0,self.num_e):
                for n in range(0,self.num_en):
                    v=[]
                    for j in range(0,self.num_parameter):
                        r=self.population[i][j]-0.5*self.s+random.random()*self.s
                        v.append(r)
                    v=self.check_violation(v,j)
                    self.enbr[n]=v
 #///////evaluate objective functions 
                    self.obj_e[n]=self.f.f(self.enbr[n]) 
                if min(self.obj_e) < self.objectives[i]:
                    index=self.obj_e.index(min(self.obj_e))
                    self.population[i]=copy.deepcopy(self.enbr[index])
                    self.objectives[i]=copy.deepcopy(self.obj_e[index])
                
            for i in range(self.num_e,self.num_b):
                for n in range(0,self.num_bn):
                    v=[]
                    for j in range(0,self.num_parameter):
                        r=self.population[i][j]-0.5*self.s+random.random()*self.s
                        v.append(r)
                    v=self.check_violation(v,j)
                    self.bnbr[n]=v
 #///////evaluate objective functions 
                    self.obj_b[n]=self.f.f(self.bnbr[n]) 
                if min(self.obj_b) < self.objectives[i]:
                    index=self.obj_b.index(min(self.obj_b))
                    self.population[i]=copy.deepcopy(self.bnbr[index])      
                    self.objectives[i]=copy.deepcopy(self.obj_b[index])    
# ////////////////////////////////////////////////////////////////////////////            
#                          Global search
# ////////////////////////////////////////////////////////////////////////////             
            for i in range(self.num_b,self.num_bees):
                v=[]
                for j in range(0,self.num_parameter):
                    r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                    v.append(r)
                self.population[i]=v
#///////evaluate objective functions 
                self.objectives[i]=self.f.f(self.population[i])

# ////////////////////////////////////////////////////////////////////////////            
#                                The End
# ////////////////////////////////////////////////////////////////////////////
                
    def check_violation(self,solution,parameter):
        i=parameter
        if solution[i] > self.U[i]:
            solution[i]=copy.deepcopy(self.U[i])
        elif solution[i] < self.L[i]:
            solution[i]=copy.deepcopy(self.L[i])
        return solution                

# ////////////////////////////////////////////////////////////////////////////            
#                                  BCO
# ////////////////////////////////////////////////////////////////////////////

class BCO(object):
    def __init__(self,function, lower_boundary, upper_boundary,\
                 algorithm_parameters=[['NP',1],\
                                       ['num_iterate',10000],\
                                       ['num_bees',50],\
                                       ['chi',0.998],\
                                       ['gamma',0.001],\
                                       ['Nc',50]]):
        
        self.__name__=BCO
        
        self.algorithm_parameters=algorithm_parameters
        
        self.num_bees=self.algorithm_parameters[2][1]#+1 #(1 for the best solution)
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        self.num_itt=self.algorithm_parameters[1][1]
        self.NP=self.algorithm_parameters[0][1]
        self.chi=self.algorithm_parameters[3][1]
        self.gamma=self.algorithm_parameters[4][1]
        self.Nc=self.algorithm_parameters[5][1]

        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        
        
        
    def run(self):
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)
        self.normobj=[[None]*1]*(self.num_bees)
        self.prob=[[None]*1]*(self.num_bees)
        self.cumprob=[[None]*1]*(self.num_bees)
        self.d=[[None]*1]*(self.num_parameter)
        

        self.report=[]
        self.report_solution=[]
        self.nfe=[]

# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# ////////////////////////////////////////////////////////////////////////////        
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
            self.population[i]=v
#///////evaluate objective functions 
            self.objectives[i]=self.f.f(self.population[i])

        
            
 #///////select the best solution               
            
        
        index=self.objectives.index(min(self.objectives))
        self.solution=copy.deepcopy(self.population[index])
        self.best=copy.deepcopy(self.objectives[index])
        
        for j in range(0, self.num_parameter):
            self.d[j]=self.U[j]-self.L[j]

# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# ////////////////////////////////////////////////////////////////////////////        
        for t in range(0, self.num_itt):
            


    
# ////////////////////////////////////////////////////////////////////////////            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
            minobj=min(self.objectives)
            if minobj<0:
                index=self.objectives.index(min(self.objectives))
                for i in range(0,self.num_bees):
                    self.normobj[i]=self.objectives[i]+abs(self.objectives[index])
            else:
                for i in range(0,self.num_bees):
                    self.normobj[i]=self.objectives[i]
            maxnorm=max(self.normobj)
            for i in range(0,self.num_bees):
                self.normobj[i]=maxnorm-self.normobj[i]+1
            

# ////////////////////////////////////////////////////////////////////////////            
#                           Roulette Wheel
# ////////////////////////////////////////////////////////////////////////////                
                
            sum_normobj=sum(i for i in self.normobj)
            prob=0
            for i in range(0,self.num_bees):
                prob+=self.normobj[i]/sum_normobj
                self.cumprob[i]=prob
                
            rand=random.random()*max(self.cumprob)
            if rand <= self.cumprob[0]:
                index=0
            else:
                for i in range(1,self.num_bees):
                    if rand <= self.cumprob[i] and rand > self.cumprob[i-1]:
                        index=i
            
# ////////////////////////////////////////////////////////////////////////////            
#                           Set initial solutions
# ////////////////////////////////////////////////////////////////////////////
            for i in range(0,self.num_bees): 
                self.population[i]=copy.deepcopy(self.population[index])
                self.objectives[i]=copy.deepcopy(self.objectives[index])

# ////////////////////////////////////////////////////////////////////////////            
#                           Generate modified solutions
# ////////////////////////////////////////////////////////////////////////////
            NC=self.Nc

            for k in range (0,self.NP):

                for b in range(0,self.num_bees):
                    j=random.randint(0,self.num_parameter-1)
                    for i in range(0, NC):
#                        j=random.randint(0,self.num_parameter-1)
                            
                        if random.random()>0.5:

                            self.population[b][j]+=random.random()*\
                            min((self.d[j]),(self.U[j]-self.population[b][j]))
                        else:
                            self.population[b][j]-=random.random()*\
                            min((self.d[j]),(self.population[b][j]-self.L[j]))

#///////evaluate objective functions                                       
                for b in range(0,self.num_bees):
                    self.objectives[b]=self.f.f(self.population[b])
                    
                    
#///////select the best solution    
                self.old=self.best
                index=self.objectives.index(min(self.objectives))
                self.solution=copy.deepcopy(self.population[index])
                self.best=copy.deepcopy(self.objectives[index])
                self.report.append(self.best) 
                self.nfe.append(self.f.nfe)
                self.report_solution.append(self.solution)
                if self.old==self.best:
                    self.improve=False
                else:
                    self.improve=True

            
# ////////////////////////////////////////////////////////////////////////////            
#                               Backward pass
# ////////////////////////////////////////////////////////////////////////////
                    
                if k%NC == 0:
                    
                        
# ////////////////////////////////////////////////////////////////////////////
#                      Normalizing objective function
# ////////////////////////////////////////////////////////////////////////////               
                    minobj=min(self.objectives)
                    if minobj<0:
                        index=self.objectives.index(min(self.objectives))
                        for i in range(0,self.num_bees):
                            self.normobj[i]=self.objectives[i]+abs(self.objectives[index])
                    else:
                        for i in range(0,self.num_bees):
                            self.normobj[i]=self.objectives[i]
                    maxnorm=max(self.normobj)
                        
                    
                    for i in range(0,self.num_bees):
                        self.normobj[i]=maxnorm-self.normobj[i]+1
                        
# ////////////////////////////////////////////////////////////////////////////
#                             Loyalty decision
# ////////////////////////////////////////////////////////////////////////////                        
                    maxn=max(self.normobj)    
                    for i in range(0,self.num_bees):
                        self.prob[i]=math.exp(-(maxn-self.normobj[i])/maxn)

                    self.uncommitted=[]
                    self.recruiter=[]
                    for i in range(0,self.num_bees):
                        if random.random()>self.prob[i]:
                            self.uncommitted.append(i)
                        else:
                            self.recruiter.append(i)
    
# ////////////////////////////////////////////////////////////////////////////
#                        Recruitment of uncommitted bees
# ////////////////////////////////////////////////////////////////////////////                            
                    sum_normobj=0       
                    for i in range(0,len(self.recruiter)):
                        sum_normobj+=self.normobj[self.recruiter[i]]
                    prob=0
                    for i in range(0,len(self.recruiter)):
                        prob+=(self.normobj[self.recruiter[i]]/sum_normobj)
                        self.cumprob[i]=prob
                    for i in range(0,len(self.uncommitted)):
                        rand=random.random()
    
                        if rand <= self.cumprob[0]:
                            index=self.recruiter[0]
                        else:
                            for j in range(1,len(self.recruiter)):
                                if rand <= self.cumprob[j] and rand > self.cumprob[j-1]:
                                    index=self.recruiter[j]
        
                        self.population[self.uncommitted[i]]=copy.deepcopy\
                        (self.population[index])
                        self.objectives[self.uncommitted[i]]=copy.deepcopy\
                        (self.objectives[index])
                        

                for j in range(0,self.num_parameter):
                    self.d[j]=self.d[j]*self.chi
                if self.d[j]<self.gamma:
                    self.d[j]=(self.U[j]-self.L[j])

# ////////////////////////////////////////////////////////////////////////////
#                                    THE END
# //////////////////////////////////////////////////////////////////////////// 
                        
# ////////////////////////////////////////////////////////////////////////////            
#                                    HBeeGA
# ////////////////////////////////////////////////////////////////////////////                        
                    
class HBeeGA(object):
    def __init__(self,function, lower_boundary, upper_boundary,\
                         algorithm_parameters=[['num_iterate',1000],\
                              ['num_bees',100],\
                              ['mutation_probability',0.05],\
                              ['brood_caring_probability',0.5],\
                              ['spermatheca_size',30]]):

        self.__name__=HBeeGA
        

        
        self.algorithm_parameters=algorithm_parameters
        
        self.num_bees=self.algorithm_parameters[1][1]
        self.num_itt=self.algorithm_parameters[0][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.f=function
        self.m_p=self.algorithm_parameters[2][1]
        self.bc_p=self.algorithm_parameters[3][1]
        self.sc_size=self.algorithm_parameters[4][1]
        self.num_parameter=len(self.L)
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        assert (self.sc_size<=self.num_bees), \
        "speramtheca size must be smaller than the num_bees"
        assert (self.m_p>=0 and self.m_p<=1), \
        "mutation_probability must be in [0,1]"
        assert (self.bc_p>=0 and self.bc_p<=1), \
        "crossover_probability must be in [0,1]"
        
        

    def run(self):
        
        self.report=[] 
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)

        self.sc=[[None]*1]*(self.sc_size)
        self.best_f=None
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# //////////////////////////////////////////////////////////////////////////// 
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.population[i]=v

# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):                  

 #///////evaluate objective functions 
            for i in range (0, self.num_bees):
                self.objectives[i]=self.f.f(self.population[i])           
# ////////////////////////////////////////////////////////////////////////////            
#                   Sort population based on fitness
# ////////////////////////////////////////////////////////////////////////////             
           
            z = [self.population for _,self.population in \
            sorted(zip(self.objectives,self.population), key=lambda pair: pair[0])]
            self.population = copy.deepcopy(z)
            self.objectives.sort()
            
           
# ////////////////////////////////////////////////////////////////////////////            
#                   Selection of best and worst solution
# ////////////////////////////////////////////////////////////////////////////
            index=self.objectives.index(max(self.objectives))
            self.worst_f = self.objectives[index]
            
            if self.best_f==None:
                self.best_f = self.objectives[0]
                self.best_P = copy.deepcopy(self.population[0])
                self.population.remove(self.population[0])
                self.objectives.remove(self.objectives[0]) 
                self.old_f = self.best_f
                self.old_P = copy.deepcopy(self.best_P)

            
            
            elif self.objectives[0] < self.best_f:
                self.old_f = self.best_f
                self.old_P = copy.deepcopy(self.best_P)
            
                self.best_f = self.objectives[0]
                self.best_P = copy.deepcopy(self.population[0])
                self.population.remove(self.population[0])
                self.objectives.remove(self.objectives[0]) 
 
            self.report.append(self.best_f)
            self.nfe.append(self.f.nfe)
            self.best=self.best_f
            self.solution=self.best_P
            self.report_solution.append(self.solution)
# ////////////////////////////////////////////////////////////////////////////            
#                              Mating fly
# ////////////////////////////////////////////////////////////////////////////
            self.dp_size=len(self.population)
            self.sum=0
            self.sigmaf = [[None]*1]*self.dp_size
            self.prob = [[None]*1]*self.dp_size
            for i in range (0,self.dp_size):
                dd = (self.objectives[i]-self.best_f)/(self.worst_f - self.best_f)
                self.sigmaf[i] = math.exp(dd)
                self.sum+=self.sigmaf[i]
                
            for i in range(0,self.sc_size):
                self.prob[0]=self.sigmaf[0]/self.sum
                for k in range(1,len(self.population)):
                    self.prob[k]=(self.sigmaf[k]/self.sum)+self.prob[k-1]
                rand = random.random()
                if rand<=self.prob[0]:
                    self.sc[i]=self.population[0]
                    del self.population[0]
                    self.sum-=self.sigmaf[0]
                    del self.prob[0]
                    del self.sigmaf[0]
                
                else:
                    for k in range(1,len(self.population)):
                        if rand>self.prob[k-1] and rand<=self.prob[k]:
                            self.sc[i]=self.population[k]
                            del self.population[k]
                            self.sum-=self.sigmaf[k]
                            del self.sigmaf[k]
                            del self.prob[k]

# ////////////////////////////////////////////////////////////////////////////            
#                               Reproduction
# ////////////////////////////////////////////////////////////////////////////            

            self.population = [[None]*1]*self.num_bees
            self.objectives = [[None]*1]*self.num_bees
            
           
            
            for i in range(0,int(self.num_bees*0.5)):
        
                c = random.randint(0,self.sc_size-1)
                self.population[i]=copy.deepcopy(self.best_P)
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=0.5:
                        self.population[i][j]=copy.deepcopy(self.sc[c][j])
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=self.m_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.population[i][j]=r
                
            for i in range (int(self.num_bees*0.5), self.num_bees):
                self.population[i]=copy.deepcopy(self.best_P)
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=self.m_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.population[i][j]=r
                
# ////////////////////////////////////////////////////////////////////////////            
#                              Brood caring
# ////////////////////////////////////////////////////////////////////////////                    
            for i in range (0,self.num_bees):
                for j in range(0, self.num_parameter):
                    rand=random.random()
                    if rand <= self.bc_p:
                        if self.best_P[j]>self.old_P[j]:
                            r=self.best_P[j]+random.random() * (self.U[j] -\
                                         self.best_P[j])
                            self.population[i][j]=r
                            
                        elif self.best_P[j]<self.old_P[j]:
                            r=self.L[j]+random.random() * (self.best_P[j] -\
                                    self.L[j])
                            self.population[i][j]=r
                            
                        elif self.best_P[j]==self.old_P[j] and\
                        self.best_P[j]>self.population[i][j]:
                            
                            r=self.population[i][j]+random.random() *\
                            (self.U[j] - self.population[i][j])
                            self.population[i][j]=r
                            
                        elif self.best_P[j]==self.old_P[j] and\
                        self.best_P[j]<self.population[i][j]:
                            r=self.L[j]+random.random() *\
                            (self.population[i][j] - self.L[j])
                            self.population[i][j]=r
                            
# ////////////////////////////////////////////////////////////////////////////            
#                                  BS
# ////////////////////////////////////////////////////////////////////////////
class BS(object):
    def __init__(self, function,lower_boundary, upper_boundary,\
                 algorithm_parameters=[['num_function_evaluation',500000],\
                              ['global_population_size',100],\
                              ['local_population_size',100],\
                              ['global_mutation_probability',0.05],\
                              ['local_mutation_probability',0.5],\
                              ['migration_threshold',5],\
                              ['num_superior_chromosomes',3],\
                              ['superior_chromosomes_threshold',20],\
                              ['crossover_probability',0.5],\
                              ['parents_portion',0.3],\
                              ['alpha',0.4],\
                              ['beta',0.4]]):
       
        self.__name__=BS
        
        
        
        self.algorithm_parameters=algorithm_parameters
                 
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        self.g_pop_s=self.algorithm_parameters[1][1]
        self.l_pop_s=self.algorithm_parameters[2][1]
        self.g_mut_p=self.algorithm_parameters[3][1]
        self.l_mut_p=self.algorithm_parameters[4][1]
        self.m_t=self.algorithm_parameters[5][1]
        self.num_sc=self.algorithm_parameters[6][1]
        self.sc_t=self.algorithm_parameters[7][1]
        self.num_g_parents=int(self.algorithm_parameters[9][1]*self.g_pop_s)
        self.num_l_parents=int(self.algorithm_parameters[9][1]*self.l_pop_s)
        self.pc=self.algorithm_parameters[8][1]
        self.total_NFE=self.algorithm_parameters[0][1]
        self.alpha=self.algorithm_parameters[10][1]
        self.beta=self.algorithm_parameters[11][1]
        
        children=self.g_pop_s-self.num_g_parents
        if children % 2 != 0:
            self.g_pop_s+=1
        children=self.l_pop_s-self.num_l_parents
        if children % 2 != 0:
            self.l_pop_s+=1
        self.l_condition=True
        self.report=[]
        self.report_solution=[]
        self.solution=[]
        self.nfe=[]
        
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upper boundary must be a list of the same length."
        
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        
        assert (self.num_sc <= self.g_pop_s), \
        "number of superior chromosomes must be less than or equal to global "\
        +"population size"
        
        assert (self.g_mut_p<=1 and self.g_mut_p>=0), \
        "global_mutation_probability must be in range [0,1]"
        
        assert (self.l_mut_p<=1 and self.l_mut_p>=0), \
        "local_mutation_probability must be in range [0,1]"
        
        assert (self.num_g_parents<self.g_pop_s), \
        "parents_portion must be in range [0,1)"
        
        assert (self.num_l_parents<self.l_pop_s), \
        "parents_portion must be in range [0,1)"
        
    def run(self):

        self.global_GA()

#        self.l_condition=False
        if self.l_condition==True:
            
            self.Local_search()
        
        
        
    def global_GA(self):
        
        
        
        self.g_population = [[None]*1]*(self.g_pop_s)
        self.g_objectives = [[None]*1]*(self.g_pop_s)
        self.g_normobj=[[None]*1]*(self.g_pop_s)
        self.g_cumprob=[[None]*1]*(self.g_pop_s)
        self.best = sys.float_info.max
        self.g_parents=[[None]*1]*(self.num_g_parents)
        self.g_parents_obj=[[None]*1]*(self.num_g_parents)
        self.superiors=[]
        self.superiors_obj=[]
        
        
        
        
        
        self.msc=0
        self.sc_counter=0
        self.INFE=0
        
# ////////////////////////////////////////////////////////////////////////////            
#                 Initiate first global GA population randomly
# ////////////////////////////////////////////////////////////////////////////        
        for i in range(0, self.g_pop_s):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.g_population[i]=v
#///////evaluate objective functions 
            self.g_objectives[i]=self.f.f(self.g_population[i])
            self.INFE+=1
            

#///////select the best solution               
        index=self.g_objectives.index(min(self.g_objectives))

        self.solution=copy.deepcopy(self.g_population[index])
        self.best=copy.deepcopy(self.g_objectives[index])
        self.report.append(self.best) 
        self.nfe.append(self.f.nfe)
        self.report_solution.append(self.solution)
# ////////////////////////////////////////////////////////////////////////////            
#                        Start golbal GA itteration 
# ////////////////////////////////////////////////////////////////////////////
        self.g_condition=True
        
        while (self.g_condition):
            
                
    
    

# ////////////////////////////////////////////////////////////////////////////            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
            minobj=min(self.g_objectives)
            if minobj<0:
                for i in range(0,self.g_pop_s):
                    self.g_normobj[i]=self.g_objectives[i]+abs(minobj)
            else:
                for i in range(0,self.g_pop_s):
                    self.g_normobj[i]=self.g_objectives[i]
            maxnorm=max(self.g_normobj)
            for i in range(0,self.g_pop_s):
                self.g_normobj[i]=maxnorm-self.g_normobj[i]+1 
                
# ////////////////////////////////////////////////////////////////////////////            
#                           Calculate probability
# ////////////////////////////////////////////////////////////////////////////                
                
            sum_normobj=sum(i for i in self.g_normobj)
            prob=0
            for i in range(0,self.g_pop_s):
                prob+=self.g_normobj[i]/sum_normobj
                self.g_cumprob[i]=prob
                
                
# ////////////////////////////////////////////////////////////////////////////            
#                             GA parents selection
# ////////////////////////////////////////////////////////////////////////////                    

            for k in range (0,self.num_g_parents):
                rand=random.random()
                if rand <= self.g_cumprob[0]:
                    b=0
                else:
                    for i in range(1,self.g_pop_s):
                        if rand <= self.g_cumprob[i] and rand> self.g_cumprob[i-1]:
                            b=i
                self.g_parents[k]=copy.deepcopy(self.g_population[b])
                self.g_parents_obj[k]=copy.deepcopy(self.g_objectives[b])

            self.effective_parents=[]
            parent_num=0

            while(parent_num==0):
                for k in range (0,self.num_g_parents):
                    rand=random.random()
                    if rand < self.pc:
                        self.effective_parents.append(self.g_parents[k])
                
                parent_num=len(self.effective_parents)

                           
# ////////////////////////////////////////////////////////////////////////////            
#                            New GA generation
# //////////////////////////////////////////////////////////////////////////// 
            for k in range (0,self.num_g_parents):
                self.g_population[k]=copy.deepcopy(self.g_parents[k])
                self.g_objectives[k]=copy.deepcopy(self.g_parents_obj[k])
                
            for k in range(self.num_g_parents,self.g_pop_s,2):
                
                rand1=random.randint(0,parent_num-1)
                rand2=random.randint(0,parent_num-1)
                parent1=copy.deepcopy(self.effective_parents[rand1])
                parent2=copy.deepcopy(self.effective_parents[rand2])
                child1=copy.deepcopy(parent1)
                child2=copy.deepcopy(parent2)
                
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand < 0.5:
                        child1[j]=copy.deepcopy(parent2[j])
                        child2[j]=copy.deepcopy(parent1[j])
                        
                self.g_population[k]=copy.deepcopy(child1)
                self.g_population[k+1]=copy.deepcopy(child2)
                
            for k in range (self.num_g_parents,self.g_pop_s):
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand <= self.g_mut_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.g_population[k][j]=r
#///////evaluate objective functions                        
            for k in range(self.num_g_parents,self.g_pop_s):
                self.g_objectives[k]=self.f.f(self.g_population[k])
                self.INFE+=1

# ////////////////////////////////////////////////////////////////////////////            
#                   Check global search termination criteria
# ////////////////////////////////////////////////////////////////////////////
                         
                        
#///////select the best solution               
            index=self.g_objectives.index(min(self.g_objectives))
            self.report.append(self.g_objectives[index]) 
            self.nfe.append(self.f.nfe)
            self.report_solution.append(self.g_population[index])
            
            if self.g_objectives[index] < self.best:
                
                self.solution=copy.deepcopy(self.g_population[index])
                self.best=copy.deepcopy(self.g_objectives[index])
                self.msc=0
            else:
                self.msc+=1
                if self.msc==self.sc_t:
                    self.superiors.append(self.solution)
                    self.superiors_obj.append(self.best)
                    self.sc_counter+=1
                    self.msc=0
                    if self.sc_counter==self.num_sc:
                        
                        self.sc_counter=0
                        self.g_condition=False
            
            
            if self.INFE >= self.total_NFE:
                self.g_condition=False
                self.l_condition=False
                print("Algorithm is terminated in Global search due to NFE"+\
                      ". Select smaller superior chromosomes threshold.")
                
#                localsearch
#                self.superiors=[]
#                self.superiors.obj=[]
#before local search in def run function check the l_condition

                
                
    def Local_search(self):
        
        print("Local search is run")
        self.l_populations=[[None]*1]*(self.num_sc)
        self.l_objectives=[[None]*1]*(self.num_sc)
        self.l_best=[sys.float_info.max]*(self.num_sc)
        self.l_solution=[[None]*1]*(self.num_sc)
        self.l_report=[[None]*1]*(self.num_sc)
        self.simplex_c=[[None]*1]*(self.num_sc)
        for i in range (0,self.num_sc):
            self.l_populations[i]=[[None]*1]*(self.l_pop_s)
            self.l_objectives[i]=[[None]*1]*(self.l_pop_s)


        self.l_normobj=[[None]*1]*(self.l_pop_s)
        self.l_cumprob=[[None]*1]*(self.l_pop_s)
        self.l_parents=[[None]*1]*(self.num_l_parents)
        self.l_parents_obj=[[None]*1]*(self.num_l_parents)
        self.mi=0
        
        for s in range (0,self.num_sc):
            
            
# ////////////////////////////////////////////////////////////////////////////            
#                 Initiate first local search population randomly
# ////////////////////////////////////////////////////////////////////////////        
            self.l_populations[s][0]=copy.deepcopy(self.superiors[s])
            self.l_objectives[s][0]=copy.deepcopy(self.superiors_obj[s])
            
            for i in range(1, self.l_pop_s):
                v=[]
                for j in range(0,self.num_parameter):
                    r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                    v.append(r)
                    self.l_populations[s][i]=v

            
# ////////////////////////////////////////////////////////////////////////////            
#                           Concentrated Crossover
# ////////////////////////////////////////////////////////////////////////////
            
            for k in range(1,self.l_pop_s):
                child=copy.deepcopy(self.l_populations[s][k])
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand < 0.5:
                        child[j]=copy.deepcopy(self.l_populations[s][0][j])
                
                self.l_populations[s][k]=copy.deepcopy(child) 
#///////evaluate objective functions 
                self.l_objectives[s][k]=self.f.f(self.l_populations[s][k])
                self.INFE+=1

# ////////////////////////////////////////////////////////////////////////////            
#                           Check termination criteria
# ////////////////////////////////////////////////////////////////////////////
#///////select the best solution               
            index=self.l_objectives[s].index(min(self.l_objectives[s]))
        
            self.l_solution[s]=copy.deepcopy(self.l_populations[s][index])
            self.l_best[s]=copy.deepcopy(self.l_objectives[s][index])
            self.l_report[s]=[(self.l_best[s])] 
            


        index=self.l_best.index(min(self.l_best))
        self.report.append(self.l_best[index])
        self.nfe.append(self.f.nfe)
        self.report_solution.append(self.l_solution[index])
        if self.l_best[index] < self.best:
            self.solution=copy.deepcopy(self.l_solution[index])
            self.best=self.l_best[index]
            


        if self.INFE>=self.total_NFE:
            self.l_condition=False

            
# ////////////////////////////////////////////////////////////////////////////            
#                       Local Search and simplex loop
# ////////////////////////////////////////////////////////////////////////////            
            
        while (self.l_condition):
            
            
            
            for s in range(0,self.num_sc):

# ////////////////////////////////////////////////////////////////////////////            
#                     select three solutions for simplex
# ////////////////////////////////////////////////////////////////////////////

                temp_population=copy.deepcopy(self.l_populations[s])
                temp_objective=copy.deepcopy(self.l_objectives[s])
                
                

                z = [[None]*1]*self.l_pop_s
                z = [temp_population for _,temp_population in \
             sorted(zip(temp_objective,temp_population), key=lambda pair: pair[0])]
                temp_population=copy.deepcopy(z)
                temp_objective.sort()
              

                self.simplex_c[s]=[]
              
                for i in range(0,3):
                    v=copy.deepcopy(temp_population[i])
                    self.simplex_c[s].append(v)
                
                    
# ////////////////////////////////////////////////////////////////////////////            
#                                 selection
            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
                minobj=min(temp_objective)
                if minobj<0:
                    for i in range(0,self.l_pop_s):
                        self.l_normobj[i]=temp_objective[i]+abs(minobj)
                else:
                    for i in range(0,self.l_pop_s):
                        self.l_normobj[i]=temp_objective[i]
                maxnorm=max(self.l_normobj)
                for i in range(0,self.l_pop_s):
                    self.l_normobj[i]=maxnorm-self.l_normobj[i]+1         
                
            
# ////////////////////////////////////////////////////////////////////////////            
#                           Calculate probability
# ////////////////////////////////////////////////////////////////////////////                
                
                sum_normobj=sum(i for i in self.l_normobj)
                prob=0
                for i in range(0,self.l_pop_s):
                    prob+=self.l_normobj[i]/sum_normobj
                    self.l_cumprob[i]=prob
                                
# ////////////////////////////////////////////////////////////////////////////            
#                             GA parents selection
# ////////////////////////////////////////////////////////////////////////////                    
                self.l_parents[0]=self.l_solution[s]
                self.l_parents_obj[0]=self.l_best[s]
                
                
                
                for k in range (1,self.num_l_parents):
                    rand=random.random()
                    if rand <= self.l_cumprob[0]:
                        b=0
                    else:
                        for i in range(1,self.l_pop_s):
                            if rand <= self.l_cumprob[i] and rand> self.l_cumprob[i-1]:
                                b=i
                    self.l_parents[k]=copy.deepcopy(temp_population[b])
                    self.l_parents_obj[k]=copy.deepcopy(temp_objective[b])

                self.effective_parents=[]
                parent_num=0
                while(parent_num==0):
                    for k in range (0,self.num_l_parents):
                        rand=random.random()
                        if rand < self.pc:
                            self.effective_parents.append(self.l_parents[k])
                    parent_num=len(self.effective_parents)

# ////////////////////////////////////////////////////////////////////////////            
#                            New GA generation
# //////////////////////////////////////////////////////////////////////////// 
                for k in range (0,self.num_l_parents):
                    temp_population[k]=copy.deepcopy(self.l_parents[k])
#population is not filled with childred since two places are needed for solutions 
#will be generated by simplex
                for k in range(self.num_l_parents,self.l_pop_s-2,2):
                    rand1=random.randint(0,parent_num-1)
                    rand2=random.randint(0,parent_num-1)
                    parent1=copy.deepcopy(self.effective_parents[rand1])
                    parent2=copy.deepcopy(self.effective_parents[rand2])
                    child1=copy.deepcopy(parent1)
                    child2=copy.deepcopy(parent2)
                    
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand < 0.5:
                            child1[j]=copy.deepcopy(parent2[j])
                            child2[j]=copy.deepcopy(parent1[j])
                            
                    temp_population[k]=copy.deepcopy(child1)
                    temp_population[k+1]=copy.deepcopy(child2)

                
                        
                for k in range (self.num_l_parents,self.l_pop_s-2):
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand <= self.l_mut_p:
                            r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                            temp_population[k][j]=r
                            
                self.l_populations[s]=copy.deepcopy(temp_population)

                    
                    
# ////////////////////////////////////////////////////////////////////////////            
#                                Migration
# ////////////////////////////////////////////////////////////////////////////                    

            self.mi+=1
            if self.mi==self.m_t:

                for s in range(0,self.num_sc-1):
                    rand1=random.randint(0,self.l_pop_s-3)
                    rand2=random.randint(0,self.l_pop_s-3)
                    temp=self.l_populations[s+1][rand2]
                    self.l_populations[s+1][rand2]=copy.deepcopy(self.l_populations[s][rand1])
                    self.l_populations[s][rand1]=copy.deepcopy(temp)
                    
                    temp=self.l_objectives[s+1][rand2]
                    self.l_objectives[s+1][rand2]=copy.deepcopy(self.l_objectives[s][rand1])
                    self.l_objectives[s][rand1]=copy.deepcopy(temp)
                    
                    
                    
                rand1=random.randint(0,self.l_pop_s-3)
                rand2=random.randint(0,self.l_pop_s-3)
                temp=self.l_populations[0][rand2]
                self.l_populations[0][rand2]=copy.deepcopy(self.l_populations[self.num_sc-1][rand1])
                self.l_populations[self.num_sc-1][rand1]=copy.deepcopy(temp)
                
                temp=self.l_objectives[0][rand2]
                self.l_objectives[0][rand2]=copy.deepcopy(self.l_objectives[self.num_sc-1][rand1])
                self.l_objectives[self.num_sc-1][rand1]=copy.deepcopy(temp)                
                
            
# ////////////////////////////////////////////////////////////////////////////            
#                                Simplex
# ////////////////////////////////////////////////////////////////////////////
            for s in range (0,self.num_sc):
                x0=[[None]*1]*(self.num_parameter)
                xref=[[None]*1]*(self.num_parameter)
                xcount=[[None]*1]*(self.num_parameter)
                x1=self.simplex_c[s][0]
                x2=self.simplex_c[s][1]
                x3=self.simplex_c[s][2]
                
                for j in range (0,self.num_parameter):
                    v=(x1[j]+x2[j])/2
                    x0[j]=copy.deepcopy(v)
                    v=(1+self.alpha)*x0[j]-self.alpha*x3[j]
                    xref[j]=copy.deepcopy(v)
                    v=(1-self.beta)*x0[j]+self.beta*x3[j]
                    xcount[j]=copy.deepcopy(v)
                for j in range (0,self.num_parameter):    
                    xref=self.check_violation(xref,j)
                    xcount=self.check_violation(xcount,j)
                
                self.l_populations[s][self.l_pop_s-2]=copy.deepcopy(xref)
                self.l_populations[s][self.l_pop_s-1]=copy.deepcopy(xcount)

                
#///////evaluate objective functions                        
                for k in range(self.num_l_parents,self.l_pop_s):
                    self.l_objectives[s][k]=self.f.f(self.l_populations[s][k])
                    self.INFE+=1 
                    
                  
# ////////////////////////////////////////////////////////////////////////////            
#                           Check termination criteria
# ////////////////////////////////////////////////////////////////////////////                    
#///////select the best solution               
                index=self.l_objectives[s].index(min(self.l_objectives[s]))
        
                self.l_solution[s]=copy.deepcopy(self.l_populations[s][index])
                self.l_best[s]=copy.deepcopy(self.l_objectives[s][index])
                self.l_report[s].append(self.l_best[s])  
        
       
            index=self.l_best.index(min(self.l_best))
            self.report.append(self.l_best[index])
            self.nfe.append(self.f.nfe)
            self.report_solution.append(self.l_solution[index])
            if self.l_best[index]<self.best:
                
                self.solution=copy.deepcopy(self.l_solution[index])
                self.best=self.l_best[index]
            

        
            if self.INFE>=self.total_NFE:
                self.l_condition=False                    
                
# ////////////////////////////////////////////////////////////////////////////            
#                                The End
# ////////////////////////////////////////////////////////////////////////////                
                        
    def check_violation(self,solution,parameter):
        i=parameter
        if solution[i] > self.U[i]:
            solution[i]=copy.deepcopy(self.U[i])
        elif solution[i] < self.L[i]:
            solution[i]=copy.deepcopy(self.L[i])
        return solution                 
                        
                        
# ////////////////////////////////////////////////////////////////////////////            
#                                  BSO
# ////////////////////////////////////////////////////////////////////////////                
class BSO(object):
    def __init__(self,function, lower_boundary, upper_boundary,\
                 algorithm_parameters=[['num_iterate',5000],\
                              ['num_bees',100],\
                              ['num_scouts',4],\
                              ['num_foragers',48],\
                              ['omega_e',0.5],\
                              ['omega_b',0.5],\
                              ['tau_max',1],\
                              ['tau_min',0.1]]):

        self.__name__=BSO


        self.algorithm_parameters=algorithm_parameters
        
        self.num_bees=self.algorithm_parameters[1][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        self.num_itt=self.algorithm_parameters[0][1]
        self.num_scouts=self.algorithm_parameters[2][1]
        self.num_foragers=self.algorithm_parameters[3][1]
        self.omega_e=self.algorithm_parameters[4][1]
        self.omega_b=self.algorithm_parameters[5][1]
        self.tau_max=self.algorithm_parameters[6][1]
        self.tau_min=self.algorithm_parameters[7][1]
        self.tau_s=(self.tau_max-self.tau_min)/(self.num_itt)

        
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.omega_e >= 0 and self.omega_e<=1), \
        "Omega_e must be selected between 0 and 1."
        assert (self.omega_b >= 0 and self.omega_b<=1), \
        "Omega_b must be selected between 0 and 1."
        assert (self.num_foragers+self.num_scouts < self.num_bees), \
        "Num_scouts and Num_foragers must be smaller than Num_bees."        
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary" 
        assert (self.tau_max <= 1), \
        "Tau must be betwween zero and one" 
        assert (self.tau_max >= self.tau_min), \
        "tau_max must be greater than or equal to tau_min" 
        
    def run(self):
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)
        self.normobj=[[None]*1]*(self.num_foragers)
        self.cumprob=[[None]*1]*(self.num_foragers)
        self.b_pop=[[None]*1]*(self.num_bees)
        self.b_obj = [[None]*1]*(self.num_bees)
        self.best=sys.float_info.max
        self.report=[]
        self.report_solution=[]
        self.nfe=[]
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# ////////////////////////////////////////////////////////////////////////////
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
            self.population[i]=copy.deepcopy(v)
            self.b_pop[i]=copy.deepcopy(v)
#///////evaluate objective functions 
            self.objectives[i]=self.f.f(self.population[i])
            self.b_obj[i]=copy.deepcopy(self.objectives[i])

                  
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):
            
# ////////////////////////////////////////////////////////////////////////////            
#                        Sort population 
# ////////////////////////////////////////////////////////////////////////////           

            z = [self.population for _,self.population in \
             sorted(zip(self.objectives,self.population), key=lambda pair: pair[0])]
            self.population=copy.deepcopy(z)
            z = [self.b_pop for _,self.b_pop in \
             sorted(zip(self.objectives,self.b_pop), key=lambda pair: pair[0])]
            self.b_pop=copy.deepcopy(z)
            z = [self.b_obj for _,self.b_obj in \
             sorted(zip(self.objectives,self.b_obj), key=lambda pair: pair[0])]
            self.b_obj=copy.deepcopy(z)         
            self.objectives.sort()
            

# ////////////////////////////////////////////////////////////////////////////            
#                      select the best food source position
# ////////////////////////////////////////////////////////////////////////////             
#            self.solution=copy.deepcopy(self.population[0])
#            self.best=copy.deepcopy(self.objectives[0])
#            self.report.append(self.best) 

            
            for i in range (0,self.num_foragers):
                if self.b_obj[i]>self.objectives[i]:
                    self.b_pop[i]=copy.deepcopy(self.population[i])
                    self.b_obj[i]=copy.deepcopy(self.objectives[i])
                if self.best>self.b_obj[i]:
                    self.best=copy.deepcopy(self.b_obj[i])
                    self.solution=copy.deepcopy(self.b_pop[i])
            
            index=self.b_obj.index(min(self.b_obj))
            self.report.append(self.b_obj[index]) 
            self.nfe.append(self.f.nfe)
            self.report_solution.append(self.b_pop[index])
                
# ////////////////////////////////////////////////////////////////////////////            
#                           Experienced foragers
# ////////////////////////////////////////////////////////////////////////////                    
                    
            for i in range(0,self.num_foragers):
                v=[]
                for j in range(0,self.num_parameter):
                    r=self.population[i][j]+self.omega_b*random.random()*\
                    (self.b_pop[i][j]-self.population[i][j])+self.omega_e*\
                    random.random()*(self.solution[j]-self.population[i][j])
                    r=self.check_violation(r,j)
                    v.append(r)
                    
                self.population[i]=copy.deepcopy(v)
                
#///////evaluate objective functions 
                self.objectives[i]=self.f.f(self.population[i])
                
# ////////////////////////////////////////////////////////////////////////////            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
            minobj=min(self.objectives[:self.num_foragers])
            if minobj<0:
                for i in range(0,self.num_foragers):
                    self.normobj[i]=self.objectives[i]+abs(minobj)
            else:
                for i in range(0,self.num_foragers):
                    self.normobj[i]=self.objectives[i]
            maxnorm=max(self.normobj)
            for i in range(0,self.num_foragers):
                self.normobj[i]=maxnorm-self.normobj[i]+1


# ////////////////////////////////////////////////////////////////////////////            
#                           Calculate probability
# ////////////////////////////////////////////////////////////////////////////                
                
            sum_normobj=sum(i for i in self.normobj)
            prob=0
            for i in range(0,self.num_foragers):
                prob+=self.normobj[i]/sum_normobj
                self.cumprob[i]=prob 


# ////////////////////////////////////////////////////////////////////////////            
#                                Onlookers
# //////////////////////////////////////////////////////////////////////////// 
            for i in range(self.num_foragers, self.num_bees-self.num_scouts):
                rand=random.random()
                if rand <= self.cumprob[0]:
                    e=0
                else:
                    for b in range(1,self.num_foragers):
                        if rand <= self.cumprob[b] and rand> self.cumprob[b-1]:
                            e=i
                v=[]
                for j in range (0, self.num_parameter):
                    r=self.population[i][j]+self.omega_e*random.random()*\
                    (self.population[e][j]-self.population[i][j])
                    r=self.check_violation(r,j)
                    v.append(r)
                
                self.population[i]=copy.deepcopy(v) 
                
#///////evaluate objective functions 
                self.objectives[i]=self.f.f(self.population[i])
                
# ////////////////////////////////////////////////////////////////////////////            
#                                Scouts
# ////////////////////////////////////////////////////////////////////////////            
            for i in range (self.num_bees-self.num_scouts, self.num_bees):
                v=[]
                for j in range(0,self.num_parameter):
                    r=self.population[i][j]+(random.random()-0.5)*2*\
                    (self.tau_max-(self.tau_s*t)*(self.U[j]-self.L[j]))
                    r=self.check_violation(r,j)
                    v.append(r)
                self.population[i]=copy.deepcopy(v)
                
#///////evaluate objective functions 
                self.objectives[i]=self.f.f(self.population[i])                    
                
                   
# ////////////////////////////////////////////////////////////////////////////            
#                                The End
# ////////////////////////////////////////////////////////////////////////////                 
                                     
    def check_violation(self,solution,parameter):
        q=parameter
        if solution > self.U[q]:
            solution=copy.deepcopy(self.U[q])
        elif solution < self.L[q]:
            solution=copy.deepcopy(self.L[q])
        return solution                     
                                
            
# ////////////////////////////////////////////////////////////////////////////            
#                                  FMBO
# ////////////////////////////////////////////////////////////////////////////
            
class FMBO(object):
    def __init__(self,function,lower_boundary, upper_boundary,\
                 algorithm_parameters=[['num_iterate',5000],\
                              ['num_bees',100],\
                              ['mutation_probability',0.3],\
                              ['queen_speed_parameter',0.99],\
                              ['spermatheca_size',4],\
                              ['energy_decay_rate',0.001]]):


        self.__name__=FMBO
        

        self.algorithm_parameters=algorithm_parameters
        
        
        self.num_bees=self.algorithm_parameters[1][1]
        self.num_itt=self.algorithm_parameters[0][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.f=function
        self.m_p=self.algorithm_parameters[2][1]
        self.alpha=self.algorithm_parameters[3][1]
        self.sc_size=self.algorithm_parameters[4][1]
        self.num_parameter=len(self.L)
        
        if self.algorithm_parameters[5][1] == None:
            self.omega=1/(100*self.sc_size)
        else:
            self.omega=self.algorithm_parameters[5][1]
            
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        assert (self.sc_size<=self.num_bees), \
        "speramtheca size must be smaller than the num_bees"
        assert (self.m_p>=0 and self.m_p<=1), \
        "mutation_probability must be in [0,1]"
        assert (self.alpha>=0 and self.alpha<=1), \
        "crossover_probability must be in [0,1]"
        assert (self.omega>=0 and self.omega<=1), \
        "energy decay rate must be in [0,1]"
        
    def run(self):
        
        self.report=[] 
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)

        self.sc=[[None]*1]*(self.sc_size)
        self.best_f=sys.float_info.max
        self.old_f=sys.float_info.max
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# //////////////////////////////////////////////////////////////////////////// 
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.population[i]=v
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):                  

#///////evaluate objective functions 
            for i in range (0, self.num_bees):
                self.objectives[i]=self.f.f(self.population[i])   

# ////////////////////////////////////////////////////////////////////////////            
#                     Selection of the queen (best solution)
# ////////////////////////////////////////////////////////////////////////////
            index = self.objectives.index(min(self.objectives))

            if self.objectives[index] < self.best_f:

                self.best_f = self.objectives[index]
                self.best_P = copy.deepcopy(self.population[index])
 
            self.report.append(self.best_f)
            self.nfe.append(self.f.nfe)
            self.best=self.best_f
            self.solution=self.best_P   
            self.report_solution.append(self.solution)

                            
# ////////////////////////////////////////////////////////////////////////////            
#                              Mating fly
# ////////////////////////////////////////////////////////////////////////////
              

            x=0
            while (x<self.sc_size):
                v=[]

                for j in range(0,self.num_parameter):
                    r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                    v.append(r)


                self.sc[x]=copy.deepcopy(v)
                x+=1
                
# ////////////////////////////////////////////////////////////////////////////            
#                               Reproduction
# ////////////////////////////////////////////////////////////////////////////            

            self.population = [[None]*1]*self.num_bees
            self.objectives = [[None]*1]*self.num_bees

            for i in range(0,self.num_bees):
            
                c = random.randint(0,x-1)
                self.population[i]=copy.deepcopy(self.best_P)
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=0.5:
                        self.population[i][j]=copy.deepcopy(self.sc[c][j])
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=self.m_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.population[i][j]=r
                        
                        
# ////////////////////////////////////////////////////////////////////////////            
#                                  HBMO
# ////////////////////////////////////////////////////////////////////////////
class HBMO(object):
    def __init__(self,function,lower_boundary, upper_boundary,\
                 algorithm_parameters=[['num_iterate',2500],\
                              ['num_bees',100],\
                              ['mutation_probability',0.3],\
                              ['queen_speed_parameter',0.99],\
                              ['spermatheca_size',25],\
                              ['energy_decay_rate',0.01]]):
        
        self.__name__=HBMO        
        

        self.algorithm_parameters=algorithm_parameters
        
        self.num_bees=self.algorithm_parameters[1][1]
        self.num_itt=self.algorithm_parameters[0][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.f=function
        self.m_p=self.algorithm_parameters[2][1]
        self.alpha=self.algorithm_parameters[3][1]
        self.sc_size=self.algorithm_parameters[4][1]
        self.num_parameter=len(self.L)
        
        if self.algorithm_parameters[5][1] == None:
            self.omega=1/self.sc_size
        else:
            self.omega=self.algorithm_parameters[5][1]
            
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        assert (self.sc_size<=self.num_bees), \
        "speramtheca size must be smaller than the num_bees"
        assert (self.m_p>=0 and self.m_p<=1), \
        "mutation_probability must be in [0,1]"
        assert (self.alpha>=0 and self.alpha<=1), \
        "crossover_probability must be in [0,1]"
        assert (self.omega>=0 and self.omega<=1), \
        "energy decay rate must be in [0,1]"
        
    def run(self):
        
        self.report=[]  
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)

        self.sc=[[None]*1]*(self.sc_size)
        self.best_f=sys.float_info.max
        self.old_f=sys.float_info.max
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# //////////////////////////////////////////////////////////////////////////// 
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.population[i]=v
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):                  

#///////evaluate objective functions 
            for i in range (0, self.num_bees):
                self.objectives[i]=self.f.f(self.population[i])   
# ////////////////////////////////////////////////////////////////////////////            
#                   Sort population based on fitness
# ////////////////////////////////////////////////////////////////////////////             
           
            z = [self.population for _,self.population in \
            sorted(zip(self.objectives,self.population), key=lambda pair: pair[0])]
            self.population = copy.deepcopy(z)
            self.objectives.sort()

# ////////////////////////////////////////////////////////////////////////////            
#                     Selection of the queen (best solution)
# ////////////////////////////////////////////////////////////////////////////

            
            
            if self.objectives[0] < self.best_f:
                self.old_f = self.best_f

            
                self.best_f = self.objectives[0]
                self.best_P = copy.deepcopy(self.population[0])
                self.population.remove(self.population[0])
                self.objectives.remove(self.objectives[0])
            else:
                self.old_f = self.best_f
                self.old_P = copy.deepcopy(self.best_P)
 
            self.report.append(self.best_f)
            self.nfe.append(self.f.nfe)
            self.best=self.best_f
            self.solution=self.best_P  
            self.report_solution.append(self.solution)

                            
# ////////////////////////////////////////////////////////////////////////////            
#                              Mating fly
# ////////////////////////////////////////////////////////////////////////////
            if abs(self.best_f-self.old_f)==0:
                mating_flight=True
            else:
                mating_flight=False
              
            energy=1
            lambdaa=1
            x=0
            while ((energy>0 and x<self.sc_size) and mating_flight==True):
                v=[]

                for j in range(0,self.num_parameter):
                    r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                    v.append(r)
                energy-=self.omega

#///////evaluate objective functions 
                obj=self.f.f(v)   
                d=obj-self.best_f
                phi=math.exp(-abs(d)/lambdaa)
                rand=random.random()
                if phi>=rand:

                    lambdaa=self.alpha*lambdaa
                    self.sc[x]=copy.deepcopy(v)
                    x+=1

# ////////////////////////////////////////////////////////////////////////////            
#                              Trial Solutions
# ////////////////////////////////////////////////////////////////////////////

            k=0
            for i in range(x,self.sc_size):
                self.sc[i]=copy.deepcopy(self.population[k])
                k+=1
            
# ////////////////////////////////////////////////////////////////////////////            
#                               Reproduction
# ////////////////////////////////////////////////////////////////////////////            

            self.population = [[None]*1]*self.num_bees
            self.objectives = [[None]*1]*self.num_bees
            
            for i in range(0,int(self.num_bees*0.5)):
        
                c = random.randint(0,self.sc_size-1)
                self.population[i]=copy.deepcopy(self.best_P)
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=0.5:
                        self.population[i][j]=copy.deepcopy(self.sc[c][j])
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=self.m_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.population[i][j]=r
                
            for i in range (int(self.num_bees*0.5), self.num_bees):
                self.population[i]=copy.deepcopy(self.best_P)
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand<=self.m_p:
                        r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                        self.population[i][j]=r

            
            
            
# ////////////////////////////////////////////////////////////////////////////            
#                                  MBO
# ////////////////////////////////////////////////////////////////////////////            
            
class MBO(object):
    def __init__(self,function,lower_boundary, upper_boundary,\
                 algorithm_parameters=[['num_iterate',5000],\
                              ['num_bees',100],\
                              ['mutation_probability',0.3],\
                              ['queen_speed_parameter',0.99],\
                              ['spermatheca_size',25],\
                              ['energy_decay_rate',0.01]]):




        self.__name__=MBO
        
        self.algorithm_parameters=algorithm_parameters
        
        self.num_bees=self.algorithm_parameters[1][1]
        self.num_itt=self.algorithm_parameters[0][1]
        self.L=lower_boundary
        self.U=upper_boundary
        self.f=function
        self.m_p=self.algorithm_parameters[2][1]
        self.alpha=self.algorithm_parameters[3][1]
        self.sc_size=self.algorithm_parameters[4][1]
        self.num_parameter=len(self.L)
        
        if self.algorithm_parameters[5][1] == None:
            self.omega=1/(100*self.sc_size)
        else:
            self.omega=self.algorithm_parameters[5][1]
            
        
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upperboundary must be a list of the same length."
        assert (self.num_bees == int(self.num_bees)), \
        "Numbrer of bees must be integer"
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        assert (self.sc_size<=self.num_bees), \
        "speramtheca size must be smaller than the num_bees"
        assert (self.m_p>=0 and self.m_p<=1), \
        "mutation_probability must be in [0,1]"
        assert (self.alpha>=0 and self.alpha<=1), \
        "crossover_probability must be in [0,1]"
        assert (self.omega>=0 and self.omega<=1), \
        "energy decay rate must be in [0,1]"
        
    def run(self):
        
        self.report=[]  
        self.report_solution=[]
        self.nfe=[]
        self.population = [[None]*1]*(self.num_bees)
        self.objectives = [[None]*1]*(self.num_bees)

        self.sc=[[None]*1]*(self.sc_size)
        self.best_f=sys.float_info.max
        self.old_f=sys.float_info.max
        
        
# ////////////////////////////////////////////////////////////////////////////            
#                    Initiate first population randomly
# //////////////////////////////////////////////////////////////////////////// 
        for i in range(0, self.num_bees):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.population[i]=v
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# //////////////////////////////////////////////////////////////////////////// 
        for t in range(0, self.num_itt):                  

#///////evaluate objective functions 
            for i in range (0, self.num_bees):
                self.objectives[i]=self.f.f(self.population[i])   

# ////////////////////////////////////////////////////////////////////////////            
#                     Selection of the queen (best solution)
# ////////////////////////////////////////////////////////////////////////////
            index = self.objectives.index(min(self.objectives))

            if self.objectives[index] < self.best_f:

                self.best_f = self.objectives[index]
                self.best_P = copy.deepcopy(self.population[index])
 
            self.report.append(self.best_f)
            self.nfe.append(self.f.nfe)
            self.best=self.best_f
            self.solution=self.best_P     
            self.report_solution.append(self.solution)

                            
# ////////////////////////////////////////////////////////////////////////////            
#                              Mating fly
# ////////////////////////////////////////////////////////////////////////////
              
            energy=1
            lambdaa=1
            x=0
            while (energy>0 and x<self.sc_size):
                v=[]

                for j in range(0,self.num_parameter):
                    r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                    v.append(r)

#///////evaluate objective functions 
                obj=self.f.f(v)   
                d=obj-self.best_f
                phi=math.exp(-abs(d)/lambdaa)
                rand=random.random()
                if phi>=rand:
                    self.sc[x]=copy.deepcopy(v)
                    x+=1
                lambdaa=self.alpha*lambdaa
                energy-=self.omega                
# ////////////////////////////////////////////////////////////////////////////            
#                               Reproduction
# ////////////////////////////////////////////////////////////////////////////            

            self.population = [[None]*1]*self.num_bees
            self.objectives = [[None]*1]*self.num_bees
            if x!=0:
                for i in range(0,self.num_bees):
            
                    c = random.randint(0,x-1)
                    self.population[i]=copy.deepcopy(self.best_P)
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand<=0.5:
                            self.population[i][j]=copy.deepcopy(self.sc[c][j])
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand<=self.m_p:
                            r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                            self.population[i][j]=r
            else:            
                
                for i in range (0,self.num_bees):
                    self.population[i]=copy.deepcopy(self.best_P)
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand<=self.m_p:
                            r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                            self.population[i][j]=r
                            
# ////////////////////////////////////////////////////////////////////////////            
#                                  QBE
# ////////////////////////////////////////////////////////////////////////////            
            
class QBE(object):
    def __init__(self, function,lower_boundary, upper_boundary,\
                 algorithm_parameters=[['iteration',10000],\
                              ['population_size',100],\
                              ['normal_mutation_rate',0.8],\
                              ['normal_mutation_probability',0.05],\
                              ['strong_mutation_probability',1],\
                              ['crossover_probability',0.6],\
                              ['parents_portion',0.3]]):
        

        self.__name__=QBE
        
        self.algorithm_parameters=algorithm_parameters
        
        self.L=lower_boundary
        self.U=upper_boundary
        self.num_parameter=len(self.L)
        self.f=function
        self.g_pop_s=self.algorithm_parameters[1][1]
        self.n_mut_p=self.algorithm_parameters[3][1]
        self.s_mut_p=self.algorithm_parameters[4][1]
        
        self.pc=self.algorithm_parameters[5][1]
        self.num_itt=self.algorithm_parameters[0][1] 
        self.n_mut_r=self.algorithm_parameters[2][1]
        
        
        if self.g_pop_s % 2 != 0:
            self.g_pop_s+=1      
            
        self.num_g_parents=int(self.algorithm_parameters[6][1]*self.g_pop_s)       
        self.report=[]  
        self.report_solution=[]
        self.nfe=[]
        self.solution=[] 
            
        assert (len(self.U) == len(self.L)), \
        "lower boundary and upper boundary must be a list of the same length."
        
        assert (self.L <= self.U), \
        "Lower boundary must be less than or equal to upper boundary"
        
        assert (self.n_mut_p<=1 and self.n_mut_p>=0), \
        "normal_mutation_probability must be in range [0,1]"   
        
        assert (self.s_mut_p<=1 and self.s_mut_p>=0), \
        "strong_mutation_probability must be in range [0,1]"    
        
        assert (self.n_mut_r<=1 and self.n_mut_r>=0), \
        "normal_mutation_rate must be in range [0,1]" 
        
        assert (self.num_g_parents<=self.g_pop_s), \
        "parents_portion must be in range [0,1]"
        
    def run(self):
        
        
        self.g_population = [[None]*1]*(self.g_pop_s)
        self.g_objectives = [[None]*1]*(self.g_pop_s)
        self.g_normobj=[[None]*1]*(self.g_pop_s)
        self.g_cumprob=[[None]*1]*(self.g_pop_s)
        self.best = sys.float_info.max
        self.g_parents=[[None]*1]*(self.num_g_parents)
        self.g_parents_obj=[[None]*1]*(self.num_g_parents)


# ////////////////////////////////////////////////////////////////////////////            
#                 Initiate first global GA population randomly
# ////////////////////////////////////////////////////////////////////////////        
        for i in range(0, self.g_pop_s):
            v=[]
            for j in range(0,self.num_parameter):
                r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                v.append(r)
                self.g_population[i]=v
#///////evaluate objective functions 
            self.g_objectives[i]=self.f.f(self.g_population[i])
            
        index=self.g_objectives.index(min(self.g_objectives))

        self.queen_g=copy.deepcopy(self.g_population[index])
        self.queen_f=copy.deepcopy(self.g_objectives[index])            
# ////////////////////////////////////////////////////////////////////////////            
#                        Start itteration 
# ////////////////////////////////////////////////////////////////////////////            
        for t in range(0, self.num_itt):             

#///////select the queen   
            index=self.g_objectives.index(min(self.g_objectives))
            if self.queen_f>self.g_objectives[index]:
                

                self.queen_g=copy.deepcopy(self.g_population[index])
                self.queen_f=copy.deepcopy(self.g_objectives[index])

            self.report.append(self.queen_f)
            self.nfe.append(self.f.nfe)
            self.solution=self.queen_g
            self.report_solution.append(self.solution)
            
            self.best=self.queen_f

# ////////////////////////////////////////////////////////////////////////////            
#                    Normalizing objective function 
# ////////////////////////////////////////////////////////////////////////////
            minobj=min(self.g_objectives)
            if minobj<0:
                for i in range(0,self.g_pop_s):
                    self.g_normobj[i]=self.g_objectives[i]+abs(minobj)
            else:
                for i in range(0,self.g_pop_s):
                    self.g_normobj[i]=self.g_objectives[i]
            maxnorm=max(self.g_normobj)
            for i in range(0,self.g_pop_s):
                self.g_normobj[i]=maxnorm-self.g_normobj[i]+1 
                
# ////////////////////////////////////////////////////////////////////////////            
#                           Calculate probability
# ////////////////////////////////////////////////////////////////////////////                
                
            sum_normobj=sum(i for i in self.g_normobj)
            prob=0
            for i in range(0,self.g_pop_s):
                prob+=self.g_normobj[i]/sum_normobj
                self.g_cumprob[i]=prob
                
                
# ////////////////////////////////////////////////////////////////////////////            
#                             GA parents selection
# ////////////////////////////////////////////////////////////////////////////                    
            for k in range (0,int(self.num_g_parents/2)):
                self.g_parents[k]=copy.deepcopy(self.queen_g)
                self.g_parents_obj[k]=copy.deepcopy(self.queen_f)                
                
            for k in range (int(self.num_g_parents/2),self.num_g_parents):
                rand=random.random()
                if rand <= self.g_cumprob[0]:
                    b=0
                else:
                    for i in range(1,self.g_pop_s):
                        if rand <= self.g_cumprob[i] and rand> self.g_cumprob[i-1]:
                            b=i
                self.g_parents[k]=copy.deepcopy(self.g_population[b])
                self.g_parents_obj[k]=copy.deepcopy(self.g_objectives[b])

            self.effective_parents=[]
            parent_num=0

            while(parent_num==0):
                for k in range (0,self.num_g_parents):
                    rand=random.random()
                    if rand < self.pc:
                        self.effective_parents.append(self.g_parents[k])
                
                parent_num=len(self.effective_parents)
                
# ////////////////////////////////////////////////////////////////////////////            
#                            New GA generation
# //////////////////////////////////////////////////////////////////////////// 

                
            for k in range(0,self.g_pop_s,2):
                
                rand1=random.randint(0,parent_num-1)
                rand2=random.randint(0,parent_num-1)
                parent1=copy.deepcopy(self.effective_parents[rand1])
                parent2=copy.deepcopy(self.effective_parents[rand2])
                child1=copy.deepcopy(parent1)
                child2=copy.deepcopy(parent2)
                
                for j in range (0,self.num_parameter):
                    rand=random.random()
                    if rand < 0.5:
                        child1[j]=copy.deepcopy(parent2[j])
                        child2[j]=copy.deepcopy(parent1[j])
                        
                self.g_population[k]=copy.deepcopy(child1)
                self.g_population[k+1]=copy.deepcopy(child2)
                
            for k in range (0,self.g_pop_s):
                
                if k <= (self.n_mut_r*self.g_pop_s):
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand <= self.n_mut_p:
                            r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                            self.g_population[k][j]=r
                else:
                    for j in range (0,self.num_parameter):
                        rand=random.random()
                        if rand <= self.s_mut_p:
                            r=self.L[j]+random.random() * (self.U[j] - self.L[j])
                            self.g_population[k][j]=r
#///////evaluate objective functions                        
            for k in range(0,self.g_pop_s):
                self.g_objectives[k]=self.f.f(self.g_population[k])
  
        
        
        
        
                        

                       

            
            
                        
                
                
                
                                    
            
                
                
                
            
            
            
        
        
        

        
        
        
                        
                
                