#!/usr/bin/python

'''
- Starts tidal-hifi
- Links LastFM to tidal-hifi with rescrobbled
    - https://github.com/Mastermindzh/tidal-hifi
    - https://github.com/InputUsername/rescrobbled

Prereqs:
- playerctrl
- tidal-hifi
- rescrobbled
- last.fm api key as LAST_FM_API_KEY
- last.fm secret as LAST_FM_SECRET
'''
import subprocess, re, os

LAST_FM_API_KEY = os.environ['LAST_FM_API_KEY']
LAST_FM_SECRET = os.environ['LAST_FM_SECRET']

chromium_only = r'chromium.instance(?:.*)\n'

print('Stopping rescrobbled service')
subprocess.run(['systemctl', '--user', 'stop', 'rescrobbled.service'])
print('Running Tidal')
subprocess.Popen(['nohup', 'tidal-hifi', '&'])

print('Finding chromium_instance')
playerctl_run = subprocess.run(['playerctl', '--list-all'], stdout=subprocess.PIPE)
player_lists = playerctl_run.stdout.decode('utf-8')
chromium_instance = re.match(chromium_only, player_lists).group().strip()

new_file = '''
lastfm-key = "{}"
lastfm-secret = "{}"
player-whitelist = ["{}"]
'''.format(LAST_FM_API_KEY, LAST_FM_SECRET, chromium_instance)

print('Writing new config file')
with open("/home/heston/.config/rescrobbled/config.toml", "w") as old_file:
    old_file.write(new_file)

print('Starting Rescrobbled service')
subprocess.run(['systemctl', '--user', 'start', 'rescrobbled.service'])
