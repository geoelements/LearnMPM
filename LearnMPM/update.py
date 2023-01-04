import numpy as np

def nodal_total_force(mesh):
    """
    Compute total force as sum of internal, external and damping force.

    Arguments:
        mesh: mesh
            a mesh object
    """
    for node in mesh.nodes:
        # Total force
        node.f_total = node.f_int + node.f_ext + node.f_damp

def nodal_acceleration_velocity(mesh, dt):
    """
    Compute nodal acceleration as :math:`a = f / m` and `v += a * dt`
        
    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for node in mesh.nodes:
        # Total force
        f_total = node.f_int + node.f_ext + node.f_damp
        # Accleration 
        node.acc =  f_total / node.mass if node.mass > 0 else 0.
        # Velocity
        node.velocity += node.acc * dt

def nodal_velocity(mesh):
    """Compute nodal velocity as :math:`v = mv / m`.

    Arguments:
        mesh: mesh
            a mesh object
    """
    for node in mesh.nodes:
        if(node.mass > 0.):
            node.velocity = node.momentum / node.mass

def fix_nodal_bc_momentum(mesh):
    """Set momentum and velocity to zero on specific boundary nodes.
    
    Arguments:
        mesh: mesh
            a mesh object
    """
    for nid in mesh.boundary_nodes:
        mesh.nodes[nid].momentum = 0
        mesh.nodes[nid].velocity = 0

def fix_nodal_bc_force(mesh):
    """Set nodal force to zero on specific boundary nodes.
    
    Arguments:
        mesh: mesh
            a mesh object
    """
    for nid in mesh.boundary_nodes:
        mesh.nodes[nid].f_total = 0

def momentum_in_nodes(mesh, dt):
    """Compute momentum in nodes. :math:`mv += force * dt`
    
    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for node in mesh.nodes:
        node.momentum += node.f_total * dt

def nodal_momentum(mesh):
    """
    Update nodal momentum :math:`(mv)_i = \sum_p N_i(x_p) * m_p * v_p`.

    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for node in mesh.nodes:
        node.momentum = 0
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                el.nodes[i].momentum += prtcl.mass * prtcl.velocity * prtcl.shapefn[i]

def reset_nodal_values(mesh):
    """Reset nodal values at the end of the iteration. Reset mesh.
    """
    for node in mesh.nodes:
        node.reset_values()
        
def particle_strain_increment(mesh,dt):
    """
    Particle strain increment. Compute strain based on nodal velocity. 

    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for particle in mesh.particles:
        particle.compute_strain(dt)
        
def particle_velocity(mesh, dt):
    """
    Compute particle velocity transfer nodal velocity to particle. :math:`v_p += \sum_i N_i(x_p) * {f_{total}}_i/m_i * dt`.

    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                prtcl.velocity += el.nodes[i].f_total/el.nodes[i].mass * prtcl.shapefn[i] * dt
       
def particle_position(mesh, dt):
    """
    Compute particle position based on nodal momentum to particle. :math:`x_p += \sum_i N_i(x_p) * {mv}_i/m_i * dt`.

    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for el in mesh.elements:
        for prtcl in el.particles:
            for i in range(el.nnodes):
                prtcl.x += el.nodes[i].momentum/el.nodes[i].mass * prtcl.shapefn[i] * dt

def particle_position_velocity(mesh, dt):
    """
    Compute particle position and velocity based on nodal velocity. :math:`x_p += \sum_i N_i(x_p) * v_i` and particle position :math:`x_p += v_p * dt`.

    Arguments:
        mesh: mesh
            a mesh object
        dt: float
            time step
    """
    for el in mesh.elements:
        for prtcl in el.particles:
            prtcl.velocity = 0
            for i in range(len(el.nodes)):
                prtcl.velocity += prtcl.shapefn[i] * el.nodes[i].velocity
            prtcl.x += prtcl.velocity * dt

def particle_volume_density(mesh):
    """
    Compute particle volume from :math:`V_p *= (1 + d\epsilon)` and :math:`density = density / (1 + \epsilon)`

    Arguments:
        mesh: mesh
            a mesh object
    """
    for prtcl in mesh.particles:
        prtcl.volume *= (1 + prtcl.dstrain)
        prtcl.density = prtcl.density / (1 + prtcl.dstrain)


def particle_stress(mesh):
    """Update particle stress based on dstrain.

    Arguments:
        mesh: mesh
            a mesh object
    """
    for particle in mesh.particles:
        particle.material.update_stress(particle)

def locate_particles(mesh):
    """Locate particle in the mesh and compute xi (natural coordinates) of the material points.
    
    Arguments:
        mesh: mesh
            a mesh object
    """
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