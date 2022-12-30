import numpy as np

class Linear1D:
    def sf(self, xi):
        """
        Linear 1D shape function in natural coordinates
        """
        shapefn = np.array([0.5 * (1 - xi), 0.5 * (1 + xi)])
        return shapefn

    def gradsf(self, xi):
        """
        Linear 1D gradient of shape function in natural coordinates.
        """
        gradsf = np.array([-0.5, 0.5])
        return gradsf
    
    def dn_dx(self, xi, coords):
        length = abs(coords[0] - coords[1])
        # dN/dx = dN/dxi * dxi/dx
        return self.gradsf(xi) * 2. / length
    
    def gauss_pts(self, ngauss):
        if ngauss == 1:
            return np.array([0])
        elif ngauss == 2:
            return np.array([-1./np.sqrt(3), 1./np.sqrt(3)])
        elif ngauss == 3:
            return np.array([-np.sqrt(0.6), 0, np.sqrt(6)])
        else:
            return np.array([0])