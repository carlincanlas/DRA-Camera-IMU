import time
import csv
import smbus2
from picamera2 import Picamera2
"""
Log IMU data and IMU-camerea timestamps
"""

# IMU SETUP
bus = smbus2.SMBus(1)

IMU_ADDR = 0x6A     
CTRL1_XL = 0x10
CTRL2_G  = 0x11
OUTX_L_G = 0x22
OUTX_L_A = 0x28

def init_imu():
    # Accel 
    bus.write_byte_data(IMU_ADDR, CTRL1_XL, 0x40)

    # Gyro
    bus.write_byte_data(IMU_ADDR, CTRL2_G, 0x4C)

def read_regs(start, length):
    return bus.read_i2c_block_data(IMU_ADDR, start, length)

def read_imu():
    # Gyroscope raw 
    g = read_regs(OUTX_L_G, 6)
    gx_raw = int.from_bytes(g[0:2], "little", signed=True)
    gy_raw = int.from_bytes(g[2:4], "little", signed=True)
    gz_raw = int.from_bytes(g[4:6], "little", signed=True)

    # Accelerometer raw 
    a = read_regs(OUTX_L_A, 6)
    ax_raw = int.from_bytes(a[0:2], "little", signed=True)
    ay_raw = int.from_bytes(a[2:4], "little", signed=True)
    az_raw = int.from_bytes(a[4:6], "little", signed=True)

    # Convert raw real units

    # Accel conversion
    # 1 raw = 0.061 mg = 0.000061 g
    accel_g_to_mps2 = 9.80665
    ax = ax_raw * 0.000061 * accel_g_to_mps2
    ay = ay_raw * 0.000061 * accel_g_to_mps2
    az = az_raw * 0.000061 * accel_g_to_mps2 - 0.55247724105

    # Gyro conversion
    # 1 raw = 70 mdps = 0.07 dps
    gx = gx_raw * 0.07
    gy = gy_raw * 0.07
    gz = gz_raw * 0.07

    return ax, ay, az, gx, gy, gz


# CAMERA SETUP
picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (640, 480)})
picam.configure(config)
picam.start()

# TIMESTAMP SYSTEM
t0 = time.time()   # shared reference time

imu_csv = open("imu_log.csv", "w", newline="")
cam_csv = open("cam_log.csv", "w", newline="")

imu_writer = csv.writer(imu_csv)
cam_writer = csv.writer(cam_csv)

imu_writer.writerow(["t", "ax_mps2", "ay_mps2", "az_mps2", "gx_dps", "gy_dps", "gz_dps"])
cam_writer.writerow(["t"])

# MAIN LOOP (10 seconds)
print("Logging IMU + Camera timestamps for 10 seconds...")
init_imu()

end_time = time.time() + 10.0
next_cam = 0

while time.time() < end_time:

    # IMU read 
    t = time.time() - t0
    try:
        ax, ay, az, gx, gy, gz = read_imu()
        imu_writer.writerow([t, ax, ay, az, gx, gy, gz])
    except:
        print("IMU error")
        continue

    # Camera timestamp (30 FPS )
    if t > next_cam:
        picam.capture_array()   # call capture_array() but frame is not saved
        cam_writer.writerow([time.time() - t0])
        next_cam += 1/30

imu_csv.close()
cam_csv.close()

print("Done! imu_log.csv and cam_log.csv created.")
