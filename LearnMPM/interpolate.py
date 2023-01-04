r"""Map quantities from particles to nodes using a interpolation function. This functions, have the general form:
	
.. math::
	\phi_i = \sum_p N_i(x_p) \phi_p

where,

:math:`\phi_i` is a nodal quantity,


:math:`\phi_p` is a particle quantity, and

:math:`N_i(x_p)` is the terpolation function of the node *i* evaluated at particle position :math:`x_p`.

"""

def mass_momentum_to_nodes(mesh):
	"""Map mass and momentum of particles in the elements to the associated nodes.

        Args:
            mesh: mesh object with nodes, elements and particles
	"""
	for el in mesh.elements:
		for par in el.particles:
			for i in range(len(el.nodes)):
				el.nodes[i].mass += par.mass * par.shapefn[i]
				el.nodes[i].momentum += par.mass * par.shapefn[i] * par.velocity         

def body_force_to_nodes(mesh, gravity):
	"""Compute body force at the nodes. The external force :math:`f_{ext} = \sum_i N_i * m_p * g`.

        Args:
            mesh: mesh object with nodes, elements and particles
	"""
	for el in mesh.elements:
		for par in el.particles:
			for i in range(len(el.nodes)):
				el.nodes[i].f_ext += par.mass * par.shapefn[i] * gravity

def internal_force_to_nodes(mesh):
	"""Map internal force to nodes. The nodal stresses are mapped to the nodes as internal force. The nodal internal force :math:`f_{int} = -\sum_i dN_i \sigma_p m_p / P_p`.

        Args:
            mesh: mesh object with nodes, elements and particles	
	"""
	for el in mesh.elements:
		for par in el.particles:
			for i in range(len(el.nodes)):
			     el.nodes[i].f_int -= par.dn_dx[i] * par.stress * par.mass / par.density

def external_force_to_nodes(mesh):
	"""Map external force of the particles to the nodes. The nodal external force :math:`f_{ext} = \sum_i N_i * {f_{ext}}_p`.

        Args:
            mesh: mesh object with nodes, elements and particles	
	"""
	for el in mesh.elements:
		for par in el.particles:
			for i in range(len(el.nodes)):
			     el.nodes[i].f_ext += par.shapefn[i] * par.f_ext
