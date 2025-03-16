import pygame
import numpy as np
from scipy.integrate import solve_ivp

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Double Pendulum")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Constants
g = 9.81  # gravity (m/s^2)

# Initial parameters
m1 = 1.0  # Mass of the first pendulum (kg)
m2 = 1.0  # Mass of the second pendulum (kg)
l1 = 1.0  # Length of the first pendulum (m)
l2 = 1.0  # Length of the second pendulum (m)
c1 = 0.0  # Damping coefficient for the first pendulum (kg m^2/s)
c2 = 0.0  # Damping coefficient for the second pendulum (kg m^2/s)

# Function to compute the derivatives of the system
def DoubleDampedPendulum(t, y):
    theta1, z1, theta2, z2 = y

    deltatheta = theta1 - theta2
    dtheta1_dt = z1
    dtheta2_dt = z2
    denominator = ((m1 + m2) * np.power(l1, 2) * m2 * np.power(l2, 2)) - np.power(m2 * l1 * l2 * np.cos(deltatheta), 2)

    dz1_dt = (m2 * np.power(l2, 2) * (-m2 * l1 * l2 * np.power(z2, 2) * np.sin(deltatheta) - (m1 + m2) * g * l1 * np.sin(theta1) - c1 * z1) \
              - (m2 * l1 * l2 * np.cos(deltatheta) * (m2 * l1 * l2 * np.power(z1, 2) * np.sin(deltatheta) - m2 * g * l2 * np.sin(theta2) - c2 * z2))) \
              / denominator

    dz2_dt = (-m2 * l1 * l2 * np.cos(deltatheta) * (-m2 * l1 * l2 * np.power(z2, 2) * np.sin(deltatheta) - (m1 + m2) * g * l1 * np.sin(theta1) - c1 * z1) \
              + ((m1 + m2) * np.power(l1, 2)) * (m2 * l1 * l2 * np.power(z1, 2) * np.sin(deltatheta) - m2 * g * l2 * np.sin(theta2) - c2 * z2)) \
              / denominator

    return [dtheta1_dt, dz1_dt, dtheta2_dt, dz2_dt]

# Initial conditions
y0 = [np.pi / 2, 0, np.pi / 2, 0]
t_span = (0, 100)
t_eval = np.linspace(0, 100, 1000)

# Solve the differential equations
sol = solve_ivp(DoubleDampedPendulum, t_span, y0, t_eval=t_eval)
theta1 = sol.y[0]
theta2 = sol.y[2]

# Transformation to cartesian coordinates (In pygame y = -y)
x1 = l1 * np.sin(theta1)
y1 = l1 * np.cos(theta1)  
x2 = x1 + l2 * np.sin(theta2)
y2 = y1 + l2 * np.cos(theta2)  

# Slider properties
slider_width = 300
slider_height = 20
slider_x1 = 50  
slider_x2 = 450  
slider_y_start = 650
slider_spacing = 50

# Slider rectangles
slider_m1 = pygame.Rect(slider_x1, slider_y_start, slider_width, slider_height)
slider_l1 = pygame.Rect(slider_x1, slider_y_start + slider_spacing, slider_width, slider_height)
slider_c1 = pygame.Rect(slider_x1, slider_y_start + 2 * slider_spacing, slider_width, slider_height)

slider_m2 = pygame.Rect(slider_x2, slider_y_start, slider_width, slider_height)
slider_l2 = pygame.Rect(slider_x2, slider_y_start + slider_spacing, slider_width, slider_height)
slider_c2 = pygame.Rect(slider_x2, slider_y_start + 2 * slider_spacing, slider_width, slider_height)

# Slider dragging state
dragging = None

# Main loop
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
    sol = solve_ivp(DoubleDampedPendulum, t_span, y0, t_eval=t_eval)
    theta1 = sol.y[0]
    theta2 = sol.y[2]
    x1 = l1 * np.sin(theta1)
    y1 = l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 + l2 * np.cos(theta2)
    frame = 0

while running:
    time_delta = clock.tick(30) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle slider dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider_m1.collidepoint(event.pos):
                dragging = "m1"
            elif slider_l1.collidepoint(event.pos):
                dragging = "l1"
            elif slider_c1.collidepoint(event.pos):
                dragging = "c1"
            elif slider_m2.collidepoint(event.pos):
                dragging = "m2"
            elif slider_l2.collidepoint(event.pos):
                dragging = "l2"
            elif slider_c2.collidepoint(event.pos):
                dragging = "c2"

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None
            update_simulation()  # Update simulation only when dragging stops

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, _ = event.pos
            if dragging == "m1":
                m1 = np.clip((mouse_x - slider_m1.x) / slider_m1.width * 5.0, 0.01, 10.0)
            elif dragging == "l1":
                l1 = np.clip((mouse_x - slider_l1.x) / slider_l1.width * 5.0, 0.01, 10.0)
            elif dragging == "c1":
                c1 = np.clip((mouse_x - slider_c1.x) / slider_c1.width * 1.0, 0.0, 1.0)
            elif dragging == "m2":
                m2 = np.clip((mouse_x - slider_m2.x) / slider_m2.width * 5.0, 0.01, 10.0)
            elif dragging == "l2":
                l2 = np.clip((mouse_x - slider_l2.x) / slider_l2.width * 5.0, 0.01, 10.0)
            elif dragging == "c2":
                c2 = np.clip((mouse_x - slider_c2.x) / slider_c2.width * 1.0, 0.0, 1.0)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the pendulum
    if frame < len(t_eval):
        pygame.draw.line(screen, BLACK, (WIDTH // 2, HEIGHT // 2),
                         (WIDTH // 2 + int(100 * x1[frame]), HEIGHT // 2 + int(100 * y1[frame])), 2)
        pygame.draw.line(screen, BLACK, (WIDTH // 2 + int(100 * x1[frame]), HEIGHT // 2 + int(100 * y1[frame])),
                         (WIDTH // 2 + int(100 * x2[frame]), HEIGHT // 2 + int(100 * y2[frame])), 2)
        pygame.draw.circle(screen, BLUE, (WIDTH // 2 + int(100 * x1[frame]), HEIGHT // 2 + int(100 * y1[frame])), 10)
        pygame.draw.circle(screen, RED, (WIDTH // 2 + int(100 * x2[frame]), HEIGHT // 2 + int(100 * y2[frame])), 10)
        frame += 1

    # Draw sliders in two columns
    draw_slider(slider_m1, m1, 0.01, 10.0, "Mass 1 (m1)")
    draw_slider(slider_l1, l1, 0.01, 10.0, "Length 1 (l1)")
    draw_slider(slider_c1, c1, 0.0, 1.0, "Damping 1 (c1)")

    draw_slider(slider_m2, m2, 0.01, 10.0, "Mass 2 (m2)")
    draw_slider(slider_l2, l2, 0.01, 10.0, "Length 2 (l2)")
    draw_slider(slider_c2, c2, 0.0, 1.0, "Damping 2 (c2)")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()