class Params:
    """
    Configuration object for handling MPM simulation
    
    Attributes:

        interpolation_type : string
            interpolation function type 'linear'
        
        integration_scheme : string
            material point method integration scheme, can be 'USL', 'USF' or 'MUSL'
        
        nsteps : float
            Total number of simulation steps

        dt : float
            time step

        results_particle : integer
            index of the particle to get the solution

        results_fields : string
            solution fields (position or velocity)

        results: array
            array to store the results wrt time

        damping: float
            alpha local damping factor proportional to the total nodal force
    
    """

    def __init__(self):
        self.interpolation_type = "linear"
        self.mpm_scheme = "USF"
        self.nsteps = 1000
        self.dt = 0
        self.results_particle = 0
        self.results_fields = ["position"]
        self.results = {}
        self.damping = 0