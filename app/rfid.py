import serial
import time
from data import Data
from datetime import datetime, timezone
from random import randint
from json import load
from pathlib import Path
from json import loads
from json_minify import json_minify
from pathlib import Path
import re

timeout = 1
config = loads(json_minify(open(Path(__file__).absolute().parent.parent / 'config.json', 'r').read()))


# docs: http://www.priority1design.com.au/rfidrw-e-ttl.pdf

class sensor:
    def __init__(self, rfid_record_time):
        self.ser = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=rfid_record_time,
        )

        if config["rfid_tag_type"] == "EM4100":
            self.matcher = re.compile("[0-9A-F]{10}")
            self.tag_size = 10
        elif config["rfid_tag_type"] == "FDX-B":
            self.matcher = re.compile("[0-9]{3}_[0-9]{12}")
            self.tag_size = 15

    def read(self):
        self.ser.reset_input_buffer()  # clean buffer
        self.ser.reset_output_buffer()  # clean buffer

        if config["rfid_tag_type"] == "EM4100":
            self.ser.write(b'sd0\r\n')
        elif config["rfid_tag_type"] == "FDX-B":
            self.ser.write(b'sd2\r\n')

        raw_tag = self.ser.read_until(size=self.tag_size + 6).decode(
            "utf-8"
        )  # byte count = OK + \r + \n + self.tag_size + \r + \n = 6 + self.tag_size
        if len(raw_tag) >= self.tag_size + 6:  # Check that is got the expected size
            tag = self.matcher.findall(raw_tag)[0]
        else:
            return

        data = Data(tunnel=config['box_id'], tag=tag, time=datetime.now(timezone.utc))
        return data
