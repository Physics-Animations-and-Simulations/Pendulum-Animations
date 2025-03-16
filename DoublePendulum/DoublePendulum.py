"""
File: DoublePendulum.py
Author: Raul G. Quartieri
Date: /03/2025
Description: This script creates a simple animation of the motion of the Damped Double Pendulum.
             The equations that governs the motion of this type of pendulum is given by:
             \ddot{\theta}_1 = \frac{1}{\det(\mathbf{M})} \left[ m_2 l_2^2 \left( -m_2 l_1 l_2 \dot{\theta}_2^2 \sin(\theta_1 - \theta_2) - (m_1 + m_2) g l_1 \sin \theta_1 - c_1 \dot{\theta}_1 \right) - m_2 l_1 l_2 \cos(\theta_1 - \theta_2) \left( m_2 l_1 l_2 \dot{\theta}_1^2 \sin(\theta_1 - \theta_2) - m_2 g l_2 \sin \theta_2 - c_2 \dot{\theta}_2 \right) \right]
             \ddot{\theta}_2 = \frac{1}{\det(\mathbf{M})} \left[ -m_2 l_1 l_2 \cos(\theta_1 - \theta_2) \left( -m_2 l_1 l_2 \dot{\theta}_2^2 \sin(\theta_1 - \theta_2) - (m_1 + m_2) g l_1 \sin \theta_1 - c_1 \dot{\theta}_1 \right) + (m_1 + m_2) l_1^2 \left( m_2 l_1 l_2 \dot{\theta}_1^2 \sin(\theta_1 - \theta_2) - m_2 g l_2 \sin \theta_2 - c_2 \dot{\theta}_2 \right) \right]
             \det(\mathbf{M}) = (m_1 + m_2) l_1^2 \cdot m_2 l_2^2 - (m_2 l_1 l_2 \cos(\theta_1 - \theta_2))^2.
             
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

# Constants
g = 9.81    # gravity (m/s^2)

m1 = 1      # Mass of the first pendulum (kg)
l1 = 1      # Length of the first pendulum (m)
c1 = 0      # without Damping coefficient for the first pendulum (kg m^2/s)
#c1 = 0.1    # Damping coefficient for the first pendulum (kg m^2/s)

m2 = 1      # Mass of the second pendulum (kg)
l2 = 1      # Length of the second pendulum (m)
c2 = 0      # without Damping coefficient for the second pendulum (kg m^2/s)
#c2 = 0.1    # Damping coefficient for the first pendulum (kg m^2/s)

def DoubleDampedPendulum(t, y):
    theta1, z1, theta2, z2 = y

    deltatheta = theta1 - theta2
    dtheta1_dt = z1
    dtheta2_dt = z2
    denominator = ((m1 + m2) * np.power(l1, 2) * m2 * np.sqrt(l2)) - np.power(m2*l1*l2*np.cos(deltatheta) , 2)

    dz1_dt = (m2 * np.power(l2, 2) * (-m2 * l1 * l2 * np.power(z2, 2) * np.sin(deltatheta) - (m1 + m2) * g * l1 * np.sin(theta1) - c1 * z1) \
              - (m2 * l1 * l2 * np.cos(deltatheta) * (m2 * l1 * l2 * np.power(z1, 2) * np.sin(deltatheta) - m2 * g * l2 * np.sin(theta2) - c2 * z2))) \
              / denominator

    dz2_dt = (-m2 * l1 * l2 * np.cos(deltatheta) * (-m2 * l1 * l2 * np.power(z2, 2) * np.sin(deltatheta) - (m1 + m2) * g * l1 * np.sin(theta1) - c1 * z1) \
              + ((m1 + m2) * np.power(l1, 2)) * (m2 * l1 * l2 * np.power(z1, 2) * np.sin(deltatheta) - m2 * g * l2 * np.sin(theta2) - c2 * z2)) \
              / denominator
    
    return [dtheta1_dt, dz1_dt, dtheta2_dt, dz2_dt]

y0 = [np.pi/2, 0, np.pi/2, 0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 500)

sol = solve_ivp(DoubleDampedPendulum, t_span, y0, t_eval=t_eval)
theta1 = sol.y[0]
theta2 = sol.y[2]
time = sol.t

# Simulation
x1 = l1 * np.sin(theta1)
y1 = -l1 * np.cos(theta1)
x2 = x1 + l2 * np.sin(theta2)
y2 = y1 - l2 * np.cos(theta2) 

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-(l1+l2) - 1, (l1+l2) + 1)
ax.set_ylim(-(l1+l2) - 1, (l1+l2) + 1)
ax.set_aspect("equal")
ax.grid()

line, = ax.plot([], [], "o-", lw=2, color="blue")
trace, = ax.plot([], [], "-", lw=1, color="red")

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(frame):
    line.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
    trace.set_data(x2[:frame], y2[:frame])
    return line, trace

ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=50)
plt.title("Double Pendulum Animation")
ani.save("DoublePendulum/double_pendulum.gif", writer="pillow", fps=30)
# If use the damped version
#plt.title("Damped Double Pendulum Animation")
#ani.save("DoublePendulum/damped_double_pendulum.gif", writer="pillow", fps=30)


