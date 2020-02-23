class Data:
    def __init__(self, tunnel, tag, time):
        self.tunnel = tunnel
        self.tag = tag
        self.time = time

    def get_date(self):
        return self.time.strftime('%Y-%m-%d')

    def get_time(self):
        return self.time.strftime('%H:%M:%S')
