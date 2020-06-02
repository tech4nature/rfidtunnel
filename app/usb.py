import subprocess
from logging import getLogger
from os import listdir, path

logger = getLogger(__name__)


def poweroff():
    if path.exists('/dev/sda'):
        logger.debug('USB found!')
        subprocess.run(['sudo', 'udisksctl', 'unmount', '-b', '/dev/sda1'])
        subprocess.run(['sudo', 'udisksctl', 'power-off', '-b', '/dev/sda'])  # Power off USB drive to save power
        logger.info('USB powered down')


def mount():
    if path.exists('/dev/sda'):
        logger.debug('USB found!')
        subprocess.run(['sudo', 'udisksctl', 'mount', '-b', '/dev/sda1'])  # Power off USB drive to save power
        logger.info('USB mounted')



def get_mounted_dir():
    try:
        return '/media/root/' + listdir('/media/root/')[0] + '/'
        
    except Exception as e:
        logger.error(f'Error during trying to find mounted dir: \n {e}')
        