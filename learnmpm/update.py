def compute_nodal_velocity(node, dt):
        # Total force
        f_total = node.f_int + node.f_ext + node.f_damp
        # Accleration 
        acc =  f_total / node.mass if node.mass > 0 else 0.
        # Velocity
        node.velocity += acc * dt

def compute_particle_position(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            nodal_velocity = 0
            for i in range(len(el.nodes)):
                nodal_velocity += prtcl.shapefn[i] * el.nodes[i].velocity
            prtcl.velocity = nodal_velocity
            prtcl.x += prtcl.velocity * dt

def update_particle_volume_density(prtcl):
        prtcl.volume *= (1 + prtcl.dstrain)
        prtcl.density = prtcl.density / (1 + prtcl.dstrain)


def compute_particle_stress(mesh):
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
            status, xi = el.compute_xi(xp)
            if (status):
                # Update particle xi
                prtcl.xi = xi
                # update element in particle
                prtcl.element = el
                # add the particle to the element list
                el.particles.append(prtcl)
                # break element loop for testing other particle
                break