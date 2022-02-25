# MouseWigglerPico
Mouse wiggler using the Raspberry Pi Pico microcontroller

# Installation

## CircuitPython

This project depends on CircuitPython. Load CircuitPython downloaded at the following link onto your Pico.
https://circuitpython.org/board/raspberry_pi_pico/

I tested this using version 7.1.1.

## Loading MouseWigglerPico

Once CircuitPython is loaded, a CIRCUITPYTHON drive should show up on your system. Just drag and drop all files from
the src directory of this project onto that drive.

# Hardware

This software depends on one push button installed to GP2. When pressed, this button should pull the input to ground.

## Using the BOOTSEL Button as the Input

It is possible to setup the BOOTSEL button to use as the activation button. Solder a 1K-ohm resistor from the upper
left button pin to pin 4 of the pico.

WARNING: YOU DO THIS AT YOUR OWN RISK! I don't immediately see any issue with doing this, but I could be wrong!
![button](button.jpg?raw=true)

## Case

If you have a 3D printer, I recommend the button variant of this case: https://www.thingiverse.com/thing:4924948

# Operation

## Bootup

The boot process starts with the LED flashing 7 times over 2.5 seconds. If you press and hold the button for 1 second
after the first flash, the debug serial and drive will connect for debug operation. Two quick flashes from the LED 
confirms this operation. Otherwise, those interfaces will be disabled after boot is complete.

Note that the drive will come up as read only (see note in boot.py). A tool like Thonny may then be used to edit the
code.

## Runtime

Auto wiggle is initially disabled. Single clicking the button will send 1 mouse wiggle to the host. The wiggle is 1 dot
to the right then 1 dot back. Most systems will not even move the cursor, but this is enough to wake the system. The
LED flashes every time a mouse wiggle is sent to the host.

Holding the button down for 1 second will cause the device to enter automatic wiggle mode where a wiggle will be
automatically sent every 1 second. The LED turns on to confirm this and will remain on until the button is released.
The LED with then flash every time a wiggle is sent to the host. Press the button again to disable. The automatic
wiggle setting is saved such that if automatic wiggling is activated on power down, it will be active at next power up.

Runtime operation is halted if USB data lines are disconnected from the host until USB is reconnected.
