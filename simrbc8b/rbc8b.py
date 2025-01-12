"""
Dedalus script simulating 2D horizontally-periodic Rayleigh-Benard convection.
This script demonstrates solving a 2D Cartesian initial value problem. It can
be ran serially or in parallel, and uses the built-in analysis framework to save
data snapshots to HDF5 files. The `plot_snapshots.py` script can be used to
produce plots from the saved data. It should take about 5 cpu-minutes to run.

The problem is non-dimensionalized using the box height and freefall time, so
the resulting thermal diffusivity and viscosity are related to the Prandtl
and Rayleigh numbers as:

    kappa = (Rayleigh * Prandtl)**(-1/2)
    nu = (Rayleigh / Prandtl)**(-1/2)

For incompressible hydro with two boundaries, we need two tau terms for each the
velocity and buoyancy. Here we choose to use a first-order formulation, putting
one tau term each on auxiliary first-order gradient variables and the others in
the PDE, and lifting them all to the first derivative basis. This formulation puts
a tau term in the divergence constraint, as required for this geometry.

To run and plot using e.g. 4 processes:
    $ mpiexec -n 4 python3 rayleigh_benard.py
    $ mpiexec -n 4 python3 plot_snapshots.py snapshots/*.h5
"""
#import pathlib
import subprocess
#import h5py
#import matplotlib.pyplot as plt
import numpy as np
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)


# Parameters
Lx, Lz = 4, 1
Nx, Nz = 1024, 256
Rayleigh = 2e8
Prandtl = 1
dealias = 3/2
stop_sim_time = 200
stop_wall_time = 60*60*60
timestepper = d3.RK222
max_timestep = 0.125
dtype = np.float64

# Bases
coords = d3.CartesianCoordinates('x', 'z')
dist = d3.Distributor(coords, dtype=dtype)
xbasis = d3.RealFourier(coords['x'], size=Nx, bounds=(0, Lx), dealias=dealias)
zbasis = d3.ChebyshevT(coords['z'], size=Nz, bounds=(0, Lz), dealias=dealias)

# Fields
p = dist.Field(name='p', bases=(xbasis,zbasis))
b = dist.Field(name='b', bases=(xbasis,zbasis))
u = dist.VectorField(coords, name='u', bases=(xbasis,zbasis))
tau_p = dist.Field(name='tau_p')
tau_b1 = dist.Field(name='tau_b1', bases=xbasis)
tau_b2 = dist.Field(name='tau_b2', bases=xbasis)
tau_u1 = dist.VectorField(coords, name='tau_u1', bases=xbasis)
tau_u2 = dist.VectorField(coords, name='tau_u2', bases=xbasis)
b_bot = dist.Field(name='b_bot', bases=xbasis)

# Substitutions
kappa = (Rayleigh * Prandtl)**(-1/2)
nu = (Rayleigh / Prandtl)**(-1/2)
x, z = dist.local_grids(xbasis, zbasis)
ex, ez = coords.unit_vector_fields(dist)
lift_basis = zbasis.derivative_basis(1)
lift = lambda A: d3.Lift(A, lift_basis, -1)
grad_u = d3.grad(u) + ez*lift(tau_u1) # First-order reduction
grad_b = d3.grad(b) + ez*lift(tau_b1) # First-order reduction

# Problem
# First-order form: "div(f)" becomes "trace(grad_f)"
# First-order form: "lap(f)" becomes "div(grad_f)"
problem = d3.IVP([p, b, u, tau_p, tau_b1, tau_b2, tau_u1, tau_u2], namespace=locals())
problem.add_equation("trace(grad_u) + tau_p = 0")
problem.add_equation("dt(b) - kappa*div(grad_b) + lift(tau_b2) = - u@grad(b)")
problem.add_equation("dt(u) - nu*div(grad_u) + grad(p) - b*ez + lift(tau_u2) = - u@grad(u)")
problem.add_equation("b(z=0) = b_bot") #function of x wait
problem.add_equation("u(z=0) = 0")
problem.add_equation("b(z=1) = 1")
problem.add_equation("u(z=Lz) = 0")
problem.add_equation("integ(p) = 0") # Pressure gauge
# Solver
solver = problem.build_solver(timestepper)
solver.stop_sim_time = stop_sim_time
solver.stop_wall_time = stop_wall_time


# Initial conditions
b.fill_random('g', seed=42, distribution='normal', scale=1e-3) # Random noise
b['g'] *= z * (Lz - z) #Damp noise at walls
b['g'] += z # Add linear background
b_bot['g'] = 1/2*( np.tanh( (x-1.75)/0.1 ) - np.tanh( (x-2.25)/0.1 ) )
#N2 = np.array(f['tasks/N2 center']) #what is f again?
#N2 = N2[:, 0, :]


# Analysis
snapshots = solver.evaluator.add_file_handler('snapshots', sim_dt=0.25)
snapshots.add_task(b, name='buoyancy')
snapshots.add_task(-d3.div(d3.skew(u)), name='vorticity')

analysis = solver.evaluator.add_file_handler('analysis', sim_dt=0.5)
analysis.add_task((d3.grad(b)@ez)(x=2.5), name="N2 x=2.5") #still have dimension issues
analysis.add_task((d3.grad(b)@ez)(x=1.5), name="N2 x=1.5")
analysis.add_task((d3.grad(b)@ez)(x=1), name="N2 x=1")
analysis.add_task((d3.grad(b)@ez)(x=2), name="N2 x=2")
analysis.add_task((d3.grad(b)@ez)(x=3), name="N2 x=3")
analysis.add_task((d3.grad(b)@ez)(x=4), name="N2 x=4")
#np.mean(b, axis=0) #out of bounds issues

#below 1.5
analysis.add_task((d3.grad(b)@ez)(x=1.15), name="N2 x=1.15")
analysis.add_task((d3.grad(b)@ez)(x=1.25), name="N2 x=1.25")
analysis.add_task((d3.grad(b)@ez)(x=1.35), name="N2 x=1.35")
analysis.add_task((d3.grad(b)@ez)(x=1.45), name="N2 x=1.45")

#interesting so lets look more
analysis.add_task((d3.grad(b)@ez)(x=2.45), name="N2 x=2.45")
analysis.add_task((d3.grad(b)@ez)(x=2.35), name="N2 x=2.35")
analysis.add_task((d3.grad(b)@ez)(x=2.25), name="N2 x=2.25")
analysis.add_task((d3.grad(b)@ez)(x=2.15), name="N2 x=2.15")
analysis.add_task((d3.grad(b)@ez)(x=1.75), name="N2 x=1.75")
analysis.add_task((d3.grad(b)@ez)(x=1.65), name="N2 x=1.65")
analysis.add_task((d3.grad(b)@ez)(x=1.85), name="N2 x=1.85")
analysis.add_task((d3.grad(b)@ez)(x=1.95), name="N2 x=1.95")

#between 0 to 1 now
analysis.add_task((d3.grad(b)@ez)(x=.15), name="N2 x=.15")
analysis.add_task((d3.grad(b)@ez)(x=.25), name="N2 x=.25")
analysis.add_task((d3.grad(b)@ez)(x=.35), name="N2 x=.35")
analysis.add_task((d3.grad(b)@ez)(x=.45), name="N2 x=.45")
analysis.add_task((d3.grad(b)@ez)(x=.50), name="N2 x=.50")
analysis.add_task((d3.grad(b)@ez)(x=.65), name="N2 x=.65")
analysis.add_task((d3.grad(b)@ez)(x=.75), name="N2 x=.75")
analysis.add_task((d3.grad(b)@ez)(x=.85), name="N2 x=.85")
analysis.add_task((d3.grad(b)@ez)(x=.95), name="N2 x=.95")

#between 3 to 4 now
analysis.add_task((d3.grad(b)@ez)(x=3.15), name="N2 x=3.15")
analysis.add_task((d3.grad(b)@ez)(x=3.25), name="N2 x=3.25")
analysis.add_task((d3.grad(b)@ez)(x=3.35), name="N2 x=3.35")
analysis.add_task((d3.grad(b)@ez)(x=3.45), name="N2 x=3.45")
analysis.add_task((d3.grad(b)@ez)(x=3.50), name="N2 x=3.50")
analysis.add_task((d3.grad(b)@ez)(x=3.65), name="N2 x=3.65")
analysis.add_task((d3.grad(b)@ez)(x=3.75), name="N2 x=3.75")
analysis.add_task((d3.grad(b)@ez)(x=3.85), name="N2 x=3.85")
analysis.add_task((d3.grad(b)@ez)(x=3.95), name="N2 x=3.95")


# CFL
CFL = d3.CFL(solver, initial_dt=max_timestep, cadence=10, safety=0.3, threshold=0.05,
             max_change=1.5, min_change=0.5, max_dt=max_timestep)
CFL.add_velocity(u)

# Flow properties
flow = d3.GlobalFlowProperty(solver, cadence=10)
flow.add_property(np.sqrt(u@u)/nu, name='Re')

# Main loop
startup_iter = 10
try:
    logger.info('Starting main loop')
    while solver.proceed:
        timestep = CFL.compute_timestep()
        solver.step(timestep)
        if (solver.iteration-1) % 10 == 0:
            max_Re = flow.max('Re')
            logger.info('Iteration=%i, Time=%e, dt=%e, max(Re)=%f' %(solver.iteration, solver.sim_time, timestep, max_Re))
except:
    logger.error('Exception raised, triggering end of main loop.')
    raise
finally:
    solver.log_stats()

#post-processing step starts here
print(subprocess.check_output("find analysis | sort", shell=True).decode())


    
