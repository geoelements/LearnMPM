import numpy as np

class Node1D:
    """1D MPM node

    Attributes:
        id: int
            Index of node class.

        x: float
            Location of node.
        
        mass: float
            Mass at node.
        
        velocity: float
            Velocity at node.
        
        momentum: float
            Momentum at node.
        
        f_int: float
            Internal force.
        
        f_ext: float
            External force.
        
        f_damp: float
            Damping force at the node.
        
        f_total: float
            Total nodal force.
    """

    def __init__(self):
        self.id       = None
        self.x        = 0.
        self.mass     = 0.
        self.velocity = 0.
        self.acc      = 0.
        self.momentum = 0.
        self.f_int    = 0.
        self.f_ext    = 0.
        self.f_damp   = 0.
        self.f_total  = 0.
    
    def compute_damping_force(self, alpha):
        """Compute the nodal damping force based on the nodal unbalanced forces.

        Arguments:
            alpha: Damping coefficient.
        """
        # unbalanced nodal force magnitude
        unbalanced_force = self.f_int + self.f_ext
        # nodal velocity
        nodal_vel = self.momentum/self.mass
        if abs(nodal_vel)!=0:
            # velocity direction
            vel_direction = nodal_vel/abs(nodal_vel)                
            # damping force proportional to unbalanced forces and opposite to the nodal velocity
            self.f_damp = - alpha * abs(unbalanced_force) * vel_direction

    def reset_values(self):
        """Reset nodal values to zero at the end of time step.
        """
        self.mass     = 0.
        self.velocity = 0.
        self.acc      = 0.
        self.momentum = 0.
        self.f_int    = 0.
        self.f_ext    = 0.
        self.f_damp   = 0.
        self.f_total  = 0.
