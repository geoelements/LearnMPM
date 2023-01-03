# include the modules' path to the current path
import sys
sys.path.append("..")

from LearnMPM import element
from LearnMPM import node

def test_element_init():
    el = element.Bar1D()
    assert el.id == None
    assert el.nodes == [None, None]
    assert el.nnodes == 2
    assert el.size == 0.0
    assert el.particles == []
    assert el.shapefn == None

    el.id = 0
    assert el.id == 0

    el.nodes[0] = node.Node1D()
    el.nodes[0].id = 0
    el.nodes[0].x = 0

    el.nodes[1] = node.Node1D()
    el.nodes[1].id = 1
    el.nodes[1].x = 1
    assert len(el.nodes) == 2

    el.size = abs(el.nodes[1].x - el.nodes[0].x)
    assert el.size == 1.0

    el.particles.append(0)
    el.particles.append(1)
    assert el.particles == [0, 1]

def test_coordinates():
    el = element.Bar1D()
    el.id = 0
    assert el.id == 0

    el.nodes[0] = node.Node1D()
    el.nodes[0].id = 0
    el.nodes[0].x = 0

    el.nodes[1] = node.Node1D()
    el.nodes[1].id = 1
    el.nodes[1].x = 1
    assert len(el.nodes) == 2

    el.size = abs(el.nodes[1].x - el.nodes[0].x)
    assert el.size == 1.0
    # is point in element
    status = el.is_point_in_element(0.5)
    assert status == True
    status = el.is_point_in_element(-0.5)
    assert status == False
    status = el.is_point_in_element(0.)
    assert status == True
    status = el.is_point_in_element(1.0)
    assert status == False
    # compute xi
    status, xi = el.compute_xi(0.5)
    assert status == True
    assert xi == 0.0
    status, xi = el.compute_xi(0.)
    assert status == True
    assert xi == -1.0
    status, xi = el.compute_xi(0.99999)
    assert status == True
    assert round(xi,3) == 1.0



test_element_init()
test_coordinates()
    