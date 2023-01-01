import numpy as np

def axial_vibration_bar1d(L, E, rho, duration, dt, v0, x):

    # Frequency of system mode 1
    w1 = np.pi / (2 * L) * np.sqrt(E/rho)
    b1 = np.pi / (2 * L)

    # position and velocity in time
    tt, vt, xt = [], [], []

    nsteps = int(duration/dt)
    t = 0
    for _ in range(nsteps):
        vt.append(v0 * np.cos(w1 * t) * np.sin(b1 * x))
        xt.append(v0 / w1 * np.sin(w1 * t) * np.sin(b1 * x))
        tt.append(t)

        t += dt
    
    return [xt, vt, tt]