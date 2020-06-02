# import subprocess
# from gpiozero import Button
# import json

# button = Button(2)
# state = json.load(open('state.json', 'r'))

# while True:
#     if button.is_pressed and state['hotspot'] == 0:
#         print("Enabling HotSpot")
#         state['hotspot'] = 1
#         json.dump(state, open('state.json', 'w'))
#         subprocess.run(['sudo', 'cp', '/boot/config.txt.orig', '/boot/config.txt'])
#         subprocess.run(['sudo', 'systemctl', 'enable', 'dnsmasq'])
#         subprocess.run(['sudo', 'systemctl', 'enable', 'hostapd'])
#         subprocess.run(['sudo', 'reboot'])

#     if button.is_pressed and state['hotspot'] == 1:
#         print('Disabling HotSpot')
#         state['hotspot'] = 0
#         json.dump(state, open('state.json', 'w'))
#         subprocess.run(['sudo', 'cp', '/boot/config.txt',  '/boot/config.txt.orig'])
#         subprocess.run(['sudo', 'echo', 'dtoverlay=pi3-disable-wifi', '>>', '/boot/config.txt'])
#         subprocess.run(['sudo', 'systemctl', 'disable', 'dnsmasq'])
#         subprocess.run(['sudo', 'systemctl', 'disable', 'hostapd'])
#         subprocess.run(['sudo', 'reboot'])