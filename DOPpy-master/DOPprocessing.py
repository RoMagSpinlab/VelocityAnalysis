#DOPprocessing.py
#JAA 3/1/23

# Uses DOPpy.py to import data arrays from .BDD files, then compiles data from 
# all channels into matrices, then saves the dataset as a .mat file.

# This script should be inside the directory DOPpy-master. You need a 
# directory called "Files_BDD" with all .BDD files you want to process,
# as well as a directory called "Files_MAT" to store the .mat files.

# To use: just change fname to the name of the file (without extension) that 
# you want to import. The corresonding .mat will be saved with the same fname.

# The matrices that are stored in the .mat have the following properties:
#   t = time (seconds)
#       rows = time entries
#       columns = channels (always 10 total columns)
#   d = depth (mm) aka distance from transducer
#       rows = channels (always 10 total rows)
#       columns = space entries (number of gates)
#   v = velocity(m/s) 
#       rows = velocity at each time step
#       columns = velocity at each depth location
#       level = channel (always 10 total levels)
# *If a channel was not used to record data, then that channel will show as 
# all zeros


###########################################################


#Import packages
from DOPpy import DOP
from scipy.io import savemat
import numpy as np

#Define file name
dname   = 'Files_BDD/' 
fname   = 'RC_85W34C1RPM_6000blks_175820'

#Where to save?
dsave   = 'Files_MAT/'

#Read in data
bdd     = DOP(dname + fname + '.BDD')
chans   = bdd.getChannels()
time    = bdd.getTime(1)    #length of time is the same for all channels
gate    = bdd.getDepth(1)   #number of gates is the same for all channels
chanALL = 10                #value if all channels are being used (gives easier processing to make all matrices this size)

#Pre-allocate time, depth, and velocity matrices
t = np.zeros((time.size,chanALL))
d = np.zeros((chanALL,gate.size))
v = np.zeros((time.size,gate.size,chanALL))

#Populate matrices with measurements
for i in chans:
    t[:,i-1] = bdd.getTime(i); 
    d[i-1,:] = bdd.getDepth(i);
    v[:,:,i-1] = bdd.getVelocity(i)
    
#Save the data as a .mat
savemat(dsave + fname + '.mat', dict(t=t, d=d, v=v))

# Channel 1  = D4
# Channel 2  = D2
# Channel 3  = D3
# Channel 4  = D8
# Channel 5  = D5
# Channel 6  = D6
# Channel 7  = D7
# Channel 8  = D9
# Channel 9  = NA (D1 is the missing probe)
# Channel 10 = D10


###########################################################


# # Quick visualization: (may need to change the time and space cutoffs in the
# # plt.contour command as well as the plt.clim range)

# #Channel to look at
# chan = 1

# # Import data
# xdata = bdd.getTime(chan)
# ydata = bdd.getDepth(chan)
# zdata = bdd.getVelocity(chan)

# # Implementation of matplotlib function
# import matplotlib.pyplot as plt

# plt.figure(figsize=(8, 3))
# ax = plt.gca()

# # plots filled contour plot
# CF = plt.contourf(xdata[:], ydata[0:241], np.transpose(zdata[:,0:241])*1000, 50,
#                   cmap=plt.cm.RdBu)
# plt.gca().invert_yaxis()
 
# ax.set_xlabel('Times [s]')
# ax.set_ylabel('Depth [mm]')
# #plt.clim(-3,3)
# cbar = plt.colorbar(CF)
# cbar.ax.set_ylabel('u [mm/s]')
# plt.show()

# #### 




