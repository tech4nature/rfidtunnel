import smbus

bus = smbus.SMBus(1)
addr = 0x69


def firmware_id():
    return bus.read_byte_data(addr, 0)


def input_volts():
    return bus.read_byte_data(addr, 1) + (bus.read_byte_data(addr, 2) / 100)


def output_volts():
    return bus.read_byte_data(addr, 3) + (bus.read_byte_data(addr, 4) / 100)


def output_current():
    return bus.read_byte_data(addr, 5) + (bus.read_byte_data(addr, 6) / 100)


def power_mode():
    return bus.read_byte_data(addr, 7)


def shutdown_low_volts():
    return bool(bus.read_byte_data(addr, 8))


def get_address():
    return bus.read_byte_data(addr, 9)


def set_address(number):
    bus.write_byte_data(addr, 9, number)


def get_default():
    return bool(bus.read_byte_data(addr, 10))


def set_default_on(on):
    bus.write_byte_data(addr, 10, int(on))


def get_led_interval():
    return bus.read_byte_data(addr, 11)


def set_led_interval(seconds):
    if seconds in [1, 2, 4, 8]:
        mode = [1, 2, 4, 8].index(seconds) + 6
        bus.write_byte_data(addr, 11, mode)
    else:
        raise ValueError("Invalid amount of seconds supplied to set_led_interval: It needs to be 1, 2, 4 or 8!")


def get_voltage_threshold():
    threshold = bus.read_byte_data(addr, 12) / 10
    return threshold if threshold != 25.5 else "Disabled"


def set_voltage_threshold(voltage):
    if 2 <= voltage <= 25:
        bus.write_byte_data(addr, 12, voltage * 10)
    else:
        raise ValueError("Invalid voltage supplied to set_voltage_threshold: It needs to be 2.0 - 25.0,"
                         "or 0 if you want to disable the voltage threshold!")


def get_led_duration():
    duration = bus.read_byte_data(addr, 13)
    return duration if duration != 0 else "Disabled"


def set_led_duration(duration):
    if 0 <= duration <= 255:
        bus.write_byte_data(addr, 13, duration)
    else:
        raise ValueError("Invalid duration supplied to set_led_duration: It needs to be 0 - 255, where 0 disables it!")


def get_poweroff_delay():
    return bus.read_byte_data(addr, 14)


def set_poweroff_delay(delay):
    if 0 <= delay <= 8:
        bus.write_byte_data(addr, 14, delay * 10)
    else:
        raise ValueError("Invalid delay supplied to set_poweroff_delay: It needs to be 0 - 8!")


def get_recovery_threshold():
    threshold = bus.read_byte_data(addr, 12) / 10
    return threshold if threshold != 25.5 else "Disabled"


def set_recovery_threshold(voltage):
    if 2 <= voltage <= 25:
        bus.write_byte_data(addr, 12, voltage * 10)
    else:
        raise ValueError("Invalid voltage supplied to set_voltage_threshold: It needs to be 2.0 - 25.0,"
                         "or 0 if you want to disable the voltage threshold!")


def get_load_duration():
    duration = bus.read_byte_data(addr, 16)
    return duration if duration != 0 else "Disabled"


def set_load_duration(duration):
    if 0 <= duration <= 255:
        bus.write_byte_data(addr, 16, duration)
    else:
        raise ValueError("Invalid duration supplied to set_load_duration: It needs to be 0 - 255, where 0 disables it!")
