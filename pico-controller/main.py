from machine import Pin, I2C
import sys
import select
import time
import json

from mcp9808 import MCP9808

# Built-in led for heartbeat.
led = Pin(25, Pin.OUT)

# Pin numbers depend on where it is plugged in.
relays = {
    'relay_0': Pin(20, Pin.OUT),
    'relay_1': Pin(21, Pin.OUT)
}

# I2C pin numbers shouldn't need to change if using Pico.
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
temp_sensor = MCP9808(i2c)


def handle_input():
    data = dict()
    if select.select([sys.stdin], [], [], 0)[0]:
        # Read the stdin, which is mapped to serial for usb.
        line = sys.stdin.readline()
        try:
            # Try to parse json.
            data = json.loads(line)
        except Exception as e:
            # Otherwise just send raw.
            data['input'] = line 
    
    return data
        

while True:
    # Get user commands.
    serial_input = handle_input()

    output = dict(
        temp_c=temp_sensor.get_temp(),
        time=time.time(),
        serial_input=serial_input
    )

    # Check input for relay commands.
    for relay_name, relay in relays.items():
        try:
            # See if we have a working command for relay.
            cmd = getattr(relay, serial_input[relay_name])
            cmd()
        except (KeyError, AttributeError) as e:
            pass
        finally:
            # Get current value for output.
            output[relay_name] = bool(relay.value())
    
    # Send to stdout, which maps to serial for usb.
    print(json.dumps(output))
    
    # Heartbeat
    led.toggle()
    time.sleep(1)
    