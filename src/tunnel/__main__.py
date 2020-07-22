from logging.handlers import RotatingFileHandler
from shutil import copyfile
import logging
from csv import DictWriter
import os
from time import time
from typing import Optional
import subprocess

from .const import *
from .usb import mount, poweroff
from .rfid import RFID
from .wittypi import *

logger: logging.Logger = logging.getLogger("tunnel")
rfid = RFID()


def start():
    mounted_dir: Optional[Path] = None
    disk_path: Optional[Path] = None

    try:
        mounted_dir, disk_path = mount()
    except Exception:
        pass

    set_voltage_threshold(float(CONFIG['voltage_threshold']))
    set_recovery_threshold(float(CONFIG['recovery_threshold']))

    try:
        open(DATA_DIR / 'data.csv', 'r')
    except FileNotFoundError:
        csv_file = open(DATA_DIR / 'data.csv', 'a+')
        fieldnames = ['Tunnel', 'Ppt Tag', 'Time', 'Date']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    if mounted_dir and disk_path:
        try:
            copyfile(DATA_DIR / 'tunnel.log', mounted_dir / 'tunnel.log')
            copyfile(DATA_DIR / 'data.csv', mounted_dir / 'data.csv')
            logger.info("Files Copied")
        except Exception as e:
            logger.error("This happened during copying files to the USB stick: " + str(e))

        poweroff(disk_path)

    logger.info("Syncing time and schedule!")
    witty_pi = Path.home() / 'wittypi'
    subprocess.run(['sudo', 'bash', str(witty_pi / 'syncTime.sh')])
    subprocess.run(['sudo', 'bash', str(witty_pi / 'runScript.sh')])


def loop():
    data = rfid.read()
    if data:
        logger.info(f'Got {data.tag}')
        csv_file = open(DATA_DIR / 'data.csv', 'a+')
        fieldnames = ['Tunnel', 'Pit Tag', 'Time', 'Date']
        writer = DictWriter(csv_file, fieldnames=fieldnames)

        writer.writerow({
            'Tunnel': data.tunnel,
            'Pit Tag': data.tag,
            'Time': data.get_time(),
            'Date': data.get_date()
        })


def log_power():
    logger.debug(f"VIN: {input_volts()}")
    logger.debug(f"VOUT: {output_volts()}")
    logger.debug(f"IOUT: {output_current()}")


if __name__ == "__main__":
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    file_handler = RotatingFileHandler(str(DATA_DIR / 'tunnel.log'), maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    power_log_time = 0

    start()

    while True:
        if time() - power_log_time > CONFIG['power_log_time']:
            log_power()
            power_log_time = time()

        loop()
