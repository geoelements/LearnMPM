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

        # calculate total force in node
        update.nodal_total_force(mesh)
        
        # impose essential boundary conditions (in fixed nodes set f=m*a=0)
        mesh.elements[0].nodes[0].f_total=0
        
        # integrate the grid nodal momentum equation
        update.momentum_in_nodes(mesh, params.dt)

        # update particle velocity
        update.particle_velocity(mesh, params.dt)
        
        # update particle position
        update.particle_position(mesh, params.dt)

        if (params.mpm_scheme == 'MUSL'):
            # recalculate the nodal momentum
            update.nodal_momentum(mesh)
            # impose essential boundary conditions (in fixed nodes v=0)
            mesh.elements[0].nodes[0].velocity=0
            mesh.elements[0].nodes[0].momentum=0
        
        # Modified Update Stress Last or Update Stress Last Scheme
        if (params.mpm_scheme == 'MUSL' or params.mpm_scheme == 'USL'):
            compute_stress(mesh, params)
            

        #TODO: Fix velocity update -> damped solution
        # # calculate nodal acceleration and velocity
        # update.nodal_acceleration_velocity(mesh, params.dt)

        # # impose essential boundary conditions (in fixed nodes set f=m*a=0)
        # mesh.elements[0].nodes[0].velocity = 0

        # # update particle position
        # update.particle_position_velocity(mesh, params.dt)
        
        # reset all nodal values
        update.reset_nodal_values(mesh)
        
         # store data for plot
        params.solution_array[0].append(i*params.dt)
        
        #TODO: Fix 0 index
        if params.solution_field=='velocity':
            params.solution_array[1].append(mesh.elements[-1].particles[-1].velocity[0])

        elif params.solution_field=='position':
            params.solution_array[1].append(mesh.particles[params.solution_particle].x[0])
    