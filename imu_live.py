import smbus
import time

bus = smbus.SMBus(1)
ADDR = 0x6A

# Registers
CTRL1_XL = 0x10
CTRL2_G  = 0x11
CTRL3_C  = 0x12

# Initialize IMU
bus.write_byte_data(ADDR, CTRL3_C, 0x44)  # IF_INC + BDU
time.sleep(0.1)
bus.write_byte_data(ADDR, CTRL1_XL, 0x40)  # Accel: 104 Hz, +-2g
time.sleep(0.1)
bus.write_byte_data(ADDR, CTRL2_G, 0x40)   # Gyro: 104 Hz, +-245 dps
time.sleep(0.1)

def read_word(reg):
    """Read a 16-bit signed integer from the IMU."""
    data = bus.read_i2c_block_data(ADDR, reg, 2)
    val = (data[1] << 8) | data[0]
    if val & 0x8000:
        val -= 0x10000
    return val

# Correct scale factors for LSM6DSV16X (MKI178V2)
ACCEL_SENS = 0.000598  # m/s^2 per LSB  (0.061 mg/LSB)
GYRO_SENS  = 0.00875   # dps per LSB   (8.75 mdps/LSB)

print("Reading accelerometer & gyroscope...\n")

try:
    while True:
        # Raw readings
        ax_raw = read_word(0x28)
        ay_raw = read_word(0x2A)
        az_raw = read_word(0x2C)

        gx_raw = read_word(0x22)
        gy_raw = read_word(0x24)
        gz_raw = read_word(0x26)

        # Physical units
        ax = ax_raw * ACCEL_SENS
        ay = ay_raw * ACCEL_SENS
        az = az_raw * ACCEL_SENS

        gx = gx_raw * GYRO_SENS
        gy = gy_raw * GYRO_SENS
        gz = gz_raw * GYRO_SENS

        print(
            f"Accel (m/s^2): X={ax:6.2f}, Y={ay:6.2f}, Z={az:6.2f}  |  "
            f"Gyro (deg/s): X={gx:6.2f}, Y={gy:6.2f}, Z={gz:6.2f}",
            end="\r"
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

