#!/usr/bin/python3

import leglight
import pathlib
import json

# Discover's delay can be a bit annoying, so I store the result
# in a file and read from it. I update the file with discover if the
# IP address fails
script_location = pathlib.Path(__file__).parent.resolve()

def write_leglight_to_file():
    allLights = leglight.discover(2)
    my_light = allLights[0]
    light_vars = vars(my_light)
    with open(f'{script_location}/light.json', 'w') as file:
        file.write(json.dumps(light_vars, indent=2))

def read_from_file():
    with open(f'{script_location}/light.json', 'r') as file:
        light_vars = json.load(file)
        return light_vars

def get_light(vars):
    return leglight.LegLight(vars['address'], vars['port'])

try:
    file_light_vars = read_from_file()
    file_light = get_light(file_light_vars)
except:
    print("No light found. Searching for light")
    write_leglight_to_file()
    print("Trying again")
    file_light_vars = read_from_file()
    file_light = get_light(file_light_vars)

my_light_vars = vars(file_light)
my_light = get_light(my_light_vars)

if my_light_vars['isOn'] == 1:
    my_light.off()
else:
    my_light.on()