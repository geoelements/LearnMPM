class Params:
    def __init__(self):
        self.interpolation_type = "linear"
        self.mpm_scheme = "USF"
        self.nsteps = 1000
        self.dt = 0
        self.results_particle = 0
        self.results_fields = ["position"]
        self.results = {}
        self.damping = 0