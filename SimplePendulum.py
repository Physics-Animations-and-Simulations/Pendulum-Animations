"""
File: SimplePendulum.py
Author: Raul G. Quartieri
Date: 15/03/2025
Description: This script creates a simple simulation of the motion of the Simple Pendulum.
             The equation that governs the motion of this type of pendulum is given by:
             \frac{d^2\theta}{dt^2} + \frac{g}{l} \sin(\theta) = 0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp # numerically integrates a system of ODE given an initial value: dy / dt = f(t, y), y(t0) = y0

g = 9.81 # gravity (m/s^2)
l = 5 # length of rod (m)

def SimplePendulum(t, y):
    theta, z = y
    dtheta_dt = z
    dz_dt = - (g/l) * np.sin(theta)
    return [dtheta_dt, dz_dt]

# Initial conditions:
y0 = [np.pi/2, 0]  #[initial angle and initial velocity]

# Time span for simulation
t_span = (0, 10)
t_eval = np.linspace(0, 10, 500)

# Solve the ODE
sol = solve_ivp(SimplePendulum, t_span, y0, t_eval=t_eval)
theta = sol.y[0]

# Convert to Cartesian coordinates
x1 = l * np.sin(theta)
y1 = -l * np.cos(theta)

# Creating animation
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-l-1, l+1)
ax.set_ylim(-l-1, l+1)
ax.set_aspect("equal")
ax.grid()

line, = ax.plot([], [], "o-", lw=2, color='blue')
trace, = ax.plot([], [], "-", lw=1, color='red')

# Initializing animation
def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(frame):
    line.set_data([0,x1[frame]], [0, y1[frame]])
    trace.set_data(x1[:frame], y1[:frame])
    return line, trace

ani = animation.FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=20)
plt.title("Simple Pendulum Animation")
ani.save("Physics_Simulations/Animations/simple_pendulum.gif", writer="pillow", fps=30)
#plt.show()