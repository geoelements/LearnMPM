# MPM stress update schemes

![Stress update algorithms](img/stress-update-algorithms.png)

> Comparison of USF, USL, MUSL and USAVG. $x$ is the position vector, $v$ is the velocity,
$a$ is the acceleration, $\varepsilon$ is the strain tensor and $\sigma$ is the stress
tensor. Subscripts, $p$ and $I$ represents values at material points and background nodes.
$\Delta t^* = \Delta t$ is the time step size for USF, USL and MUSL. For USAVG,
$\Delta t^* = \frac{1}{2} \Delta t$. (reproduced after Kularathna., 2018).


[1] Nairn, J. A. (2003). Material point method calculations with explicit cracks. Computer Modeling in Engineering and Sciences, 4(6), 649-664.

[2] Kularathna, S. (2018). Splitting solution scheme for material point method (Doctoral dissertation, University of Cambridge).