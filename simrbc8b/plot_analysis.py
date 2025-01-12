import h5py
import matplotlib.pyplot as plt
import numpy as np
import dedalus.public as d3

# Open the HDF5 file and perform operations within this block
with h5py.File("analysis/analysis_s1.h5", mode='r') as file:
    # Load datasets
    b_freq = file['tasks']['N2 x=1']
    t = b_freq.dims[0]['sim_time']
    z = b_freq.dims[2][0]

    # Convert datasets to numpy arrays
    b_freq_data = b_freq[:].real
    t_data = np.array(t)
    z_data = np.array(z)

    average_t=np.mean(b_freq[0:40:1,0,:].real, axis=0)
    average_t1=np.mean(b_freq[40:80:1,0,:].real, axis=0)
    average_t2=np.mean(b_freq[80:120:1,0,:].real, axis=0)
    average_t3=np.mean(b_freq[120:160:1,0,:].real, axis=0)
    average_t4=np.mean(b_freq[160:199:1,0,:].real, axis=0)
    # Plot data
    fig = plt.figure(figsize=(6, 4), dpi=100)
    plt.plot(average_t, z[:], label='t=0-40')
    plt.plot(average_t1, z[:], label='t=40-80')
    plt.plot(average_t2, z[:], label='t=80-120')
    plt.plot(average_t3, z[:], label='t=120-160')
    plt.plot(average_t4, z[:], label='t=160-199')
    plt.title('average t values at x=1')
    plt.legend()
    plt.xlabel('N2')
    plt.ylabel('z')
    plt.legend()
    #plt.xlim([-10,5])
    plt.savefig('plot_8b/all_average_t_x=1_rbc8b.png')

