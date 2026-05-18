#!/usr/bin/env python3
"""Read and control settings on a Moondrop Dawn Pro via USB."""

import os
import sys
import time
import usb.core

DAWN_PRO_VID = 0x2FC6
DAWN_PRO_PID = 0xF06A

FILTER_NAMES = [
    "Fast Roll-off Low Latency",
    "Fast Roll-off Phase Compensated",
    "Slow Roll-off Low Latency",
    "Slow Roll-off Phase Compensated",
]
GAIN_NAMES = ["Low", "High"]
LED_NAMES = ["On", "Off(Temp)", "Off"]

_prog = os.path.basename(sys.argv[0])
USAGE = f"""\
Usage:
  {_prog}                      Print all current settings
  {_prog} get <option>         Print one setting (clean output)
  {_prog} set <option> <value> Set one setting

Options:
  vol     0-100
  filter  0  Fast Roll-off Low Latency
          1  Fast Roll-off Phase Compensated
          2  Slow Roll-off Low Latency
          3  Slow Roll-off Phase Compensated
  gain    0  Low
          1  High
  led     0  On
          1  Off(Temp)
          2  Off
"""


def die(msg):
    raise SystemExit(f"Error: {msg}\n\n{USAGE.strip()}")


dev = usb.core.find(idVendor=DAWN_PRO_VID, idProduct=DAWN_PRO_PID)
if dev is None:
    raise SystemExit("Moondrop Dawn Pro not found. Is it plugged in?")


def query(cmd):
    payload = bytes([0xC0, 0xA5, cmd, 0, 0, 0, 0])
    dev.ctrl_transfer(0x43, 0xA0, 0, 0x09A0, payload)
    time.sleep(0.1)
    return dev.ctrl_transfer(0xC3, 0xA1, 0, 0x09A0, 7)


def send(cmd, value):
    payload = bytes([0xC0, 0xA5, cmd, value, 0, 0, 0])
    dev.ctrl_transfer(0x43, 0xA0, 0, 0x09A0, payload)


def get_vol():
    r = query(0xA2)
    atten = r[4]
    return 0 if atten == 0xFF else 100 - atten


def get_settings():
    r = query(0xA3)
    return r[3], r[4], r[5]


def label(names, index):
    return names[index] if index < len(names) else f"Unknown ({index})"


args = sys.argv[1:]

if not args:
    vol = get_vol()
    filter_i, gain_i, led_i = get_settings()
    print(f"Volume: {vol}%")
    print(f"Filter: {label(FILTER_NAMES, filter_i)}")
    print(f"Gain:   {label(GAIN_NAMES, gain_i)}")
    print(f"LED:    {label(LED_NAMES, led_i)}")

elif args[0] == "get":
    if len(args) != 2:
        die("'get' requires exactly one option name")
    opt = args[1]
    if opt == "vol":
        print(get_vol())
    elif opt == "filter":
        filter_i, _, _ = get_settings()
        print(label(FILTER_NAMES, filter_i))
    elif opt == "gain":
        _, gain_i, _ = get_settings()
        print(label(GAIN_NAMES, gain_i))
    elif opt == "led":
        _, _, led_i = get_settings()
        print(label(LED_NAMES, led_i))
    else:
        die(f"Unknown option '{opt}'")

elif args[0] == "set":
    if len(args) != 3:
        die("'set' requires an option name and a value")
    opt, raw = args[1], args[2]
    try:
        value = int(raw)
    except ValueError:
        die(f"Value must be an integer, got '{raw}'")
    if opt == "vol":
        if not 0 <= value <= 100:
            die("Volume must be 0-100")
        atten = 0xFF if value == 0 else 100 - value
        send(0x04, atten)
    elif opt == "filter":
        if not 0 <= value <= 3:
            die("Filter must be 0-3")
        send(0x01, value)
    elif opt == "gain":
        if not 0 <= value <= 1:
            die("Gain must be 0-1")
        send(0x02, value)
    elif opt == "led":
        if not 0 <= value <= 2:
            die("LED must be 0-2")
        send(0x06, value)
    else:
        die(f"Unknown option '{opt}'")

else:
    die(f"Unknown command '{args[0]}'")
