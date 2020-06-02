import usb
from json import loads
import subprocess
import csv
import logging.handlers
import os
import rfid
from pathlib import Path
from time import time
from json_minify import json_minify
import wittypi

config = loads(json_minify(open(Path(__file__).absolute().parent.parent / 'config.json', 'r').read()))
logger = logging.getLogger(__name__)
rfid = rfid.sensor(config['rfid_timeout'])


def init():
    # SETUP

    global logger
    global rfid

    open('/home/pi/log.csv', 'a+')  # Create file

    # WRITE HEADERS

    if os.stat("/home/pi/log.csv").st_size == 0:
        with open('/home/pi/log.csv', mode='a+') as csv_file:
            fieldnames = ['Tunnel', 'Ppt Tag', 'Time', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    # COPY FILES

    usb.mount()
    drive_dir = usb.get_mounted_dir()

    if drive_dir != None:
        subprocess.run(['sudo', 'cp', '/home/pi/log.csv', drive_dir])
        subprocess.run(['sudo', 'cp', '/home/pi/wittypi/wittyPi.log', drive_dir])
        subprocess.run(['sudo', 'cp', '/home/pi/tunnel.log', drive_dir])

        usb.poweroff()
        logger.info('Files Copied')


def main():
    # READ RFID AND WRITE TO CSV

    data = rfid.read()
    if data.tag != "TagNotPresent":
        with open('/home/pi/log.csv', mode='a+') as csv_file:
            fieldnames = ['Tunnel', 'Pit Tag', 'Time', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({
                'Tunnel': data.tunnel,
                'Pit Tag': data.tag,
                'Time': data.get_time(),
                'Date': data.get_date()
            })


def log_power():
    logger.debug(f"Vin: {wittypi.input_volts()}")
    logger.debug(f"Vout: {wittypi.output_volts()}")
    logger.debug(f"Iout: {wittypi.output_current()}")


if __name__ == "__main__":
    # Setup logging to record into a file called tunnel.log, tunnel.log is limited to 1KiB, once the file is full,
    # it will copy the contents of tunnel.log into another file: tunnel.log.1. This process is then repeated until it
    # reaches hedge.log.5, after this point the last backup, hedge.log.5, will be deleted.
    # More extensive explanation: https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler

    formatter = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'

    logging.basicConfig(filename='tunnel.log', level=logging.DEBUG, format=formatter)

    init()

    power_log_last_ran = 0

    while True:
        main()

        if time() - power_log_last_ran > config['power_log_time']:
            log_power()
            power_log_last_ran = time()
