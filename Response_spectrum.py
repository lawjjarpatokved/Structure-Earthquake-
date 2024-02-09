import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


accl=pd.read_csv('Time_Series/Formatted/for_testing_random_collection/Irpinia.txt',header=None,sep=',')

g=981
dt=(accl.iloc[1][0])-(accl.iloc[0][0])
Final_time=accl.iloc[-1][0]
No_of_steps=int(Final_time/dt)

#Function to find the spectral acceleration for a given Time period.
def Spectral_acceleration(Time_period,Damping,accln,g):
    print("No problem till here1")
    #Necessary data from acceleration time history
    dt=(accln.iloc[1][0])-(accln.iloc[0][0])
    Final_time=accln.iloc[-1][0]
    #print("No problem till here2")
    No_of_steps=int(Final_time/dt)
    #print("No problem till here2")
    # accln.iloc[:,1]=accln.iloc[:,1]*scaling
    #Necessary calculations for Newmarks algorithm
    
    w=2*np.pi/Time_period
    K=(w**2)
    C=2*(Damping/100)*w
    a1=(6/(dt*dt))+(3/dt)*C
    a2=(6/dt)+2*C
    a3=2+(dt/2)*C
    K_hat=K+a1
    u0=0 # initial displacement
    v0=0 # initial velocity
    a0=-accln[0][1]*g # initial acceleration
    displacement=[]
    displacement.append(u0)
    velocity=[]
    velocity.append(v0)
    acceleration=[]
    acceleration.append(a0)
    PI=[]
    PI.append("-")

    for i in range(1,No_of_steps+1):
        Pi=-accln.iloc[i][1]*g+a1*displacement[i-1]+a2*velocity[i-1]+a3*acceleration[i-1]
        PI.append(Pi)
        displacement.append(Pi/K_hat)
        vel=(3/dt)*(displacement[i]-displacement[i-1])-2*velocity[i-1]-(dt/2)*acceleration[i-1]
        velocity.append(vel)
        acl=(6/dt**2)*(displacement[i]-displacement[i-1])-(6/dt)*velocity[i-1]-2*acceleration[i-1]
        acceleration.append(acl)
    Spec_disp=max(max(displacement),abs(min(displacement)))
    Spec_acc=max(max(acceleration),abs(min(acceleration)))
    Pseudo_Vel=w*Spec_disp
    Pseudo_accl=w*Pseudo_Vel
    # print(f"w={w}")
    # print(f"K={K}")
    # print(f"C={C}")
    # print(f"a1={a1}")
    # print(f"a2={a2}")
    # print(f"a3={a3}")
    # print(f"Khat={K_hat}")
    df=pd.DataFrame(PI)
    df[1]=pd.DataFrame(displacement)
    df[2]=pd.DataFrame(velocity)
    df[3]=pd.DataFrame(acceleration)
    # df.insert(0,"time",accl.iloc[:,0].values)
    # df.insert(1,"accl",accl.iloc[:,1].values)
    disp_max=abs(df[1].values)
    Spec_disp=max(disp_max)
    Pseudo_vel=Spec_disp*w
    Pseudo_accl=Pseudo_vel*w/g
    return Spec_acc/g


time=[]
spec_acc=[]
plt.figure()
for a in np.arange(0.01,3.01,0.01):
    time.append(a)
    d=Spectral_acceleration(a,5,accl,g)
    spec_acc.append(d)
plt.plot(time,spec_acc,color='blue')
plt.xlabel('Time Period')
plt.ylabel('Acceleration(g)')
plt.title('Pseudo Acceleration Response Spectrum')
plt.show()