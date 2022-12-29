class Params:
    def __init__(self):
        self.interpolation_type = "linear"
        self.integration_scheme = "USF"
        self.nsteps = 1000
        self.dt = 0
        self.solution_particle = 0
        self.solution_field = "position"
        self.solution_array = [[],[]]
        self.damping_local_alpha = 0