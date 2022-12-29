def compute_particle_position(mesh, dt):
    for el in mesh.elements:
        for prtcl in el.particles:
            nodal_velocity = 0
            for i in range(len(el.nodes)):
                nodal_velocity += prtcl.shapefn[i] * el.nodes[i].velocity
            prtcl.velocity = nodal_velocity
            prtcl.x += prtcl.velocity * dt

def update_volume_density(prtcl):
        prtcl.volume *= (1 + prtcl.dstrain)
        prtcl.density = prtcl.density / (1 + prtcl.dstrain)
