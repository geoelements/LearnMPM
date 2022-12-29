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
        self.dim = 1          # Dimension

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
        
    def put_particles_in_all_mesh_elements(self,ppelem,material):
        """
        Distributes particles in elements mesh
        
        Arguments
        ---------
        ppelem: int
            number of particles per element

        material: material
            a material object

        """
        self.ppelem=ppelem
            
        for el in range(len(self.elements)):
            
            el = self.elements[el]
            le = el.size
         
            ncoords = np.array([node.x for node in el.nodes])
            for _ in range(ppelem):
                
                # particle mass
                pmass = le * material.density/ppelem
                
                # particle position
                if(len(el.particles)==0):
                    xp=el.nodes[0].x + le/(2 * ppelem)
                    
                elif(len(el.particles)==(ppelem-1)):
                    xp=el.nodes[1].x - le/(2 * ppelem)   
                
                else:
                    xp=el.nodes[0].x + le/(2 * ppelem) + len(el.particles) * (le/ppelem)
                
                _, xi = el.compute_xi(xp)
                    
                # create particle
                ip = particle.Particle1D(pmass,xp, xi, material)
                ip.id=len(self.particles)
                ip.shapefn = el.shapefn.sf(xi)
                ip.dn_dx = el.shapefn.dn_dx(xi, ncoords)
                
                # set the element in the particle
                ip.element=el

                # append in elements
                el.particles.append(ip)                
                                
                # append in mesh
                self.particles.append(ip)

    def generate_particles(self, ppc, material):
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
                