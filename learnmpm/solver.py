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
    # create a dictionary of solution fields
    params.results = {}
    params.results['time'] = []
    for field in params.results_fields:
        params.results[field] = []

    # main simulation loop
    for i in range(params.nsteps):    
        # update particles list in each element
        update.locate_particles(mesh)

        # map particle mass and momentum to nodes
        interpolate.mass_momentum_to_nodes(mesh)

        # impose essential boundary conditions (in fixed nodes set mv=0)
        update.fix_nodal_bc_momentum(mesh)

        if params.mpm_scheme == 'USF':
            compute_stress(mesh, params)
            
        # particle internal force to nodes
        interpolate.internal_force_to_nodes(mesh)
        
        # particle external forces to nodes
        interpolate.external_force_to_nodes(mesh)

        # calculate total force in node
        update.nodal_total_force(mesh)
        
        # impose essential boundary conditions (in fixed nodes set f=m*a=0)
        update.fix_nodal_bc_force(mesh)
        
        # integrate the grid nodal momentum equation
        update.momentum_in_nodes(mesh, params.dt)

        # update particle velocity
        update.particle_velocity(mesh, params.dt)
        
        # update particle position
        update.particle_position(mesh, params.dt)

        #TODO: Fix velocity update
        # # calculate nodal acceleration and velocity
        # update.nodal_acceleration_velocity(mesh, params.dt)

        # # impose essential boundary conditions (in fixed nodes set f=m*a=0)
        # update.fix_nodal_bc_momentum(mesh)

        # # update particle position
        # update.particle_position_velocity(mesh, params.dt)

        if (params.mpm_scheme == 'MUSL'):
            # recalculate the nodal momentum
            update.nodal_momentum(mesh)
            # impose essential boundary conditions (in fixed nodes set v=0)
            update.fix_nodal_bc_momentum(mesh)
        
        # Modified Update Stress Last or Update Stress Last Scheme
        if (params.mpm_scheme == 'MUSL' or params.mpm_scheme == 'USL'):
            compute_stress(mesh, params)
            
        # reset all nodal values
        update.reset_nodal_values(mesh)
        
         # store data for plot
        params.results['time'].append(i*params.dt)
        
        #TODO: Fix 0 index
        #TODO: Fix particle indexing
        if 'velocity' in params.results_fields:
            params.results['velocity'].append(mesh.elements[-1].particles[-1].velocity[0])

        if 'position' in params.results_fields:
            params.results['position'].append(mesh.particles[params.solution_particle].x[0])
    