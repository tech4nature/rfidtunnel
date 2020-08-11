import sys
from datetime import datetime, timedelta
from pathlib import Path
from subprocess import run


if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    diff = end - start if end - start > 0 else end + 24 - start
    off_time = timedelta(days=1) - timedelta(hours=diff) - timedelta(minutes=10)

    schedule = f"""BEGIN {datetime.now().replace(hour=start).strftime(f"%Y-%m-%d %H:00:00")}
    END {datetime.now().replace(hour=start).strftime(f"2030-%m-%d %H:00:00")}
    
    ON H{diff}
    OFF M5
    ON M5
    OFF S{off_time.seconds}
    """.replace('    ', '')

    schedule_file = str(Path.home() / 'wittypi' / 'schedule.wpi')
    open(schedule_file, 'a+')
    open(schedule_file, 'w').write(schedule)

    run(['sudo', 'bash', str(Path.home() / 'wittypi' / 'runScript.sh')])
