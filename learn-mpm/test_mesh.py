from learn-mpm import mesh

def test_mesh_init():
    msh = mesh.Mesh1D(10,1)
    assert len(msh.nodes) == 2
    
    msh = mesh.Mesh1D(10,2)
    assert len(msh.nodes) == 3

test_mesh_init()