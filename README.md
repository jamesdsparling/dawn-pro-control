# Dawn Pro Control

Read and control settings on a Moondrop Dawn Pro via USB.

```
Usage:
  dawn_pro_control.py                      Print all current settings
  dawn_pro_control.py get <option>         Print one setting (clean output)
  dawn_pro_control.py set <option> <value> Set one setting

Options:
  vol     0-100
  filter  0  Fast Roll-off Low Latency
          1  Fast Roll-off Phase Compensated
          2  Slow Roll-off Low Latency
          3  Slow Roll-off Phase Compensated
  gain    0  Low
          1  Middle
          2  High
  led     0  On
          1  Off(Temp)
          2  Off
```
