def nodal_acceleration_velocity(node, dt):
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

def particle_strain_increment(mesh,dt):
    for particle in mesh.particles:
        particle.compute_strain(particle, dt)
        

def particle_position_velocity(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            nodal_velocity = 0
            for i in range(len(el.nodes)):
                nodal_velocity += prtcl.shapefn[i] * el.nodes[i].velocity
            prtcl.velocity = nodal_velocity
            prtcl.x += prtcl.velocity * dt

def particle_volume_density(prtcl):
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
            if (prcl_in_cell):
                # update particle xi
                prtcl.xi = xi
                # update element in particle
                prtcl.element = el
                # update particle shapefns and grads
                prtcl.shapefn = el.shapefn.sf(xi)
                prtcl.gradsf = el.shapefn.gradsf(xi)
                # add the particle to the element list
                el.particles.append(prtcl)
                # break element loop for testing other particle
                break