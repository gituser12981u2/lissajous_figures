import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Define the Lissajous function
def lissajous(t, A, B, a, b, delta):
    x = A * np.sin(a * t + delta)
    y = B * np.sin(b * t)
    return x, y


# Initialize parameters
A = 1  # Amplitude for x
B = 1  # Amplitude for y
a = 3  # Frequency for x
b = 2  # Frequency for y
delta = np.pi / 2  # Phase difference
t = np.linspace(0, 2 * np.pi, 1000)

# Create figure and axis
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_aspect('equal')
line, = ax.plot([], [], lw=2, color='green')

# Set limits and labels
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_facecolor('black')
ax.grid(False)
ax.axis('off')


# Initialize the animation
def init():
    line.set_data([], [])
    return line,


# Animation function
def animate(i):
    t = np.linspace(0, 2 * np.pi, 1000)
    a = 3 + 0.05 * i
    b = 2 + 0.05 * i
    x, y = lissajous(t, A, B, a, b, delta)
    line.set_data(x, y)
    return line,


# Create animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=400,
                              interval=30, blit=True)

plt.show()
