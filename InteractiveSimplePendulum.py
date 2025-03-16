"""
File: DumpedPendulum.py
Author: Raul G. Quartieri
Date: 15/03/2025
Description: This script creates a simple animation of the motion of the Simple Pendulum.
             The equation that governs the motion of this type of pendulum is given by:
             \frac{d^2\theta}{dt^2} + \frac{b}{m l^2} \frac{d\theta}{dt} + \frac{g}{l} \sin(\theta) = 0
"""

import pygame
import numpy as np
from scipy.integrate import solve_ivp


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Double Pendulum")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)


g = 9.81  # gravity (m/s^2)
# Initial parameters
m = 1.0  # Mass of the pendulum (kg)
l = 1.0  # Length of the pendulum (m)
b = 0.0  # Damping coefficient for the pendulum (kg m^2/s)

def SimplePemdulum(t, y):
    theta, z = y
    dtheta_dt = z
    dz_dt =  -(b/(m * np.power(l, 2)))*z - (g/l)*np.sin(theta)
    return [dtheta_dt, dz_dt]

# Solving The ODE
y0 = [np.pi/2, 0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 500)

sol = solve_ivp(SimplePemdulum, t_span, y0, t_eval=t_eval)
theta = sol.y[0]

# Transformation to cartesian coordinates
x1 = l*np.sin(theta)
y1 = l*np.cos(theta)

# Slider 
slider_width = 300
slider_height = 20
slider_x = 50   
slider_y_start = 650
slider_spacing = 50

slider_m = pygame.Rect(slider_x, slider_y_start, slider_width, slider_height)
slider_l = pygame.Rect(slider_x, slider_y_start + slider_spacing, slider_width, slider_height)
slider_b = pygame.Rect(slider_x, slider_y_start + 2 * slider_spacing, slider_width, slider_height)

dragging = None

clock = pygame.time.Clock()
running = True
frame = 0

def draw_slider(slider, value, min_val, max_val, label):
    pygame.draw.rect(screen, GRAY, slider)
    handle_x = slider.x + int((value - min_val) / (max_val - min_val) * slider.width)
    pygame.draw.rect(screen, GREEN, (handle_x - 5, slider.y, 10, slider.height))
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"{label}: {value:.2f}", True, BLACK)
    screen.blit(text, (slider.x, slider.y - 20))

def update_simulation():
    global sol, theta1, theta2, x1, y1, x2, y2, frame
    sol = solve_ivp(SimplePemdulum, t_span, y0, t_eval=t_eval)
    theta = sol.y[0]
    x1 = l * np.sin(theta)
    y1 = l * np.cos(theta)
    frame = 0

while running:
    time_delta = clock.tick(30)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider_m.collidepoint(event.pos):
                dragging = "m"
            elif slider_l.collidepoint(event.pos):
                dragging = "l"
            elif slider_b.collidepoint(event.pos):
                dragging = "b"
        
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None
            update_simulation()

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, _ = event.pos
            if dragging == "m":
                m = np.clip((mouse_x - slider_m.x) / slider_m.width * 10.0, 0.01, 10.0) 
            elif dragging == "l":
                l = np.clip((mouse_x - slider_l.x) / slider_l.width * 10.0, 0.01, 10.0)
            elif dragging == "b":
                c = np.clip((mouse_x - slider_b.x) / slider_b.width * 1.0, 0.0, 1.0)

    screen.fill(WHITE)

    if frame < len(t_eval):
        pygame.draw.line(screen, BLACK, (WIDTH // 2, HEIGHT // 2),
                         (WIDTH // 2 + int(100 * x1[frame]), HEIGHT // 2 + int(100 * y1[frame])), 2)
        pygame.draw.circle(screen, BLUE, (WIDTH // 2 + int(100 * x1[frame]), HEIGHT // 2 + int(100 * y1[frame])), 10)
        frame += 1
    
    draw_slider(slider_m, m, 0.01, 10.0, "Mass (m)")
    draw_slider(slider_l, l, 0.01, 10.0, "Length (l)")
    draw_slider(slider_b, b, 0.0, 1.0, "Damping (b)")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()