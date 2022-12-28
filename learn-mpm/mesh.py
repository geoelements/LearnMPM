import numpy as np

from learn-mpm import element
from learn-mpm import node
from learn-mpm import particle

class Mesh1D:
    def __init__(self, domain_size, nelements):
        
        self.nodes = []       # List of nodes
        self.elements = []    # List of elements
        self.particles = []   # List of particles
        
        self.nelements = nelements    # Number of elements in mesh
        self.ppelem = 2       # particles per element

        # Subsequent elements
        for i in range(nelements):
            # Create element
            el = element.Bar1D()
            el.id = i
            
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
        
        print("Number of nodes: ", len(self.nodes))