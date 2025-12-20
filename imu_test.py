import smbus, time
"""
Test IMU is powered
Read WHO_AM_I register
"""

bus = smbus.SMBus(1) # Open I2C bus #1
addr = 0x6A

while True:
    try:
        who = bus.read_byte_data(addr, 0x0F) # 0x0F = WHO_AM_I register
        print(f"WHO_AM_I: 0x{who:X}")
    except Exception as e:
        print("I2C error:", e)
    time.sleep(1)

