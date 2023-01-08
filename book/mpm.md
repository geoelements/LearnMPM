# An introduction to the Material Point Method
The Material Point Method (MPM) is a particle based method that represents the material as a collection of material points, and their deformations are determined by Newton’s laws of motion. 
The MPM is a hybrid Eulerian-Lagrangian approach, which uses moving material points and computational nodes on a background mesh.
This approach is very effective particularly in the context of large deformations.

![algorithm](img/mpm-algorithm.png)
> Illustration of the MPM algorithm: (1) A representation of material points overlaid on a computational grid. 
Arrows represent material point state vectors (mass, volume, velocity, etc.) being projected to the nodes of the computational grid. 
(2) The equations of motion are solved onto the nodes, resulting in updated nodal velocities and positions. 
(3) The updated nodal kinematics are interpolated back to the material points. 
(4) The state of the material points is updated, and the
computational grid is reset


## MPM discretization

A typical 2D discretisation of a solid body is shown below. 
The grey circles are the material points $x_{p}$, where _p_ represents a material point, and the computational nodes are the points of intersection of the grid (denoted as $X_{i}$, where _i_ represents a computational node). 
The MPM involves discretising the domain, $\Omega$, with a set of material points. 
The material points are assigned an initial value of position, velocity, mass, volume, and stress, denoted as 
$\mathbf{x}_{p}$, $\mathbf{\mathit{v}}_{p}$, $\mathit{m}_{p}$, $\mathbf{V}_{p}$, and $\sigma_{p}$. 
Depending on the material being simulated, additional parameters, like pressure, temperature, pore-water pressure, etc., are specified at the material points. 
The material points are assumed to be within the computational grid which for ease of computation, is assumed to be a Cartesian lattice. 
At every time step $\mathit{t}_{k}$, the MPM computation cycle involves projecting the data, such as position, mass, and velocity, from the material points to the computational grid using the standard nodal basis functions, called the _shape functions_, derived from the position of the particle with respect to the grid. 
Gradient terms are calculated on the computational grid, and the governing equation, i.e. the equation of motion, is solved with the updated position and velocity values mapping back to the material points. 
The mesh is reinitialised to its original state and the computational cycle is repeated. 

![MPM discretization](img/mpm-discretization.png)

## Conservation properties
MPM automatically satisfies the mass conservation by assigning a constant mass to each material point. 
The momentum balance is enforced in governing equations. 
However, Bardenhagen (2002) showed that the original MPM formulation does not satisfy the energy conservation explicitly. 
It was found that the energy conservation in MPM is strongly
dependent on the two algorithms which are used to update the stress at material points.
