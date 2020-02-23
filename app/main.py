import logging
import usb
from json import load, dump
import subprocess
from datetime import datetime, timezone
import csv
import logging.handlers
import os
import rfid

logger = logging.getLogger(__name__)
state = load(open('state.json', 'r'))
rfid = rfid.sensor(45)


def main():
    # SETUP

    global logger
    global state

    open('/home/pi/log.csv', 'a+')  # Create file

    # USB MOUNT/ POWER OFF

    usb.check_for_mount(state['usb'])

    if state['usb']:
        logger.info("USB Mounted")
    else:
        logger.info("USB Powered Down")

    # WRITE HEADERS

    if os.stat("/home/pi/log.csv").st_size == 0:
        with open('/home/pi/log.csv', mode='a+') as csv_file:
            fieldnames = ['Tunnel', 'Ppt Tag', 'Time', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    # READ RFID AND WRITE TO CSV

    data = rfid.read()

    with open('/home/pi/log.csv', mode='a+') as csv_file:
        fieldnames = ['Tunnel', 'Pit Tag', 'Time', 'Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writerow({
            'Tunnel': data.tunnel,
            'Pit Tag': data.tag,
            'Time': data.get_time(),
            'Date': data.get_date()
        })

    # COPY FILES

    if state['usb']:
        drive_dir = usb.get_mounted_dir()

        subprocess.run(['sudo', 'cp', '/home/pi/log.csv', drive_dir])

        logger.info('Files Copied')

    state['usb'] = not state['usb']  # Invert usb state
    logger.debug("USB State Inverted")

    # STORE STATE
    
    dump(state, open('state.json', 'w'))


if __name__ == "__main__":
    # Setup logging to record into a file called tunnel.log, tunnel.log is limited to 1KiB, once the file is full,
    # it will copy the contents of tunnel.log into another file: tunnel.log.1. This process is then repeated until it
    # reaches hedge.log.5, after this point the last backup, hedge.log.5, will be deleted.
    # More extensive explanation: https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler

    handler = logging.handlers.RotatingFileHandler(
        filename="tunnel.log", maxBytes=1024 * 1024, backupCount=5
    )
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)

    main()
