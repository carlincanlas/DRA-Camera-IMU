import smbus
import time
from math import sqrt

bus = smbus.SMBus(1)
ADDR = 0x6A

def read_word(reg):
    data = bus.read_i2c_block_data(ADDR, reg, 2)
    val = (data[1] << 8) | data[0]
    if val & 0x8000:
        val -= 0x10000
    return val

ACCEL_SENS = 0.000598   # m/s^2 per LSB
                        # 0.061 mg = 0.061 × 9.80665 × 10⁻³ m/s² ≈ 0.000598 m/s²
for i in range(50):
    ax_raw = read_word(0x28)
    ay_raw = read_word(0x2A)
    az_raw = read_word(0x2C)

    ax = ax_raw * ACCEL_SENS
    ay = ay_raw * ACCEL_SENS
    az = az_raw * ACCEL_SENS

    mag = sqrt(ax*ax + ay*ay + az*az)
    print(f"raw: {ax_raw:6d},{ay_raw:6d},{az_raw:6d} | m/s2: {ax:6.3f},{ay:6.3f},{az:6.3f} | |a|={mag:5.3f}")
    time.sleep(0.1)
