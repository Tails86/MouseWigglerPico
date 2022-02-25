# MouseWigglerPico
Mouse wiggler using the Raspberry Pi Pico microcontroller

# Installation

## CircuitPython

This project depends on CircuitPython. Load CircuitPython downloaded at the following link onto your Pico.
https://circuitpython.org/board/raspberry_pi_pico/
I tested using version 7.1.1.

## Loading MouseWigglerPico

Once CircuitPython is loaded, a CIRCUITPYTHON drive should show up on your system. Just drag and drop all .py files
from this project onto that drive.

# Hardware

This software depends on one push button installed to GP2. When pressed, this button should pull the input to ground.

## Using the BOOTSEL Button as the Input

It is possible to setup the BOOTSEL button to use as the activation button. Solder a 1K-ohm resistor from the upper
left button pin to pin 4 of the pico.
WARNING: YOU DO THIS AT YOUR OWN RISK! I don't immediately see any issue with doing this, but I could be wrong!
![button](button.jpg?raw=true)

# Operation

## Bootup

The boot process starts with the LED flashing 7 times over 2.5 seconds. If you press and hold the button for 1 second
after the first flash, the debug serial and drive will connect for debug operation. Otherwise, those interfaces will be
disabled after boot is complete.

## Runtime

Auto wiggle is initially disabled. Single clicking the button will send 1 mouse wiggle to the host. The wiggle is 1 dot
to the right then 1 dot back. Most systems will not even move the cursor, but this is enough to wake the system.

Holding the button down for 1 second will cause the device to enter automatic wiggle mode where a wiggle will be
automatically sent every 1 second. Press the button again to disable. The automatic wiggle setting is saved such that
if automatic wiggling is activated on power down, it will be active at next power up.