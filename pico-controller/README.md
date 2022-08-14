# pico controller

The [pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) is running [micropython](https://micropython.org/) and is most easily edited using [thonny](https://thonny.org/).

The [main.py](main.py) program runs by default when the pico is powered on. The program runs in a loop and collects the current temperature as well as the status of the relays.  It outputs text in a json format and includes a timestamp in unix epoch time (the pico, unlike a normal raspberry pi, has a real-time clock) as well as copy of the [serial input](#input). 

## Output
<a name="output"></a>

An example output looks like:

```json
{"time": 1660466250, "relay_1": false, "relay_0": false, "temp_c": 26.875, "serial_input": {}}
```

## Input
<a name="input"></a>

The pico can accept serial input to control the relays. The input should be given in the following format:

```json
{"relay_0":"on"}
```

Both relays can be specified at once:

```json
{"relay_0":"on", "relay_1": "off"}
```

The relays can also be toggled from their current state:

```json
{"relay_0":"toggle", "relay_1": "toggle"}
```

The result of the given command will be immediately reflected in the output. Here is the reading immediately before the command is received and when the command is received. The relays reflect the state (`true`) of the `serial_input` from the same line.

```json
{"time": 1660465915, "relay_1": false, "relay_0": false, "temp_c": 26.3125, "serial_input": {}}
{"time": 1660465916, "relay_1": true, "relay_0": true, "temp_c": 26.3125, "serial_input": {"relay_1": "toggle", "relay_0": "toggle"}}
```

### Command line

The relays can be controlled directly from the command line by doing an `echo` directly to the serial input device, shown here as `/dev/ttyACM0`:

```bash
$ echo '{"relay_0":"off", "relay_1":"on"}' > /dev/ttyACM0
```

The output can be monitored in a separate terminal with `pyserial-miniterm`:

```bash
$ pyserial-miniterm /dev/ttyACM0
--- Miniterm on /dev/ttyACM0  9600,8,N,1 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
{"time": 1609459204, "relay_1": false, "relay_0": false, "temp_c": 26.8125, "serial_input": {}}
{"time": 1609459205, "relay_1": false, "relay_0": false, "temp_c": 26.75, "serial_input": {}}
{"time": 1609459206, "relay_1": false, "relay_0": false, "temp_c": 26.8125, "serial_input": {}}
{"time": 1609459207, "relay_1": false, "relay_0": true, "temp_c": 26.8125, "serial_input": {"relay_1": "off", "relay_0": "on"}}
{"time": 1609459208, "relay_1": false, "relay_0": true, "temp_c": 26.8125, "serial_input": {}}
{"time": 1609459209, "relay_1": false, "relay_0": true, "temp_c": 26.8125, "serial_input": {}}

```