import numpy as np

from learnmpm import element
from learnmpm import node
from learnmpm import particle
from learnmpm import shapefn

class Mesh1D:
    def __init__(self, domain_size, nelements):
        
        self.nodes = []       # List of nodes
        self.elements = []    # List of elements
        self.particles = []   # List of particles
        
        self.nelements = nelements    # Number of elements in mesh

        # Subsequent elements
        for i in range(nelements):
            # Create element
            el = element.Bar1D()
            el.id = i
            el.shapefn = shapefn.Linear1D()

            # Node 0 
            if i == 0: # First element
                el.nodes[0] = node.Node1D()
                el.nodes[0].id = 0
                self.nodes.append(el.nodes[0])

            else: # Subsequent elements connected to previous node
                el.nodes[0]=self.elements[i-1].nodes[1]
            

            # Node 1
            el.nodes[1] = node.Node1D()
            el.nodes[1].id = len(self.nodes)
            self.nodes.append(el.nodes[1])

            # Element length and coordinates
            length = domain_size/nelements
            el.size = np.array([length])
            el.nodes[0].x = np.array([i * length])
            el.nodes[1].x = np.array([el.nodes[0].x + length])
            
            self.elements.append(el)
        
    
    def generate_particles_mesh(self, ppc, material):
        # Iterate through each element
        for el in self.elements:
            # Compute particle mass
            pmass = el.size * material.density / ppc

            # Particle location in natural coordinates
            xis = el.shapefn.gauss_pts(ppc)
            
            # Nodal coordinates
            n0x = el.nodes[0].x
            n1x = el.nodes[1].x
            
            for xi in xis:
                # Compute the physical coordinates
                x = (n0x + n1x)/2 + (n1x - n0x)/2  * xi
                # Create particle
                prt = particle.Particle1D(pmass, x, xi, material)
                prt.id = len(self.particles)

                prt.shapefn = el.shapefn.sf(xi)
                prt.gradsf = el.shapefn.gradsf(xi)

                # Add reference to particle, element and mesh
                particle.element = el
                el.particles.append(prt)
                self.particles.append(prt)