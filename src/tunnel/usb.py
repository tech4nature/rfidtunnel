import logging
from os import path, walk
from pathlib import Path
from subprocess import run
from typing import Optional, Tuple

logger = logging.getLogger("tunnel.usb")


def mount() -> Optional[Tuple]:
    if path.exists(Path('/') / 'dev' / 'sda'):
        logger.debug('USB Found')
        run(['sudo', 'udisksctl', 'mount', '-b', '/dev/sda1'])
        logger.info('USB Mounted')

        for filepath in Path('/media/root').glob('*'):
            return filepath, Path('/dev/sda1')

    else:
        logger.warning('USB not found, skipping mount and copy')


def poweroff(disk_path: Optional[Path] = None) -> None:
    if not disk_path:
        logger.warning('No path was specified to demount, there is most likely a warning above saying the USB was not '
                       'found...')
        return

    if path.exists(str(disk_path)):
        logger.debug('Mounted USB found')
        run(['sudo', 'udisksctl', 'unmount', '-b', '/dev/sda1'])
        logger.info("USB Demounted")
        run(['sudo', 'udisksctl', 'power-off', '-b', '/dev/sda'])  # Power off to save power
        logger.info("USB Powered Off")
    else:
        logger.warning('Although a path was provided, a mounted USB was not found.')
