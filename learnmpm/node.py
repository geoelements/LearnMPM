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

