from subprocess import run
from json import dump, load
from logging import getLogger

logger = logging.getLogger(__name__)


def check_for_mount(usb_state):
    if not usb_state:
        run('sudo', 'udisksctl', 'power-off', '-b', '/dev/sda')  # Power off USB drive to save power

    if usb_state:
        run('sudo', 'udisksctl', 'mount' '-b', '/dev/sda')  # Mount USB drive
