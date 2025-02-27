import serial
import time
import matplotlib.pyplot as plt

# -----------------------------
# 1) Configure your serial port
# -----------------------------
PORT_NAME = 'COM11'
BAUD_RATE = 115200

# Open serial port
ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1)
time.sleep(2)  # Give the connection a second to settle

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
plt.ion()  # Interactive mode ON
fig, ax = plt.subplots()

# We'll create 3 lines for X, Y, Z
line_x, = ax.plot([], [], label='Acc X')
line_y, = ax.plot([], [], label='Acc Y')
line_z, = ax.plot([], [], label='Acc Z')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration (m/s^2)')
ax.set_title('Real-Time Acceleration from MPU6050')
ax.legend()
plt.show()

# -----------------------------
# 4) Main Loop for Reading & Plotting
# -----------------------------
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("X:"):
            # Expected format: X:0.08 Y:-0.56 Z:8.38
            # Remove labels: "X:", "Y:", "Z:"
            clean_line = line.replace("X:", "").replace("Y:", "").replace("Z:", "")
            # Now we should have something like: "0.08 -0.56 8.38"
            parts = clean_line.split()
            
            if len(parts) == 3:
                try:
                    ax_val = float(parts[0])
                    ay_val = float(parts[1])
                    az_val = float(parts[2])
                    
                    # Time since start of script
                    current_time = time.time() - start_time
                    
                    # Append to lists
                    times.append(current_time)
                    accX_list.append(ax_val)
                    accY_list.append(ay_val)
                    accZ_list.append(az_val)
                    
                    # Update plot data
                    line_x.set_xdata(times)
                    line_x.set_ydata(accX_list)
                    line_y.set_xdata(times)
                    line_y.set_ydata(accY_list)
                    line_z.set_xdata(times)
                    line_z.set_ydata(accZ_list)
                    
                    # Rescale axes
                    ax.relim()
                    ax.autoscale_view()
                    
                    # Redraw the figure
                    plt.draw()
                    plt.pause(0.01)
                
                except ValueError:
                    pass  # Ignore lines that don't parse properly

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
    plt.close()
