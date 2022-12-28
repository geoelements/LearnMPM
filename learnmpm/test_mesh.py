from learnmpm import mesh
from learnmpm import material

def test_mesh_init():
    msh = mesh.Mesh1D(10,1)
    assert len(msh.nodes) == 2
    
    msh = mesh.Mesh1D(10,2)
    assert len(msh.nodes) == 3
    
def test_mesh_particles():
    msh = mesh.Mesh1D(10,1)
    assert len(msh.nodes) == 2
    assert len(msh.elements) == 1
    le = material.LinearElastic(1e5, 1800)

    assert len(msh.particles) == 0
    msh.generate_particles_mesh(2, le)
    assert len(msh.particles) == 2


test_mesh_init()
test_mesh_particles()