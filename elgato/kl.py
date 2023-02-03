'''
Toggles Elgato key light

Finds the Elgato light based on MAC address, so if you lose power
and the light's IP address changes, the script will still be able
to locate it.
'''
import subprocess
import leglight
import re
import os
from dotenv import load_dotenv

mac_address = os.getenv('MAC_ADDRESS')

run_arp = subprocess.Popen(['arp', '-an'], stdout=subprocess.PIPE)
run_grep = subprocess.Popen(
    ['grep', mac_address],
    stdin=run_arp.stdout,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
    )

run_arp.stdout.close()
out, err = run_grep.communicate()

ip_string = out.decode('utf-8')
ip = re.search('(?<=\().*?(?=\))', ip_string)

my_light = leglight.LegLight(ip.group(),9123)
light_vars = vars(my_light)

if light_vars['isOn'] == 1:
    my_light.off()
else:
    my_light.on()