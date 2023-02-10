#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
from scipy.io import readsav
import numpy as np
import glob



# In[5]:


Frequencies= []
I_Stokes= []
Trends= []
Data_Frames= []

Path= "home/jovyan/work/custom/ARECIBO REDS/New_Reduced_Data"

Files= glob.glob(Path + "\*.sav")

#print(glob.glob(Path + "\*.sav"))
 
for file in Files:
    IDL_data= readsav(file)
    IDL_data_all= IDLdata["data"]
    i_stokes= IDL_data_all["I"][0]
    freq= IDL_data_all["f"][0]
    I_Stokes.append(i_stokes)
    Frequencies.append(freq)
    print(i_stokes)
print("Done")

#print(Frequencies)
#data = QTable.read("/New_Reduced_Data/a3123_reduced_20170429_000_B1140+223.sav")


# In[6]:


data = QTable.read("a3123_reduced_20170429_000_B1140+223.sav")
#print(data)
time= data['Time (s)']

i_mean= data['I_mean (Jy)']
i_serror= data['I_serror (Jy)']
print(np.std(i_serror))
#print(stdev(i_serror))

q_mean= data['Q_mean (Jy)']
q_serror= data['Q_serror (Jy)']
print(np.std(q_serror))

u_mean= data['U_mean (Jy)']
u_serror= data['U_serror (Jy)']
print(np.std(u_serror))

v_mean= data['V_mean (Jy)']
v_serror= data['V_serror (Jy)']
print(np.std(v_serror))

fig,axs= plt.subplots(4,1, sharex= True, figsize=(12,10))
fig.suptitle("a3123_reduced_20170429_000_B1140+223", fontsize= "x-large")


axs[0].plot(time,i_mean)
#axs[0].plot(time,i_serror, color="g")
#axs[0].axhline(np.std(i_serror), color='r',linestyle= "dashed")
#axs[0].axhline(-(np.std(i_serror)), color='r',linestyle= "dashed")
#axs[0].plot(np.std(i_serror), linestyle= "dashed", color="green")
axs[0].set_ylabel("Stokes I (Jy)")
axs[0].set_xlim(0, 600)

axs[1].plot(time,q_mean)
axs[1].set_ylabel("Stokes Q (Jy)")
axs[1].set_xlim(0, 600)

axs[2].plot(time,u_mean)
axs[2].set_ylabel("Stokes U (Jy)")
axs[2].set_xlim(0, 600)

axs[3].plot(time,u_mean)
axs[3].set_ylabel("Stokes V (Jy)")
axs[3].set_xlim(0, 600)
axs[3].set_xlabel("Time (s)")

#plt.subplot(time,i_mean)
#plt.subplot(time,q_mean)
plt.show()


# In[ ]:




