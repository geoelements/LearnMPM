def map_mass_momentum_to_nodes(mesh):
	for el in mesh.elements:
		for par in el.particles:
            for i in range(len(el.nodes)):
                el.nodes[i].mass += par.mass * par.shapefn[i]
                el.nodes[i].momentum += par.mass * par.shapefn[i] * par.velocity


def map_body_force_to_nodes(mesh, gravity):
	for el in mesh.elements:
		for par in el.particles:
            for i in range(len(el.nodes)):
                el.nodes[i].f_ext += par.mass * par.shapefn[i] * gravity

def internal_force_to_nodes(msh):
	for el in mesh.elements:
		for par in el.particles:
            for i in range(len(el.nodes)):
			     el.nodes[i].f_int -= par.gradsf[i] * par.stress * par.mass / par.density

def external_force_to_nodes(msh):
	for el in mesh.elements:
		for par in el.particles:
            for i in range(len(el.nodes)):
			     el.nodes[i].f_int += par.shapefn[i] * par.f_ext
			