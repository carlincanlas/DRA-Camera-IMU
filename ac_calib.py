#!/usr/bin/env python3
import smbus
import time
from math import sqrt

bus = smbus.SMBus(1)
ADDR = 0x6A

OUTX_L_A = 0x28

# initial sensitivity used in your logger (m/s^2 per LSB)
ACCEL_SENS_INIT = 0.000598  # 0.061 mg/LSB

def read_word(reg):
    data = bus.read_i2c_block_data(ADDR, reg, 2)
    val = (data[1] << 8) | data[0]
    if val & 0x8000:
        val -= 0x10000
    return val

def collect_raw(n=300, delay=0.01):
    axs = []
    ays = []
    azs = []
    print(f"Collecting {n} samples ? keep board still and flat...")
    for _ in range(n):
        axs.append(read_word(OUTX_L_A + 0))
        ays.append(read_word(OUTX_L_A + 2))
        azs.append(read_word(OUTX_L_A + 4))
        time.sleep(delay)
    return axs, ays, azs

if __name__ == "__main__":
    ax_list, ay_list, az_list = collect_raw(n=300, delay=0.01)

    ax_mean = sum(ax_list) / len(ax_list)
    ay_mean = sum(ay_list) / len(ay_list)
    az_mean = sum(az_list) / len(az_list)

    print(f"\nRaw means: ax={ax_mean:.2f}, ay={ay_mean:.2f}, az={az_mean:.2f}")

    g = 9.80665
    measured_sensitivity = g / az_mean
    print(f"Measured sensitivity (m/s^2 per LSB): {measured_sensitivity:.9f}")

    scale = measured_sensitivity / ACCEL_SENS_INIT
    print(f"Scale factor to apply to converted m/s^2 values: {scale:.6f}")

    # compute biases in LSB
    ax_bias = ax_mean
    ay_bias = ay_mean
    # remove 1g (in LSB) from az_mean to get zero-motion bias in LSB for Z
    raw_eq_for_1g_init = g / ACCEL_SENS_INIT
    az_bias = az_mean - raw_eq_for_1g_init

    print("\nBiases (LSB):")
    print(f"AX_BIAS = {ax_bias:.6f}")
    print(f"AY_BIAS = {ay_bias:.6f}")
    print(f"AZ_BIAS = {az_bias:.6f}  # this already has 1g removed")
    print(f"\nCopy these 4 numbers into your logger.")
