#!/usr/bin/env python
# coding: utf-8

# In[38]:


get_ipython().system('pip install wotan')
get_ipython().system('pip install statsmodels sklearn supersmoother pygam')
from astropy.table import QTable
import pandas as pd
import astropy.units as un
import numpy as np
import matplotlib.pyplot as plt
from statistics import stdev
from wotan import flatten



# In[39]:


data = QTable.read("a3123_20170429_004_5_GL436_01637MHz_ON_ON_series.csv")
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
fig.suptitle("a3123_20170429_004_5_GL436_01637MHz_ON_ON_series", fontsize= "x-large")


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

#data.to_pandas()


# # Examples of Different De-Trending Techniques using Wotan package in Python

# ## Time-windowed sliders with location estimates methods: Biweight, Mean, Huber

# ## De-Trending using Biweight method

# In[40]:


#Biweight

flatten_lc1, trend_lc1 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of Stokes values (I,Q,U,V)
    method='biweight',
    window_length=20,    # The length of the filter window in units of ``time``
    edge_cutoff=0.5,      # length (in units of time) to be cut off each edge.
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    cval=5.0              # Tuning parameter for the robust estimators
    )
# Mean
flatten_lc2, trend_lc2 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of Stokes values (I,Q,U,V)
    method='mean',
    window_length=20,    # The length of the filter window in units of ``time``
    edge_cutoff=0.5,      # length (in units of time) to be cut off each edge.
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    cval=5.0              # Tuning parameter for the robust estimators
    )

# Huber
flatten_lc3, trend_lc3 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of Stokes values (I,Q,U,V)
    method='huber',
    window_length=20,    # The length of the filter window in units of ``time``
    edge_cutoff=0.5,      # length (in units of time) to be cut off each edge.
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    cval=5.0              # Tuning parameter for the robust estimators
    )

#Median
flatten_lc4, trend_lc4 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of Stokes values (I,Q,U,V)
    method='median',
    window_length=20,    # The length of the filter window in units of ``time``
    edge_cutoff=0.5,      # length (in units of time) to be cut off each edge.
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    cval=5.0              # Tuning parameter for the robust estimators
    )

#Visualize methods

from matplotlib import rcParams; rcParams["figure.dpi"] = 150

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc1, color='red', linewidth=1, label="Biweight")
plt.plot(time, trend_lc2, color='cyan', linewidth=1,label="Mean")
plt.plot(time, trend_lc3, color='orange', linewidth=1, label="Huber")
plt.plot(time, trend_lc4, color='green', linewidth=1, label="Median")
plt.legend()
plt.title("Robust statistics methods for detrending: Time-windowed sliders with location estimates")
plt.show();
plt.close()

plt.scatter(time, flatten_lc1, s=1, color='red', label="Biweight")
plt.scatter(time, flatten_lc2, s=1, color='cyan',label="Mean")
plt.scatter(time, flatten_lc3, s=1, color='orange',label="Huber")
plt.scatter(time, flatten_lc4, s=1, color='green',label="Median")
plt.legend()
plt.title("Robust statistics methods for detrending: Time-windowed sliders with location estimates")
plt.show()
plt.close();


# "Note: The tuning constant cval is defined as multiples in units of median absolute deviation from the central location. Defaults are usually chosen to achieve high efficiency for Gaussian distributions. For the biweight a cval of 6 includes data up to 4 standard deviations (6 median absolute deviations) from the central location and has an efficiency of 98%. Another typical value for the biweight is 4.685 with 95% efficiency. Larger values for make the estimate more efficient but less robust. The default for the biweight in wotan is 5, as it has shown the best results in the transit injection retrieval experiment."
# 
# Source: https://github.com/hippke/wotan/blob/master/examples/biweight.ipynb

# ## Polynomial and Sine Methods: De-Trending using Cofiam, Cosine and Savgol methods

# ##  > Detrending using Cofiam method

# In[41]:


#Cofiam
flatten_lc5, trend_lc5 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='cofiam',
    window_length=20
    ,    # The length of the filter window in units of ``time``
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )

#Cosine
flatten_lc6, trend_lc6 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='cosine',
    robust=True,          # Iteratively clip 2-sigma outliers until convergence
    window_length=20,    # The length of the filter window in units of ``time``
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )
#Savgol
flatten_lc7, trend_lc7 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='savgol',
    window_length=int(1000/60),    # The length of the filter window in cadences
    break_tolerance=20,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )

#Visualize

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc5, color='red', linewidth=1, label= "Cofiam")
plt.plot(time, trend_lc6, color='cyan', linewidth=1, label="Cosine")
plt.plot(time, trend_lc7, color='orange', linewidth=1, label="Savgol")
plt.legend()
plt.title("De-Trending using Cofiam, Cosine and Savgol methods for I Stokes \n a3123(_20170429_004_5_GL436_01637MHz_ON_ON_series")
plt.show()
plt.close()

#plt.scatter(time, i_mean, s=1, color='black')
#plt.plot(time, trend_lc5, color='red', linewidth=1, label='cofiam')
#plt.xlim(5, 9)
#plt.ylim(0.9995, 1.0022)
#plt.legend()
#plt.show();
#plt.close()

plt.scatter(time, flatten_lc5, s=1, color='red',label="Cofiam");
plt.scatter(time, flatten_lc6, s=1, color='cyan', label="Cosine")
plt.scatter(time, flatten_lc7, s=1, color='orange',label="Savgol")
plt.legend()
plt.show()
plt.close()


# ## > Detrending using Cosine method

# In[16]:


flatten_lc2, trend_lc2 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='cosine',
    robust=True,          # Iteratively clip 2-sigma outliers until convergence
    window_length=20,    # The length of the filter window in units of ``time``
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )

#Visualize

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc2, color='cyan', linewidth=1)
plt.show();
plt.close()

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc2, color='cyan', linewidth=1, label='cosine')
plt.xlim(5, 9)
plt.ylim(0.9995, 1.0022)
plt.legend()
plt.show();
plt.close()

plt.scatter(time, flatten_lc1, s=1, color='black');


# ## > Detrending using Savgol method

# In[22]:


flatten_lc3, trend_lc3 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='savgol',
    window_length=int(1000/60),    # The length of the filter window in cadences
    break_tolerance=20,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )


#Visualize

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc3, color='orange', linewidth=1, label='savgol')
plt.show();
plt.close()

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc3, color='orange', linewidth=1, label='savgol')
plt.xlim(5, 9)
plt.ylim(0.9995, 1.0022)
plt.legend()
plt.show();
plt.close()

plt.scatter(time, flatten_lc1, s=1, color='black');


# ## Regression Methods: Using lowess and supersmooth methods

# In[ ]:


flatten_lc1, trend_lc1 = flatten(
    time,                 # Array of time values
    i_mean,                 # Array of flux values
    method='lowess',
    window_length=1.5,    # The length of the filter window in units of ``time``
    break_tolerance=0.5,  # Split into segments at breaks longer than that
    return_trend=True,    # Return trend and flattened light curve
    )


plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc1, color='red', linewidth=1)
#plt.plot(time, trend_lc2, color='blue', linewidth=1)
plt.show();
plt.close()

plt.scatter(time, i_mean, s=1, color='black')
plt.plot(time, trend_lc1, color='red', linewidth=1, label='lowess')
#plt.plot(time, trend_lc2, color='blue', linewidth=1, label='supersmoother')
plt.xlim(5, 9)
plt.ylim(0.9995, 1.0022)
plt.legend()
plt.show();
plt.close()

plt.scatter(time, flatten_lc1, s=1, color='black');


# Only lowess worked, for some reason.
# 
# ## Ridge regression, LASSO, Elasticnet

# In[ ]:





# In[ ]:




