import serial
from .data import Data
from datetime import datetime, timezone
from .const import *
import re

timeout = 1


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
            self.tag_size = 15
            self.ser.write(b'sd2\r\n')

    def read(self):
        self.ser.reset_input_buffer()  # clean buffer
        self.ser.reset_output_buffer()  # clean buffer

        raw_tag = self.ser.read_until(size=self.tag_size + 6).decode()
        # byte count = OK + \r + \n + self.tag_size + \r + \n = 6 + self.tag_size

        if len(raw_tag) >= self.tag_size:  # Check that is got the expected size
            tag = self.matcher.findall(raw_tag)[0]
        else:
            return

        data = Data(CONFIG['box_id'], tag, datetime.now())
        return data
