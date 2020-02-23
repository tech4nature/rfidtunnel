import serial
import time
from data import Data
from datetime import datetime, timezone
from random import randint

timeout = 1


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

    def read(self):
        self.ser.reset_input_buffer()  # clean buffer
        self.ser.reset_output_buffer()  # clean buffer
        self.ser.write(b"sd2\r\n")  # set mode of rfid
        a = self.ser.read_until(size=19).decode(
            "utf-8"
        )  # 16 byte  + \r + \n somehow is 19 not 18
        if len(a) > 15:  # if read then return out of function
            tag = a
        else:
            tag = "TagNotPresent"  # return only if timed out

        data = Data(tunnel=randint(0, 1000), tag=tag[-16:], time=datetime.now(timezone.utc))
        return data
