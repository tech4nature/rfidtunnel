from subprocess import run
from datetime import datetime


if __name__ == "__main__":
    try:
        print("Finding address of Tunnel...")
        nmap = run(['nmap', '-T5', '-sP', '10.42.0.1-255'], capture_output=True).stdout.decode()
        ip = nmap.split('\n')[3][21:]
    except:
        print("The tunnel could not be found, make sure its turned on and plugged in!")
        input()
        exit()

    action = int(input("""
Enter what you would like to do today:
1) Sync the time
2) Set the tunnel id
3) Schedule when the tunnel runs
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
            run(['ssh', f'pi@{ip}', 'sudo', 'bash', '/home/pi/wittypi/runScript.sh'])
        else:
            print("Time is correct!")

    if action == 2:
        tunnel_id = input("Enter the tunnel id you would like to use: ")
        run(['ssh', f'pi@{ip}', '/home/pi/.pyenv/shims/python', '-m', 'src.tunnel.set_box_id', tunnel_id])

    if action == 3:
        start = input("Enter the hour you want the tunnel to start at: ")
        end = input("Enter the hour you want the tunnel to end at: ")

        run(['ssh', f'pi@{ip}', '/home/pi/.pyenv/shims/python', '-m', 'src.tunnel.set_box_id', start, end])

    input("Press Enter to exit...")
