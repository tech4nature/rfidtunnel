import logging
import usb
from json import load, dump

logger = logging.get_logger(__name__)
state = load(open('state.json', 'r'))


def main():
    # SETUP

    global logger
    global state

    # USB

    usb.check_for_mount(state['usb'])

    if state['usb']:
        logger.info("USB Mounted")
    else:
        logger.info("USB Unmounted")

    # TODO: Setup USB Copy if state == True

    state['usb'] = not state['usb']  # Invert usb state
    logger.debug("USB State Inverted")

    # 


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
