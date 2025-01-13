import h5py
import matplotlib.pyplot as plt
import numpy as np
import os #operating systems to create directories aand file paths

# List of directories consisting of  the analysis files
directories = ["simrbc6b","simrbc7b","simrbc8b", "simrbc9b", "simrbc10b"]

# List of labels corresponding to each directory
labels = ["Ra=2e6", "Ra=2e7", "Ra=2e8", "Ra=2e9", "Ra=2e10"]

# Initialize figure for plotting
fig = plt.figure(figsize=(6, 4), dpi=100)

# Loop through each directory and process the corresponding file
for dir, label in zip(directories, labels):
    file_path = os.path.join(dir, "analysis", "analysis_s1.h5")
    
    if os.path.exists(file_path):
        with h5py.File(file_path, mode='r') as file:
            # Load datasets
            b_freq = file['tasks']['N2 x=1']
            t = b_freq.dims[0]['sim_time']
            z = b_freq.dims[2][0]

            # Calculate averages over different time intervals
            average_t = np.mean(b_freq[200:399:1,0,:].real, axis=0)
           # average_t1 = np.mean(b_freq[40:80:1,0,:].real, axis=0)
           # average_t2 = np.mean(b_freq[80:120:1,0,:].real, axis=0)
           # average_t3 = np.mean(b_freq[120:160:1,0,:].real, axis=0)
           #average_t4 = np.mean(b_freq[160:199:1,0,:].real, axis=0)
            
            # Plot data
            plt.plot(average_t, z[:], label=label)
           #plt.plot(average_t1, z[:], label=f'{dir} t=40-80')
           #plt.plot(average_t2, z[:], label=f'{dir} t=80-120')
           #plt.plot(average_t3, z[:], label=f'{dir} t=120-160')
           #plt.plot(average_t4, z[:], label=f'{dir} t=160-199')
    else:
        print(f"File {file_path} not found.")

# Add titles and labels
plt.title('Average t [200-400] values at x=1 from multiple simulations')
plt.xlabel('N2')
plt.ylabel('z')
plt.xlim([-1, 2])
plt.legend()
plt.savefig('plots/updated_average_t_x=1_all_rbc.png')
