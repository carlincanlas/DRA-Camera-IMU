import pandas as pd
import matplotlib.pyplot as plt

# Load data
imu = pd.read_csv("imu_log.csv")
cam = pd.read_csv("cam_log.csv")

g = 9.81

imu["ax_g"] = imu["ax_mps2"] / g
imu["ay_g"] = imu["ay_mps2"] / g
imu["az_g"] = imu["az_mps2"] / g

# Moving Average
window = 10

# Accelerometer smoothing
imu["ax_smooth"] = imu["ax_g"].rolling(window, center=True).mean()
imu["ay_smooth"] = imu["ay_g"].rolling(window, center=True).mean()
imu["az_smooth"] = imu["az_g"].rolling(window, center=True).mean()

# Gyroscope smoothing
imu["gx_smooth"] = imu["gx_dps"].rolling(window, center=True).mean()
imu["gy_smooth"] = imu["gy_dps"].rolling(window, center=True).mean()
imu["gz_smooth"] = imu["gz_dps"].rolling(window, center=True).mean()


# PLOT ACCELEROMETER
plt.figure(figsize=(10,5))
# Non-smoothed data
#plt.plot(imu["t"], imu["ax_mps2"], label="ax raw", alpha=0.4)
#plt.plot(imu["t"], imu["ay_mps2"], label="ay raw", alpha=0.4)
#plt.plot(imu["t"], imu["az_mps2"], label="az raw", alpha=0.4)

plt.plot(imu["t"], imu["ax_smooth"], label="ax", linewidth=2)
plt.plot(imu["t"], imu["ay_smooth"], label="ay", linewidth=2)
plt.plot(imu["t"], imu["az_smooth"], label="az", linewidth=2)

plt.legend()
plt.title("Accelerometer 180deg y axis rotation")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.grid(True)


# PLOT GYROSCOPE 
plt.figure(figsize=(10,5))
#plt.plot(imu["t"], imu["gx_dps"], label="gx raw", alpha=0.4)
#plt.plot(imu["t"], imu["gy_dps"], label="gy raw", alpha=0.4)
#plt.plot(imu["t"], imu["gz_dps"], label="gz raw", alpha=0.4)

plt.plot(imu["t"], imu["gx_smooth"], label="gx", linewidth=2)
plt.plot(imu["t"], imu["gy_smooth"], label="gy", linewidth=2)
plt.plot(imu["t"], imu["gz_smooth"], label="gz", linewidth=2)

plt.legend()
plt.title("Gyroscope 180deg y axis rotation")
plt.xlabel("Time (s)")
plt.ylabel("Angular Rate (deg/s)")
plt.grid(True)

plt.show()
