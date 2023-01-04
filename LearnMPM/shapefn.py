import numpy as np

class Linear1D:
    """Define linear 1D shape function for element.

    """
    def sf(self, xi):
        """
        Linear 1D shape function in natural coordinates.

        Arguments:
            xi: float
                location in natural coordinates
        
        Returns:
            shape function of 1D linear element in natural coords.
        """
        shapefn = np.array([0.5 * (1 - xi), 0.5 * (1 + xi)])
        return shapefn

    def gradsf(self, xi):
        """
        Linear 1D gradient of shape function in natural coordinates.
        
        Arguments:
            xi: float
                location in natural coordinates
        
        Returns:
            Gradient of shape function of 1D linear element.
        """
        gradsf = np.array([-0.5, 0.5])
        return gradsf
    
    def dn_dx(self, xi, coords):
        """
        Linear 1D gradient of shape function in physical coordinates.

        Arguments:
            xi: float
                location in natural coordinates
            coords: array
                Nodal coordinates

        Returns:
            Gradient of 1D shape fn in physical coords at xi
        """
        length = abs(coords[0] - coords[1])
        # dN/dx = dN/dxi * dxi/dx
        return self.gradsf(xi) * 2. / length
    
    def gauss_pts(self, ngauss):
        """
        Gauss point coordinates of an element

        Arguments:
            ngauss: int
                Number of gauss points
        
        Returns:
            Location of gauss points in the element
        """
        if ngauss == 1:
            return np.array([0])
        elif ngauss == 2:
            return np.array([-1./np.sqrt(3), 1./np.sqrt(3)])
        elif ngauss == 3:
            return np.array([-np.sqrt(0.6), 0, np.sqrt(6)])
        else:
            return np.array([0])