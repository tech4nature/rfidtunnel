from datetime import datetime, timedelta, date
from pathlib import Path
from shutil import copyfile
from subprocess import run
from logging import getLogger
from json import load

logger = getLogger(__name__)

class Schedule:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end
        self.ons = []
        self.offs = []


    def on(self, on_for: timedelta):
        if len(self.ons) != len(self.offs):
            logger.error('ONs and OFFs are declared incorrectly!')
            return

        self.ons.append(on_for)
        logger.info('ON added successfully')
    
    def off(self, off_for: timedelta):
        if len(self.ons) - 1 != len(self.offs):
            logger.error('ONs and OFFs are declared incorrectly!')
            return
        
        if (off_for.days * 86400) + off_for.seconds >= 61200:
            logger.warning('OFF {off_for} too large, the battery will run out! The max is 17 hrs.') 
            return

        self.offs.append(off_for)
    
    def save(self, name: str):
        if len(self.ons) != len(self.offs):
            logger.error('ONs and OFFs are declared incorrectly!')
            return
        
        schedule = ''
        schedule += f'BEGIN {self.start.strftime("%Y-%m-%d %H:%M:%S")} \n'
        schedule += f'END {self.end.strftime("%Y-%m-%d %H:%M:%S")} \n'
        
        for i in range(len(self.ons)):
            schedule += f'ON S{self.ons[i].seconds} \n'
            schedule += f'OFF S{self.offs[i].seconds} \n'
        
        self.schedules_path = Path.home() / 'wittyPi' / 'schedules'
        self.schedule_file = open(self.schedules_path / (name + '.wpi'), 'w+')
        self.schedule_file.write(schedule)
        self.schedule_file.close()

        logger.info(f'Schedule saved as {self.schedule_file}')

    def run(self):
        copyfile(str(self.schedule_file.name), str(self.schedules_path.parent / 'schedule.wpi'))
        run(['sudo', str(self.schedules_path.parent / 'runScript.sh')])
        logger.info(f'Running schedule: {self.schedule_file}')


if __name__ == "__main__":
    config = load(open(Path(__file__).absolute().parent.parent / 'config.json', 'r'))

    start = datetime.strptime(config['starttime'], '%H:%M:%S')
    end = datetime.strptime(config['endtime'], '%H:%M:%S')

    startfull = datetime.strptime(
        config['startdate'] + config['starttime'], '%d/%m/%Y%H:%M:%S')
    endfull = datetime.strptime(
        config['enddate'] + config['endtime'], '%d/%m/%Y%H:%M:%S')


    diff = end - start
    if diff.days == -1:
        diff += timedelta(days=1)

    schedule = Schedule(startfull, endfull)

    schedule.on(diff)
    schedule.off(timedelta(minutes=5))
    schedule.on(timedelta(minutes=5))
    schedule.off(timedelta(days=1) - diff - timedelta(minutes=10))

    schedule.save('test')
    schedule.run()

