
import h5py
import matplotlib.pyplot as plt
import numpy as np
import dedalus.public as d3

#open first analysis
with h5py.File("analysis/analysis_s1.h5", mode='r') as file:
    # Load datasets
    b_freq = file['tasks']['N2 x=1.45']
    t = b_freq.dims[0]['sim_time']
    z = b_freq.dims[2][0]


    # Plot data
    fig = plt.figure(figsize=(6, 4), dpi=100)
    print(z.shape)
    print(t.shape)
    print(t[100])
    print(b_freq[:].real.shape)
    plt.plot( b_freq[0,0,:].real, z[:], label='t=%f' %t[0])
    plt.plot( b_freq[100,0,:].real, z[:], label='t=%f' %t[100])
    plt.plot( b_freq[200,0,:].real, z[:], label='t=%f' %t[200])
    plt.plot( b_freq[300,0,:].real, z[:], label='t=%f' %t[300])
    plt.plot( b_freq[399,0,:].real, z[:], label='t=%f' %t[399])
    plt.title('x=1.45')
    plt.legend()
    plt.xlabel('N2')
    plt.ylabel('z')
    plt.savefig('plots_7b/x=1.45_7b.png')
