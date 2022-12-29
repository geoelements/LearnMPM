import numpy as np

def nodal_total_force(mesh):
    for node in mesh.nodes:
        # Total force
        node.f_total = node.f_int + node.f_ext + node.f_damp

def nodal_acceleration_velocity(mesh, dt):
    for node in mesh.nodes:
        # Total force
        f_total = node.f_int + node.f_ext + node.f_damp
        # Accleration 
        acc =  f_total / node.mass if node.mass > 0 else 0.
        # Velocity
        node.velocity += acc * dt

def nodal_velocity(mesh):
    for node in mesh.nodes:
        if(node.mass > 0.):
            node.velocity = node.momentum / node.mass

def momentum_in_nodes(mesh, dt):
    for node in mesh.nodes:
        node.momentum += node.f_total * dt

def nodal_momentum(mesh):
    for node in mesh.nodes:
        node.momentum = 0
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                el.nodes[i].momentum += prtcl.mass * prtcl.velocity * prtcl.shapefn[i]

def reset_nodal_values(mesh):
    for node in mesh.nodes:
        node.reset_values()
        
def particle_strain_increment(mesh,dt):
    for particle in mesh.particles:
        particle.compute_strain(dt)
        
def particle_velocity(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                prtcl.velocity += el.nodes[i].f_total/el.nodes[i].mass * prtcl.shapefn[i] * dt
       
def particle_position(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                prtcl.x += el.nodes[i].momentum/el.nodes[i].mass * prtcl.shapefn[i] * dt

def particle_position_velocity(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            # nodal_velocity = 0
            prtcl.velocity = 0
            for i in range(len(el.nodes)):
                prtcl.velocity += prtcl.shapefn[i] * el.nodes[i].velocity
            # prtcl.velocity = nodal_velocity
            prtcl.x += prtcl.velocity * dt

def particle_volume_density(mesh):
    for prtcl in mesh.particles:
        prtcl.volume *= (1 + prtcl.dstrain)
        prtcl.density = prtcl.density / (1 + prtcl.dstrain)


def particle_stress(mesh):
    for particle in mesh.particles:
        particle.material.update_stress(particle)

def locate_particles(mesh):
    # clear particle list in elements
    for element in mesh.elements:
        element.particles = []
   
    for prtcl in mesh.particles:
        # get particle position
        xp = prtcl.x
        # for each element in mesh
        for el in mesh.elements:
            # verify the particle is inside the element
            prcl_in_cell, xi = el.compute_xi(xp)
            ncoords = np.array([node.x for node in el.nodes])
            
            if (prcl_in_cell):
                # update particle xi
                prtcl.xi = xi
                # update element in particle
                prtcl.element = el
                # update particle shapefns and grads
                prtcl.shapefn = el.shapefn.sf(xi)
                prtcl.dn_dx = el.shapefn.dn_dx(xi, ncoords)
                # add the particle to the element list
                el.particles.append(prtcl)
                # break element loop for testing other particle
                break