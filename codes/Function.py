#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 23:11:50 2019

@author: Mohammad Solgi
"""
import numpy as np
import math
import time

        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Ackley
# ////////////////////////////////////////////////////////////////////////////
        
class Ackley(object):
    def __init__(self,nfe=0):
        
        self.__name__=Ackley
        
        self.nfe=nfe
        self.L=[-32.768]
        self.U=[32.768]
        

        
    def f(self,vector):
        

        
        vector = np.array(vector)
        self.nfe+=1
        dim=len(vector)
        
        t1=0
        t2=0
        for i in range (0,dim):
            t1+=vector[i]**2
            t2+=math.cos(2*math.pi*vector[i])
    
        
            
        OF=20+math.e-20*math.exp((t1/dim)*-0.2)-math.exp(t2/dim)
            

    
        return OF
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Griewank
# //////////////////////////////////////////////////////////////////////////// 
class Griewank(object):
    def __init__(self,nfe=0):
        
        
        self.__name__=Griewank
          
        self.nfe=nfe   
        
        
        self.L=[-600]
        self.U=[600]
        
    def f(self,vector):
    

        self.nfe+=1

        dim=len(vector)
    
        vector = np.array(vector)
        t1=0
        t2=1
        for i in range (0,dim):
            t1+=(vector[i]-100)**2
            t2=t2*math.cos((vector[i]-100)/((i+1)**0.5))
        OF=(t1/4000)-t2+1
        
        return OF
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Michalewicz
# //////////////////////////////////////////////////////////////////////////// 
class Michalewicz(object):
    def __init__(self,nfe=0):
        
        self.__name__=Michalewicz        
        
        self.nfe=nfe
        self.L=[0]
        self.U=[math.pi]
        
    def f(self,vector):
    
    
        vector = np.array(vector)

        self.nfe+=1

        dim=len(vector)
        
        
        OF=0
        for i in range (0,dim):
            OF-=math.sin(vector[i])*(math.sin(((i+1)*vector[i]**2)/math.pi))**20
    
            
    
    
        return OF
    
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Rastrigin
# ////////////////////////////////////////////////////////////////////////////
class Rastrigin(object):
    def __init__(self,nfe=0):
        
        self.__name__=Rastrigin        
        self.nfe=nfe
        
        self.L=[-5.12]
        self.U=[5.12]

    def f(self,vector):
    

        self.nfe+=1

        dim=len(vector)  
        
        vector = np.array(vector)
        OF=0
        for i in range (0,dim):
            OF+=(vector[i]**2)-10*math.cos(2*math.pi*vector[i])+10
        
      
    
        return OF
    
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Rosenbrock
# ////////////////////////////////////////////////////////////////////////////
class Rosenbrock(object):
    def __init__(self,nfe=0):
        
        self.__name__=Rosenbrock              
        self.nfe=nfe  
        
        self.L=[-50]
        self.U=[50]
    
    def f(self,vector):
    

        self.nfe+=1

        dim=len(vector)
        
        vector = np.array(vector)
        OF=0
        for i in range (0,dim-1):
            OF+=(100*(vector[i+1]-(vector[i]**2))**2)+(vector[i]-1)**2
        

    
        return OF
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Schaffer
# //////////////////////////////////////////////////////////////////////////// 
class Schaffer(object):
    def __init__(self,nfe=0):
        
        self.__name__=Schaffer         
        self.nfe=nfe          
    

        self.L=[-100]
        self.U=[100]
        
    def f(self,vector):
    
        

        self.nfe+=1

        dim=len(vector)
        vector = np.array(vector)
        
        y=0
        for i in range (0,dim):
            y+=vector[i]**2
        s=math.sin(y**0.5)
        OF=0.5+(((s**2)-0.5)/(1+0.001*y)**2)
    
    
        return OF
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Sphere
# //////////////////////////////////////////////////////////////////////////// 
class Sphere(object):
    def __init__(self,nfe=0):
        
        self.__name__=Sphere          
        self.nfe=nfe  
        
        self.L=[-100]
        self.U=[100]
        
    def f(self,vector):
    
        

        self.nfe+=1

        dim=len(vector)
        
        vector = np.array(vector)
        OF=0
        for i in range (0,dim):
            OF+=vector[i]**2

    
        return OF    
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Schwefel
# ////////////////////////////////////////////////////////////////////////////
class Schwefel(object):
    def __init__(self,nfe=0):
        
        self.__name__=Schwefel           
        self.nfe=nfe
        
        
        self.L=[-500]
        self.U=[500]
    
    def f(self,vector):
    

        self.nfe+=1

        dim=len(vector) 
        
        vector = np.array(vector)

        
        
        OF=0
        for i in range (0,dim):
            OF+=-vector[i]*math.sin((abs(vector[i]))**0.5)
            
        OF=418.9829*dim-OF
    
        return OF
# ////////////////////////////////////////////////////////////////////////////
        
# ////////////////////////////////////////////////////////////////////////////            
#                                  Weierstrass
# ////////////////////////////////////////////////////////////////////////////
class Weierstrass(object):
    def __init__(self,nfe=0):
        
        self.__name__=Weierstrass            
        self.nfe=nfe
        
        self.L=[-0.5]
        self.U=[0.5]

        
    def f(self,vector):
    
        

        self.nfe+=1

        dim=len(vector) 
        
        vector = np.array(vector)

        a=0.5
        b=3
        OF=0
        for i in range (0,dim):
            t1=0
            for k in range (0,21):
                t1+=(a**k)*math.cos((2*math.pi*(b**k))*(vector[i]+0.5))
            OF+=t1
        t2=0    
        for k in range (0,21):
            t2+=(a**k)*math.cos(math.pi*(b**k))
        OF-=dim*t2
    
        return OF
# ////////////////////////////////////////////////////////////////////////////            
#                                     Constrained-1
# ////////////////////////////////////////////////////////////////////////////
class Constrained(object):    
    def __init__(self,nfe=0):
        
        self.__name__=Constrained         
        self.nfe=nfe
        
        self.L=[-6]
        self.U=[6]   
        
    def f(self,vector):
    
        

        self.nfe+=1

#        dim=len(vector) 
        
        vector = np.array(vector)

        g=5.062-vector[0]**2-(vector[1]-2.5)**2
        h=(vector[0]-0.05)**2+(vector[1]-2.5)**2-4.83688798
        

        OF=(((vector[0]**2)+vector[1]-11)**2)+(vector[0]+(vector[1]**2)-7)**2
        if h<0:
            OF+=5000+1000*abs(h)
        if g<0:
            OF+=5000+1000*abs(g)
        
    
        return OF        
        
    
    
    
    