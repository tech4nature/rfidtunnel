from subprocess import run
from datetime import datetime

if __name__ == "__main__":
    print("Finding address of Tunnel...")
    ip = "192.168.100.62"
    # for i in range(2, 255):
    #     ping = run(['ping', f'10.42.0.{i}', '-c', '3'])
    #     if ping.returncode == 0:
    #         ip = f'10.42.0.{i}'
    #         print(f"Found Tunnel at {ip}")
    #         break

    if ip == 0:
        print("No Tunnel was found, make sure its connected!")
        exit()

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

    tunnel_id = input("Enter the tunnel id you would like to use: ")
    run(['ssh', f'pi@{ip}', '/home/pi/.pyenv/shims/python', 'src/set_box_id.py', tunnel_id])
