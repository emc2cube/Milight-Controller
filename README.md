# Milight-Controller

Simple Python script to control wifi LED lights from various brands:
* MiLight
* LimitlessLED
* AppLight
* AppLamp
* LEDme
* dekolight
* iLight
* EasyBulb

# Usage:
```.py
./milight.py -i <wifi_bridge_ip> -p <wifi_bridge_port> -g <light_group> -c <command> -b <brightness_level>
```

# Available options:
## Light Group (-g)
0 (or "all"), 1, 2, 3 and 4.

## Commands (-c)
Basic commands: on, off, white
Colors: blue, aqua, cyan, mint, green, lime, yellow, orange, red, pink, fuchsia, purple.
Special modes: fade_rainbow, fade_white, fade_rgbw, blink_rainbow, blink_random, blink_red, blink_green, blink_blue, fade_blink_all.
Setings: faster, slower to change special mode animation speed. You can also use "disco" to go to the next special mode as you would do on the remote or smartphone application.

## Brightness (-b)
Integer between 0 (dimest setting) and 25 (brightest).

# Exemples:
Turn all the lights to white with a 50% brightness level:
```.py
./milight.py -i 10.0.0.100 -p 8899 -g all -c white -b 13
```

Turn the light group 2 into a fading rainbow animation, max brightness:
```.py
./milight.py -i 10.0.0.100 -p 8899 -g 2 -c fade_rainbow -b 25
```

Switch the light group 4 off:
```.py
./milight.py -i 10.0.0.100 -p 8899 -g 4 -c off
```

# Mac OS X application (10.9+)
Simple GUI using this python script to control your lights. Maybe one day I will try to do a full obj-c version using an UDP library to send the commands, but for now it's working like that.
The application is not signed by a dev certificate so you may have to change your settings of gatekeeper to launch it. You may also force it's first launch by doing right click -> open and then allowing its launch by the system.
