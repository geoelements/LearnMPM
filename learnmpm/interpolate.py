def map_mass_momentum_to_nodes(mesh):
	for el in mesh.elements:
		for par in el.particles:
            for i in range(len(el.nodes)):
                el.nodes[i].mass += par.mass * par.shapefn[i]
                el.nodes[i].momentum += par.mass * par.shapefn[i] * par.velocity
                