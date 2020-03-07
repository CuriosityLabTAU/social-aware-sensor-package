#!/usr/bin/env python
import usb.util
from tuning import Tuning

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
mic_tuning = Tuning(dev)
while True:
    if mic_tuning.is_voice() == 1:
        direction_str = (360 - mic_tuning.direction) * 1280 / 360
        print(direction_str)
        break
