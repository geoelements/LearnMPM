from learnmpm import update
from learnmpm import interpolate

def compute_stress(mesh, params):
    # calculate the grid nodal velocity
    update.nodal_velocity(mesh)

    # calculate particle strain increment
    update.particle_strain_increment(mesh, params.dt)
    
    # update particle volume and density
    update.particle_volume_density(mesh)

    # update particle stress
    update.particle_stress(mesh)
    
# Update Stress First Scheme
def explicit_solution(mesh, params):
    # main simulation loop
    for i in range(params.nsteps):    
        # update particles list in each element
        update.locate_particles(mesh)

        # map particle mass and momentum to nodes
        interpolate.mass_momentum_to_nodes(mesh)

        # impose essential boundary conditions (in fixed nodes set mv=0)
        mesh.elements[0].nodes[0].momentum = 0
        
        if params.mpm_scheme == 'USF':
            compute_stress(mesh, params)
            
        # particle internal force to nodes
        interpolate.internal_force_to_nodes(mesh)
        
        # particle external forces to nodes
        interpolate.external_force_to_nodes(mesh)

        # calculate nodal acceleration and velocity
        update.nodal_acceleration_velocity(mesh, params.dt)
        
        # impose essential boundary conditions (in fixed nodes set f=m*a=0)
        mesh.elements[0].nodes[0].velocity = 0

         # store data for plot
        params.solution_array[0].append(i*params.dt)
        
        if params.solution_field=='velocity':
            params.solution_array[1].append(mesh.particles[params.solution_particle].velocity)
        
        elif params.solution_field=='position':
            params.solution_array[1].append(mesh.particles[params.solution_particle].position)
        
     
        # update particle position
        update.particle_position_velocity(mesh, params.dt)
        
        # reset all nodal values
        update.reset_nodal_values(mesh)