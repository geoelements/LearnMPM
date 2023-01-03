"""Import class definitions into the LearnMPM package namespace."""

import logging

from .meta import __version__
from .element import Element1D
from .material import LinearElastic1D
from .mesh import Mesh1D
from .node import Node1D
from .params import Params
from .particle import Particle1D
from .shapefn import Linear1D

logging.getLogger('LearnMPM').addHandler(logging.NullHandler())
