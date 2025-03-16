"""
File: DumpedPendulum.py
Author: Raul G. Quartieri
Date: 15/03/2025
Description: This script creates a simple animation of the motion of the Damped Pendulum.
             The equation that governs the motion of this type of pendulum is given by:
             \frac{d^2\theta}{dt^2} + \frac{b}{m l^2} \frac{d\theta}{dt} + \frac{g}{l} \sin(\theta) = 0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

g = 9.81    # gravity (m/s^2)
l = 5       # length of rod (m)
m = 5       # mass (kg)
b = 0.8     # dumping coefficient (kg/s)

def DampedPemdulum(t, y):
    theta, z = y
    dtheta_dt = z
    dz_dt =  -(b/(m * np.power(l, 2)))*z - (g/l)*np.sin(theta)
    return [dtheta_dt, dz_dt]

# Solving The ODE
y0 = [np.pi/2, 0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 500)

sol = solve_ivp(DampedPemdulum, t_span, y0, t_eval=t_eval)
theta = sol.y[0]
time = sol.t

# Simulation
x1 = l * np.sin(theta)
y1 = -l * np.cos(theta)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-l - 1, l + 1)
ax.set_ylim(-l - 1, l + 1)
ax.set_aspect("equal")
ax.grid()

line, = ax.plot([], [], "o-", lw=2, color="blue")
trace, = ax.plot([], [], "-", lw=1, color="red")

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(frame):
    line.set_data([0, x1[frame]], [0, y1[frame]])
    trace.set_data(x1[:frame], y1[:frame])
    return line, trace

ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=50)
plt.title("Damped Pendulum Animation")
ani.save("DampedPendulum/damped_pendulum.gif", writer="pillow", fps=30)
#plt.show()