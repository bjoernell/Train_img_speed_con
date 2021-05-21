from smbus import SMBus
#i2c addr:
addr = 0x08
bus = SMBus(1)

def transmitSpeed(pwm):
        ipwm = int (pwm)
        bus.write_byte(addr, ipwm)