import time
import json
import numpy as np
import smbus2

# IMU SETUP
bus = smbus2.SMBus(1)
IMU_ADDR = 0x6A
CTRL1_XL = 0x10
CTRL2_G  = 0x11
OUTX_L_G = 0x22
OUTX_L_A = 0x28

def init_imu():
    bus.write_byte_data(IMU_ADDR, CTRL1_XL, 0x40)  # Accel 104 Hz
    bus.write_byte_data(IMU_ADDR, CTRL2_G, 0x4C)   # Gyro 104 Hz, 2000 dps

def read_regs(start, length):
    return bus.read_i2c_block_data(IMU_ADDR, start, length)

def read_imu():
    # Gyro raw
    g = read_regs(OUTX_L_G, 6)
    gx_raw = int.from_bytes(g[0:2], "little", signed=True)
    gy_raw = int.from_bytes(g[2:4], "little", signed=True)
    gz_raw = int.from_bytes(g[4:6], "little", signed=True)

    # Accel raw
    a = read_regs(OUTX_L_A, 6)
    ax_raw = int.from_bytes(a[0:2], "little", signed=True)
    ay_raw = int.from_bytes(a[2:4], "little", signed=True)
    az_raw = int.from_bytes(a[4:6], "little", signed=True)

    # Convert accel (0.061 mg/LSB)
    accel_g_to_mps2 = 9.80665
    ax = ax_raw * 0.000061 * accel_g_to_mps2
    ay = ay_raw * 0.000061 * accel_g_to_mps2
    az = az_raw * 0.000061 * accel_g_to_mps2

    # Convert gyro (0.07 dps/LSB)
    gx = gx_raw * 0.07
    gy = gy_raw * 0.07
    gz = gz_raw * 0.07

    return ax, ay, az, gx, gy, gz


# CALIBRATION
def calibrate(samples=500, delay=0.002):
    print("Initializing IMU...")
    init_imu()
    time.sleep(0.5)

    print("\nHold IMU completely still for 2 seconds...")
    time.sleep(2)

    accel_data = []
    gyro_data = []

    print("Collecting data...")
    for _ in range(samples):
        ax, ay, az, gx, gy, gz = read_imu()
        accel_data.append([ax, ay, az])
        gyro_data.append([gx, gy, gz])
        time.sleep(delay)

    accel_data = np.array(accel_data)
    gyro_data  = np.array(gyro_data)

    accel_offset = accel_data.mean(axis=0)
    gyro_offset  = gyro_data.mean(axis=0)

    # Save to JSON
    calibration = {
        "accel_offset": accel_offset.tolist(),
        "gyro_offset": gyro_offset.tolist()
    }

    with open("imu_calibration.json", "w") as f:
        json.dump(calibration, f, indent=4)

    print("\nCalibration complete!")
    print("Saved to imu_calibration.json\n")

    print("Accel offset (m/s^2):", accel_offset)
    print("Gyro offset (dps):   ", gyro_offset)


if __name__ == "__main__":
    calibrate()
