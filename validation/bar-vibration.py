# include the modules' path to the current path
import sys
sys.path.append("..")

# external modules
import matplotlib.pyplot as plt # for plot
import numpy as np # for sin

# local modules
from learnmpm import mesh
from learnmpm import material
from learnmpm import params as prms
from learnmpm import solver

# bar length
L = 25

# number of elements
nelements = 15

# create an 1D mesh
msh = mesh.Mesh1D(domain_size=L, nelements=nelements)

# define a linear material 
elastic = material.LinearElastic1D(E=100, density=1)

# put particles in mesh element and set the material
msh.generate_particles(ppc = 2, material = elastic)

# setup the model
params = prms.Params()
params.mpm_scheme = 'USF'
params.nsteps = 600
params.dt = 0.1
params.solution_particle = -1
params.solution_field = 'velocity'
params.damping = 0.0

# verify time step
dt_critical=msh.elements[0].size/(elastic.E/elastic.density)**0.5
params.dt = params.dt if params.dt < dt_critical else dt_critical

# impose initial condition in particles
vo = 0.1
b1 = np.pi/2.0/L
for prtcl in msh.particles:
  prtcl.velocity = vo * np.sin(b1 * prtcl.x)

# solve the problem in time
solver.explicit_solution(msh, params)
    
# plot mpm solution
plt.plot(params.solution_array[0], params.solution_array[1], 'ob', markersize = 2, label='mpm')

# plot the analytical solution
from analytical import continuum_bar_vibration as cbv
[anal_xt,anal_vt, anal_t] = cbv.continuum_bar_vibration_solution(L,elastic.E,elastic.density,params.dt * params.nsteps, params.dt,vo,msh.particles[params.solution_particle].x)
plt.plot(anal_t,anal_vt,'r',linewidth=2,label='analytical')

# configure axis, legends and show plot
plt.xlabel('time (s)')
plt.ylabel('velocity (m/s)')
plt.legend()
plt.show()