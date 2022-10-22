'''
Toggles Elgato key light
'''
import leglight

my_light = leglight.LegLight('192.168.0.48',9123)
light_vars = vars(my_light)

if light_vars['isOn'] == 1:
    my_light.off()
else:
    my_light.on()
