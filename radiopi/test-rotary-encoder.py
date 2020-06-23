# -*- encoding: utf-8 -*-
from __future__ import print_function

import evdev
import select

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

value = 1
print("Value: {0}".format(value))

done = False
while not done:
    r, w, x = select.select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            event = evdev.util.categorize(event)
            if isinstance(event, evdev.events.RelEvent):
                value = value + event.event.value
                print("Value: {0}".format(value))
            elif isinstance(event, evdev.events.KeyEvent):
                if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                    print("Enter...")
                    done = True
                    break
