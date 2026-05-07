import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
g = 9.81  # Gravity (m/s^2)
e_hard = 1.50 / 4.40  # Rebound coefficient for hard surface
e_soft = 0.80 / 4.40  # Rebound coefficient for soft surface
dt_hard = 0.005  # Collision duration for hard surface (s)
dt_soft = 0.020  # Collision duration for soft surface (s)

# Time array
t_total = 1.5  # Total simulation time (s)
fps = 60
num_frames = int(t_total * fps)
time_array = np.linspace(0, t_total, num_frames)

# Function to calculate position, velocity, and acceleration
def calculate_trajectory(drop_height, e):
    t_fall = np.sqrt(2 * drop_height / g)
    v1 = -np.sqrt(2 * g * drop_height)
    v2 = abs(v1) * e

    position = []
    velocity = []
    acceleration = []

    for t in time_array:
        if t < t_fall:
            pos = drop_height - 0.5 * g * t**2
            vel = -g * t
            acc = -g
        else:
            t_bounce = t - t_fall
            pos = v2 * t_bounce - 0.5 * g * t_bounce**2
            vel = v2 - g * t_bounce
            acc = -g
            if pos < 0:
                pos = 0
                vel = 0
                acc = 0
        position.append(pos)
        velocity.append(vel)
        acceleration.append(acc)

    return np.array(position), np.array(velocity), np.array(acceleration)

# Calculate trajectories for hard and soft surfaces
drop_height = 1.0  # Initial drop height (m)
position_hard, velocity_hard, acceleration_hard = calculate_trajectory(drop_height, e_hard)
position_soft, velocity_soft, acceleration_soft = calculate_trajectory(drop_height, e_soft)

# Plot position-time and acceleration-time graphs
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Position-Time Graph
ax1.plot(time_array, position_hard, label='Hard Surface', color='red')
ax1.plot(time_array, position_soft, label='Soft Surface', color='green')
ax1.set_title('Position-Time Graph')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (m)')
ax1.legend()
ax1.grid(True)

# Acceleration-Time Graph
ax2.plot(time_array, acceleration_hard, label='Hard Surface', color='red')
ax2.plot(time_array, acceleration_soft, label='Soft Surface', color='green')
ax2.set_title('Acceleration-Time Graph')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Acceleration (m/s^2)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# Calculate rebound coefficients and create a table
v1 = -np.sqrt(2 * g * drop_height)
v2_hard = abs(v1) * e_hard
v2_soft = abs(v1) * e_soft

rebound_data = {
    'Surface': ['Hard', 'Soft'],
    'Initial Velocity (m/s)': [v1, v1],
    'Rebound Velocity (m/s)': [v2_hard, v2_soft],
    'Rebound Coefficient (e)': [e_hard, e_soft]
}

rebound_table = pd.DataFrame(rebound_data)
print(rebound_table)