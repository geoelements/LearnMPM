import numpy as np

from LearnMPM import element
from LearnMPM import node
from LearnMPM import particle
from LearnMPM import shapefn

class Mesh1D:
    """
    1D Mesh class with nodes, elements and particles. 

    Attributes:

    nodes: List
        List of nodes

    elements: List
        List of elements

    particles: List
        List of particles
    
    boundary_nodes: List
        Node ids of the boundary nodes

    nelements: int
        Number of elements in the mesh
    
    dim: int
        Dimension of Mesh (1D)
    """
    def __init__(self, domain_size, nelements):
        self.nodes = []       # List of nodes
        self.elements = []    # List of elements
        self.particles = []   # List of particles
        self.boundary_nodes = []      # List of boundary nodes
        self.nelements = nelements    # Number of elements in mesh
        self.dim = 1                  # Dimension

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
            el.nodes[0].x = i * length
            el.nodes[1].x = el.nodes[0].x + length
            self.elements.append(el)
        
    def generate_particles_uniform(self, ppc, material):
        """
        Distributes particles uniformly across all elements in the mesh
        
        Arguments
        ---------
        ppc: int
            number of particles per cell

        material: material
            a material object
        """
            
        for el in range(len(self.elements)):
            el = self.elements[el]
            length = el.size
            ncoords = np.array([node.x for node in el.nodes])
            for _ in range(ppc):
                # particle mass
                pmass = length * material.density/ppc
                
                # particle position
                if(len(el.particles)==0):
                    xp=el.nodes[0].x + length/(2 * ppc)
                elif(len(el.particles)==(ppc - 1)):
                    xp=el.nodes[1].x - length/(2 * ppc)
                else:
                    xp=el.nodes[0].x + length/(2 * ppc) + len(el.particles) * (length/ppc)
                
                _, xi = el.compute_xi(xp)
                    
                # create particle
                prtcl = particle.Particle1D(pmass,xp, xi, material)
                prtcl.id=len(self.particles)
                prtcl.shapefn = el.shapefn.sf(xi)
                prtcl.dn_dx = el.shapefn.dn_dx(xi, ncoords)
                
                # set the element in the particle
                prtcl.element=el

                # append particle to current element
                el.particles.append(prtcl)                
                                
                # append in mesh
                self.particles.append(prtcl)

    def generate_particles_gauss(self, ppc, material):
        """
        Distributes particles at Gauss locations in the elements.
        
        Arguments
        ---------
        ppc: int
            number of particles per cell

        material: material
            a material object
        """        
        # Iterate through each element
        for el in self.elements:
            # Compute particle mass
            psize = el.size / ppc
            pmass = psize * material.density

            # Particle location in natural coordinates
            xis = el.shapefn.gauss_pts(ppc)
            
            # Nodal coordinates
            n0x = el.nodes[0].x
            n1x = el.nodes[1].x
            ncoords = np.array([node.x for node in el.nodes])
            for xi in xis:
                # Compute the physical coordinates
                x = (n0x + n1x)/2 + (n1x - n0x)/2  * xi
                # Create particle
                prt = particle.Particle1D(pmass, x, xi, material)
                prt.id = len(self.particles)
                prt.volume = psize
                prt.shapefn = el.shapefn.sf(xi)
                prt.dn_dx = el.shapefn.dn_dx(xi, ncoords)

                # Add reference to particle, element and mesh
                particle.element = el
                el.particles.append(prt)
                self.particles.append(prt)
                