import pandas as pd
import matplotlib.pyplot as plt

# Load data
imu = pd.read_csv("imu_log.csv")
cam = pd.read_csv("cam_log.csv")

# -----------------------------
# PLOT ACCELEROMETER (m/s2)
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(imu["t"], imu["ax_mps2"], label="ax (m/s^2)")
plt.plot(imu["t"], imu["ay_mps2"], label="ay (m/s^2)")
plt.plot(imu["t"], imu["az_mps2"], label="az (m/s^2)")
plt.scatter(cam["t"], [0]*len(cam), label="Camera timestamps", marker="|", s=200)  
plt.legend()
plt.title("Accelerometer vs Camera Sync")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s2)")
plt.grid(True)

# -----------------------------
# PLOT GYROSCOPE (deg/s)
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(imu["t"], imu["gx_dps"], label="gx (deg/s)")
plt.plot(imu["t"], imu["gy_dps"], label="gy (deg/s)")
plt.plot(imu["t"], imu["gz_dps"], label="gz (deg/s)")
plt.scatter(cam["t"], [0]*len(cam), label="Camera timestamps", marker="|", s=200)
plt.legend()
plt.title("Gyroscope vs Camera Sync")
plt.xlabel("Time (s)")
plt.ylabel("Angular Rate (deg/s)")
plt.grid(True)

plt.show()
