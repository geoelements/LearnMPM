
# include the modules' path to the current path
import sys
sys.path.append("..")

from LearnMPM import mesh
from LearnMPM import material
from LearnMPM import interpolate

def test_mesh_init():
    msh = mesh.Mesh1D(10,1)
    assert len(msh.nodes) == 2
    
    msh = mesh.Mesh1D(10,2)
    assert len(msh.nodes) == 3
    
def test_mesh_particles_uniform():
    msh = mesh.Mesh1D(10,1)
    assert len(msh.nodes) == 2
    assert len(msh.elements) == 1
    le = material.LinearElastic1D(1e5, 1800)

    assert len(msh.particles) == 0
    msh.generate_particles_uniform(2, le)
    assert len(msh.particles) == 2

def test_mesh_particles_gauss():
    msh = mesh.Mesh1D(10,2)
    assert len(msh.nodes) == 3
    assert len(msh.elements) == 2
    le = material.LinearElastic1D(1e5, 1800)

    assert len(msh.particles) == 0
    msh.generate_particles_uniform(2, le)
    assert len(msh.particles) == 4

def test_mesh_interpolate():
    msh = mesh.Mesh1D(10,2)
    le = material.LinearElastic1D(1e5, 1800)
    assert len(msh.particles) == 0
    msh.generate_particles_uniform(2, le)
    assert len(msh.particles) == 4
    interpolate.mass_momentum_to_nodes(msh)

test_mesh_init()
test_mesh_particles_uniform()
test_mesh_particles_gauss()
test_mesh_interpolate()