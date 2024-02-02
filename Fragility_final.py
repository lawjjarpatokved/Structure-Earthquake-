
import numpy as np
import math as math
import openseespy.opensees as ops
import time
import openseespy.postprocessing.Get_Rendering as opp
import vfo.vfo as vfo
import matplotlib.pyplot as plt
import os
import pandas as pd
from Assign_Functions import *
import scipy as scp

def fragility_interpolator(IDA_output,Polynomial_degree,limit_states):
    x_values=IDA_output.iloc[:,0].values
    y_values=IDA_output.iloc[:,1].values 

### THIS PART IS FOR FITTING THE POINTS WITH POLYNOMIAL EQN OF 3RD DEGREE
### IF YOU WISH TO USE CUBIC SPLINE COMMENT OUT THIS CHUNK OF CODE 
    a=np.polyfit(x_values,y_values,Polynomial_degree) 
    p=np.poly1d(a)
    x=np.linspace(min(x_values),max(x_values),100)
    plt.figure(figsize=(5, 5))
    plt.scatter(x_values,y_values)
    plt.plot(x,p(x),color="r")
    plt.title(f"Polynomial of degree {Polynomial_degree}")
    plt.show()
    return p(limit_states.iloc[0][1]),p(limit_states.iloc[1][1]),p(limit_states.iloc[2][1])

### IF YOU WISH TO USE CUBIC SPLINE INTERPOLATION COMMENT OUT THE ABOVE CHUNK OF CODE
    cs=scp.interpolate.CubicSpline(x_values,y_values)
    x=np.linspace(min(x_values),max(x_values),100)
    plt.figure(figsize=(5, 5))
    plt.scatter(x_values,y_values)
    plt.plot(x,cs(x),color="r")
    plt.title("CubicSpline")
    plt.show()
    return cs(limit_states.iloc[0][1]),cs(limit_states.iloc[1][1]),cs(limit_states.iloc[2][1])

    

def fragility_parameters(Damage_state):
   Log_Damagestate=[np.log(a) for a in Damage_state]
   s=pd.Series(Log_Damagestate)
   Mean=s.mean()
   STDEV=s.std()
   return Mean,STDEV

def fragility_help(x,Log_mean,Log_SD):
    return scp.stats.norm.cdf((np.log(x)-Log_mean)/Log_SD)

def fragility_plotter(x,y,z,w):
   plt.plot(x,y,color='g',label='IO')
   plt.plot(x,z,color='b',label='LS')
   plt.plot(x,w,color='r',label='CP')
   plt.legend()
   plt.title('Fragility Curves')
   plt.xlabel('Sa(T1,5%)')
   plt.ylabel('Probability of Failure')
   plt.grid()
   plt.show()

def fragility_generator():
    IO=[]
    LS=[]
    CP=[]
    limit_states=pd.read_csv('D:\c drive\Desktop\SBSB\SBSB IDA\sagar_latest\Time_Series\Formatted\Limit_states.txt')
    IDA_capacity_curve_filepath='D:\c drive\Desktop\SBSB\SBSB IDA\sagar_latest\Time_Series\Formatted\SBSB_1st_trial-20240130T101302Z-001\SBSB_1st_trial\IDA_capacity_curve'
    for files in os.listdir(IDA_capacity_curve_filepath):
        if files.endswith('.csv'):    
            CSV_path=os.path.join(IDA_capacity_curve_filepath,files)
            IDA_output=pd.read_csv(CSV_path,header=None,sep=',')
            io,ls,cp=fragility_interpolator(IDA_output,2,limit_states)
            IO.append(io)
            LS.append(ls)
            CP.append(cp)
    IO_mean,IO_stdev=fragility_parameters(IO)
    LS_mean,LS_stdev=fragility_parameters(LS)
    CP_mean,CP_stdev=fragility_parameters(CP)
    print(IO_mean,IO_stdev,LS_mean,LS_stdev,CP_mean,CP_stdev)
    x = np.arange(0.001, 5, 0.001)
    fragility_plotter(x,fragility_help(x,IO_mean,IO_stdev),fragility_help(x,LS_mean,LS_stdev),fragility_help(x,CP_mean,CP_stdev))

   
fragility_generator()
