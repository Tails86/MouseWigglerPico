# MouseWigglerPico
Mouse wiggler using the Raspberry Pi Pico microcontroller

# Installation

## CircuitPython

This project depends on CircuitPython. Load CircuitPython downloaded at the following link onto your Pico.
https://circuitpython.org/board/raspberry_pi_pico/

I tested this using version 7.1.1.

# Installing Dependencies using Thonny

Install Thonny from: https://thonny.org/

With CircuitPython installed on the Pico and the Pico connected, launch thonny. Press the stop button near the top. Go
to `Tools->Manage Packages...`. In the search bar, type in `adafruit_hid` and click search. Then select adafruit_hid
from the list and click Install.

## Loading MouseWigglerPico

Once CircuitPython is loaded, a CIRCUITPY drive should show up on your system. Just drag and drop all files from
the src directory of this project onto that drive. The drive should look like the following.
![button](CIRCUITPYTHON_drive.jpg?raw=true)

# Hardware

This software depends on one push button installed to GP2. When pressed, this button should pull the input to ground.

## Using the BOOTSEL Button as the Input

It is possible to setup the BOOTSEL button to use as the activation button. Solder a 1K-ohm resistor from the upper
left button pin to pin 4 of the pico.

WARNING: YOU DO THIS AT YOUR OWN RISK! I don't immediately see any issue with doing this, but I could be wrong!
![button](button.jpg?raw=true)

## Case

If you have a 3D printer, I recommend the button variant of this case: https://www.thingiverse.com/thing:4924948

Printing with transparent or translucent filament allows the LED to shine through.

# Operation

## Bootup

The boot process starts with the LED flashing 7 times over 2.5 seconds. If you press and hold the button for 1 second
after the first flash, the debug serial and drive will connect for debug operation. Two quick flashes from the LED 
confirms this operation. Otherwise, those interfaces will be disabled after boot is complete.

As a fallback, debug mode may also be activated if GP1 is shorted to ground on power up.

The settings storage is set as read only while in debug mode in order to avoid data corruption. This means that
settings won't persist from power down to power up.

## Runtime

A mouse wiggle is 1 dot to the right then 1 dot back. Most systems will not even move the cursor, but this is enough to
wake the system.

Auto wiggle mode is initially enabled. In this mode, a wiggle will be automatically sent every 1 second. The LED with
flash every time a wiggle is sent to the host. Press the button to disable this mode.

When auto wiggle mode is disabled, single clicking the button will send 1 mouse wiggle to the host. The LED flashes
every time a mouse wiggle is sent to the host. Holding the button down for 1 second will cause the device to enter
automatic wiggle mode. The LED turns on to confirm this and will remain on until the button is released. 

The automatic wiggle setting is saved such that whatever mode is set on power down will be reloaded at next power up.

Runtime operation is halted if USB data lines are disconnected from the host until USB is reconnected.
