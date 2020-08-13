import serial
from .data import Data
from datetime import datetime
from .const import *
import re
from logging import getLogger

logger = getLogger("tunnel.rfid")


# docs: http://www.priority1design.com.au/rfidrw-e-ttl.pdf

class RFID:
    def __init__(self):
        self.ser = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=CONFIG['rfid_timeout'],
        )

        if CONFIG["rfid_tag_type"] == "EM4100":
            self.matcher = re.compile("[0-9A-F]{10}")
            self.tag_size = 10
            self.ser.write(b'sd0\r\n')
        elif CONFIG["rfid_tag_type"] == "FDX-B":
            self.matcher = re.compile("[0-9]{3}_[0-9]{12}")
            self.tag_size = 16
            self.ser.write(b'sd2\r\n')

    def read(self):
        self.ser.reset_input_buffer()  # clean buffer
        self.ser.reset_output_buffer()  # clean buffer

        raw_tag = self.ser.read_until(size=self.tag_size + 1)
        logger.debug(f"Raw RFID data is: {raw_tag}")
        # byte count = self.tag_size + \r = self.tag_size + 1

        try:
            tag = self.matcher.findall(raw_tag.decode())[0]  # Decode uses the UTF-8 codec
        except:
            return

        data = Data(CONFIG['box_id'], tag, datetime.now())  # Instantiate data class
        return data
