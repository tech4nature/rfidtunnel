from subprocess import run
from datetime import datetime
import string
from time import sleep


def get_times():
    while True:
        try:
            start = int(input("Enter the hour you want the tunnel to start at: "))
            end = int(input("Enter the hour you want the tunnel to end at: "))
            break
        except ValueError:
            print("Please write the values in the correct format!")

    return start, end


if __name__ == "__main__":
    try:
        print("Finding address of Tunnel...")
        nmap = run(['nmap', '-T5', '-sP', '10.42.0.1-255'], capture_output=True).stdout.decode()
        ip = nmap.split('\n')[3][21:]
        print(ip)
    except:
        print("The tunnel could not be found, make sure its turned on and plugged in!")
        input()
        exit()

    action = int(input("""
Enter what you would like to do today:
1) Sync the time
2) Set the tunnel id
3) Schedule when the tunnel runs
4) Delete the data off the tunnel
5) Shutdown the tunnel
"""))

    if action == 1:
        print("Checking time...")
        host_date = datetime.now()

        remote_raw_date = run(['ssh', f'pi@{ip}', 'date'], capture_output=True).stdout.decode()[4:19]
        remote_date = datetime.strptime(remote_raw_date, '%d %b %H:%M:%S').replace(year=host_date.year)

        print(f"Host time is: {host_date}")
        print(f"Tunnel's time is: {remote_date}")

        diff = (host_date - remote_date).total_seconds()
        if diff < 0:
            diff = -diff

        if diff > 60:
            print("Difference in time is too large, syncing time!")
            run(['ssh', f'pi@{ip}', 'sudo', 'bash', '/home/pi/wittypi/syncTime.sh'])
            run(['ssh', f'pi@{ip}', 'sudo', 'bash', '/home/pi/wittypi/runScript.sh', '>>', '/dev/null'])
            print("Sync successful!")
        else:
            print("Time is correct!")

    elif action == 2:
        while True:
            tunnel_id = input(
                "Enter the tunnel id you would like to use, it has to only have letters or numbers and no spaces: "
            )

            invalid = False

            for i in tunnel_id:
                if i not in string.ascii_letters + string.digits:
                    print("Box id is invalid, try again!")
                    invalid = True

            if not invalid:
                break

        run(['ssh', f'pi@{ip}', '/home/pi/.pyenv/shims/python', '-m', 'src.tunnel.set_box_id', tunnel_id])

    elif action == 3:
        print("The format for entering the times is in 24 hour clock, only include hours, for example 3pm is 15 and "
              "2am is 2!")
        while True:
            start, end = get_times()
            diff = end - start
            diff = diff if diff >= 0 else diff + 24

            if start not in range(0, 24) or end not in range(0, 24):
                print("Time is not in range please enter it properly")

            elif diff == 0:
                print("You cannot have the same time as both the end and start time!")

            elif diff > 12:
                print(
                    "The system is not designed to run for more than 12 hours per day and most likely will run for less "
                    "than 2 weeks"
                )
                while True:
                    yesno = input("Is this ok (yes/ no)? ")
                    if yesno.lower() not in ['yes', 'no']:
                        print("You did not enter a yes or a no, please enter it properly!")
                    else:
                        break
                if yesno == 'yes':
                    break
            else:
                break

        schedule = run(
            [
                'ssh', f'pi@{ip}', '/home/pi/.pyenv/shims/python', '-m', 'src.tunnel.schedule', str(start), str(end),
                '>>', '/dev/null'
            ],
            capture_output=True
        ).stderr.decode()

        if not schedule:
            print("Schedule successfully written!")
        else:
            print("Something went wrong, please try again!")

    elif action == 4:
        run(['ssh', f'pi@{ip}', 'sudo', 'pkill', '-f', 'python'])
        run(['ssh', f'pi@{ip}', 'rm', 'data/data.csv'])
        print("Data deleted!")

    elif action == 5:
        run(['ssh', f'pi@{ip}', 'sudo', 'poweroff'])
        print("Please wait for the tunnel shutdown!")
        sleep(10)
        print("Tunnel is shutdown!")

    input("Press Enter to exit...")
