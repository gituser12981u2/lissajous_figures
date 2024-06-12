import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize parameters
A = 1  # Amplitude for x
B = 1  # Amplitude for y
delta = np.pi / 2  # Phase difference
t = np.linspace(0, 2 * np.pi, 1000)

# Create figure and axis
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')  # Set the figure background color to black
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.grid(False)
ax.axis('off')  # Turn off the axis

# Initialize the line and point
line, = ax.plot([], [], lw=1, color='green')
point, = ax.plot([], [], 'go', markersize=5)

# Set limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)


# Function to generate the Lissajous points
def complex_pattern(t, A, B, freq1, freq2, phase_shift):
    x = A * np.sin(freq1 * t + phase_shift)
    y = B * np.sin(freq2 * t)
    return x, y


# Initialize the animation
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point


# Animation function
def animate(i):
    freq1 = 5 + 0.1 * i  # Slowly increase frequency for x
    freq2 = 2 + 0.1 * i  # Slowly increase frequency for y
    phase_shift = 0.1 * i
    t = np.linspace(0, 2 * np.pi, 1000)
    x, y = complex_pattern(t, A, B, freq1, freq2, phase_shift)
    line.set_data(x, y)
    point.set_data([x[-1]], [y[-1]])  # Point at the end of the line
    return line, point


# Create animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=400,
                              interval=30, blit=True)

plt.show()
