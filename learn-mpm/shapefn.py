import numpy as np

def Linear1DShapefn(xi):
    """
    Linear 1D shape function in natural coordinates
    """
    shapefn = np.array([0.5 * (1 - xi), 0.5 * (1 + xi)])
    return shapefn


def Linear1DGradsf(xi):
    """
    Linear 1D gradient of shape function in natural coordinates.
    """
    gradsf = np.array([-0.5, 0.5])
    return gradsf