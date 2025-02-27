import serial
import time
import matplotlib.pyplot as plt

# -----------------------------
# 1) Configure your serial port
# -----------------------------
PORT_NAME = 'COM11'  # Update as needed (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200

ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for the connection to settle

# -----------------------------
# 2) Prepare lists for the data
# -----------------------------
times = []
accX_list = []
accY_list = []
accZ_list = []

start_time = time.time()

# -----------------------------
# 3) Setup live plotting
# -----------------------------
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()

# Create 3 lines for X, Y, Z data
line_x, = ax.plot([], [], label='Acc X')
line_y, = ax.plot([], [], label='Acc Y')
line_z, = ax.plot([], [], label='Acc Z')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration (m/s^2)')
ax.set_title('Real-Time Accelerationy')
ax.legend()
plt.show()

# -----------------------------
# 4) Main Loop for Reading & Plotting
# -----------------------------
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("X:"):
            # Expected format: "X:0.08 Y:-0.56 Z:8.38"
            clean_line = line.replace("X:", "").replace("Y:", "").replace("Z:", "")
            parts = clean_line.split()
            
            if len(parts) == 3:
                try:
                    ax_val = float(parts[0])
                    ay_val = float(parts[1])
                    az_val = float(parts[2])
                    
                    current_time = time.time() - start_time
                    times.append(current_time)
                    accX_list.append(ax_val)
                    accY_list.append(ay_val)
                    accZ_list.append(az_val)
                    
                    # Remove data older than 6 seconds
                    while times and times[0] < current_time - 6:
                        times.pop(0)
                        accX_list.pop(0)
                        accY_list.pop(0)
                        accZ_list.pop(0)
                    
                    # Update the plot data
                    line_x.set_data(times, accX_list)
                    line_y.set_data(times, accY_list)
                    line_z.set_data(times, accZ_list)
                    
                    # Set x-axis to show only last 6 seconds
                    ax.set_xlim(max(0, current_time - 6), current_time)
                    
                    # Optionally adjust y-axis if needed
                    ax.relim()
                    ax.autoscale_view(True, True, True)
                    
                    plt.draw()
                    plt.pause(0.01)
                
                except ValueError:
                    pass  # Skip this line if there's a parsing error

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
    plt.close()
