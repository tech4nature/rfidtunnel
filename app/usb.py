import subprocess
from json import dump, load
from logging import getLogger
from os import listdir

logger = getLogger(__name__)


def check_for_mount(usb_state):
    if not usb_state:
        subprocess.run(['sudo', 'udisksctl', 'power-off', '-b', '/dev/sda'])  # Power off USB drive to save power

    if usb_state:
        subprocess.run(['sudo', 'udisksctl', 'mount', '-b', '/dev/sda1'])  # Mount USB drive


def get_mounted_dir():
    return '/media/root/' + listdir('/media/root/')[0] + '/'