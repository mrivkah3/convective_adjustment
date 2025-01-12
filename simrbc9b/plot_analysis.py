
import h5py
import matplotlib.pyplot as plt
import numpy as np
import dedalus.public as d3

#open first analysis
with h5py.File("analysis/analysis_s1.h5", mode='r') as file:
    # Load datasets
    b_freq = file['tasks']['N2 x=.25']
    t = b_freq.dims[0]['sim_time']
    z = b_freq.dims[2][0]
    
    j=np.arange(b_freq.shape[2])
   # avg_z_b= np.sum(b_freq[200,0,: ].real*np.cos(2*np.pi*(j+1/2)))
    
    #avg_t=np.sum(b_freq[:,0,:].real*.5, axis=0)/t[-1]
    average_t=np.mean(b_freq[0:40:1,0,:].real, axis=0)
    average_t1=np.mean(b_freq[40:80:1,0,:].real, axis=0)
    average_t2=np.mean(b_freq[80:120:1,0,:].real, axis=0)
    average_t3=np.mean(b_freq[120:160:1,0,:].real, axis=0)
    average_t4=np.mean(b_freq[160:199:1,0,:].real, axis=0)
    # Plot data
    fig = plt.figure(figsize=(6, 4), dpi=100)
    #print(t[1:]-t[:-1])
    #print(z.shape)
    #print(avg_t.shape)
    #print(t[100])
    #print(b_freq[:].real.shape)
    plt.plot(average_t,z[:], label='t=0-40')
    plt.plot(average_t1, z[:], label='t=40-80')
    plt.plot(average_t2, z[:], label='t=80-120')
    plt.plot(average_t3, z[:], label='t=120-160')
    plt.plot(average_t4, z[:], label='t=160-199')
   # plt.plot( b_freq[0,0,:].real, z[:], label='t=%f' %t[0])
   # plt.plot( b_freq[100,0,:].real, z[:], label='t=%f' %t[100])
   # plt.plot( b_freq[200,0,:].real, z[:], label='t=%f' %t[200])
   # plt.plot( b_freq[300,0,:].real, z[:], label='t=%f' %t[300])
   # plt.plot( b_freq[399,0,:].real, z[:], label='t=%f' %t[399])
    plt.title('average t values at  x=.25')
    plt.xlabel('N2')
    plt.ylabel('z')
    plt.xlim([-3,5])
    plt.legend()
    plt.savefig('plots/all_average_t_x=.25_rbc9.png')
