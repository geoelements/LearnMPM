import numpy as np

class Node1D:
    """1D MPM node
    Attributes:
        id: Index of node class.
        x: Location of node.
        mass: Mass at node.
        velocity: Velocity at node.
        momentum: Momentum at node.
        f_int: Internal force.
        f_ext: External force.
    """

    def __init__(self):
        self.id = None
        self.x = 0.
        self.mass = 0.
        self.velocity = 0.
        self.momentum = 0.
        self.f_int = 0.
        self.f_ext = 0.
        self.f_damp = 0.
    
    def compute_damping_force(self, alpha):
        # unbalanced nodal force magnitude
        unbalanced_force = self.f_int + self.f_ext
        # nodal velocity
        nodal_vel = self.momentum/self.mass
        if abs(nodal_vel)!=0:
            # velocity direction
            vel_direction = nodal_vel/abs(nodal_vel)                
            # damping force proportional to unbalanced forces and opposite to the nodal velocity
            self.f_damp = - alpha * abs(unbalanced_force) * vel_direction

    def compute_acceleration_velocity(self, dt):
        # Total force
        f_total = self.f_int + self.f_ext + self.f_damp
        # Accleration 
        if self.mass > 0:
            acc = f_total / self.mass
        # Velocity
        self.velocity += acc * dt

    def reset_values(self):
        self.mass     = 0
        self.velocity = 0
        self.momentum = 0
        self.f_int = 0
        self.f_ext = 0
        self.f_damp = 0

