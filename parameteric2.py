import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize parameters
A = 1  # Amplitude for x
B = 1  # Amplitude for y
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.grid(False)
ax.axis('off')

# Initialize the line and point with alpha for trail effect
line, = ax.plot([], [], lw=1.5, color='lime', alpha=0.8)
point, = ax.plot([], [], 'o', color='yellow', markersize=4, alpha=0.9)

# Set limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Persistent state variables


class PatternState:
    def __init__(self):
        self.time_accumulator = 0.0
        self.freq1_base = 3.0
        self.freq2_base = 2.0
        self.phase_accumulator = 0.0
        self.speed_factor = 1.0
        self.trail_x = []
        self.trail_y = []
        self.max_trail_length = 800

        # Random variation parameters
        self.freq1_variation = 0.0
        self.freq2_variation = 0.0
        self.amplitude_variation = 0.0
        self.speed_variation_timer = 0.0


state = PatternState()


def generate_random_variations():
    """Generate smooth random variations for parameters"""
    # Use Perlin-noise-like smooth variations
    global_time = state.time_accumulator * 0.02

    # Frequency variations that change slowly
    state.freq1_variation = 0.5 * \
        np.sin(global_time * 0.3) + 0.3 * np.sin(global_time * 0.7)
    state.freq2_variation = 0.4 * \
        np.cos(global_time * 0.4) + 0.2 * np.cos(global_time * 0.9)

    # Amplitude breathing effect
    state.amplitude_variation = 0.2 * \
        np.sin(global_time * 0.2) + 0.1 * np.cos(global_time * 0.6)

    # Speed variations - sometimes fast, sometimes slow
    speed_wave1 = np.sin(global_time * 0.15)
    speed_wave2 = np.cos(global_time * 0.23)
    state.speed_factor = 0.5 + 0.7 * (speed_wave1 * speed_wave2) + 0.3


def complex_pattern(t, freq1, freq2, phase_shift, amp_factor):
    """Generate Lissajous curve points"""
    x = (A + state.amplitude_variation) * \
        amp_factor * np.sin(freq1 * t + phase_shift)
    y = (B + state.amplitude_variation) * amp_factor * \
        np.sin(freq2 * t + phase_shift * 0.7)
    return x, y


def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point


def animate(frame):
    # Generate smooth random variations
    generate_random_variations()

    # Update time with variable speed
    dt = 0.03 * state.speed_factor
    state.time_accumulator += dt

    # Calculate frequencies with smooth variations
    freq1 = state.freq1_base + state.freq1_variation
    freq2 = state.freq2_base + state.freq2_variation

    # Update phase continuously for smooth motion
    state.phase_accumulator += dt * 2

    # Create amplitude breathing effect
    amp_factor = 0.8 + 0.3 * np.sin(state.time_accumulator * 0.1)

    # Generate current pattern segment
    t_segment = np.linspace(0, 2 * np.pi, 300)
    x_new, y_new = complex_pattern(
        t_segment, freq1, freq2, state.phase_accumulator, amp_factor)

    # Add new points to trail
    state.trail_x.extend(x_new[::10])  # Subsample to control trail density
    state.trail_y.extend(y_new[::10])

    # Maintain trail length for persistence
    if len(state.trail_x) > state.max_trail_length:
        excess = len(state.trail_x) - state.max_trail_length
        state.trail_x = state.trail_x[excess:]
        state.trail_y = state.trail_y[excess:]

    # Set the line data to show the persistent trail
    line.set_data(state.trail_x, state.trail_y)

    # Current point position
    current_t = state.time_accumulator
    x_current, y_current = complex_pattern(
        np.array([current_t]), freq1, freq2, state.phase_accumulator, amp_factor)
    point.set_data([x_current[0]], [y_current[0]])

    # Occasionally change base frequencies for variety
    if frame % 500 == 0:
        state.freq1_base += np.random.uniform(-0.2, 0.2)
        state.freq2_base += np.random.uniform(-0.2, 0.2)
        # Keep frequencies in reasonable range
        state.freq1_base = np.clip(state.freq1_base, 1, 6)
        state.freq2_base = np.clip(state.freq2_base, 1, 6)

    # Occasionally clear trail for dramatic effect
    if frame % 800 == 799:
        state.trail_x = []
        state.trail_y = []

    return line, point


# Create animation that runs infinitely without restarting
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=None,
                              interval=25, blit=True, repeat=True, cache_frame_data=False)

plt.tight_layout()
plt.show()
