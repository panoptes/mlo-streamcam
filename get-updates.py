#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime as dt
import time

from panoptes.utils.serializers import from_json, to_json
from panoptes.utils.serial.device import SerialDevice


def main():
    device = SerialDevice(port='/dev/ttyACM0', reader_callback=from_json)
    time_path = Path('time.txt')
    pico_log = Path('pico-log.json')

    while True:
        with time_path.open('w') as f0, pico_log.open('a') as f1:
            try:
                # Write to the time.txt file, include the temperature.
                f0.write(f'{dt.now():%c} HST {device.readings[-1]["temp_c"]:10.01f}° C')

                # Write the readings.
                f1.write(to_json(device.readings[-1]) + '\n')
            except Exception as e:
                print(e)

        time.sleep(1)

if __name__ == '__main__':
    main()
