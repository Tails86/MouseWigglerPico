import time
import usb_hid
from adafruit_hid.mouse import Mouse
import board
import digitalio
import button
import led
import json
import os
import util

SETTINGS_DIR = '/settings'
SETTINGS_FILE_PATH = SETTINGS_DIR + '/settings.json'

# Global mouse object
mouse = None

# Global settings (default settings here)
settings = {'wiggling': True}

def mouse_init():
    global mouse
    # We may be stuck in this loop if device is plugged in while host is asleep
    while mouse is None:
        try:
            mouse = Mouse(usb_hid.devices)
        except:
            time.sleep(1.0)
    led.blink([1.0])
        
def mouse_move_safe(x: int = 0, y: int = 0, wheel: int = 0):
    global mouse
    try:
        mouse.move(x=x, y=y, wheel=wheel)
    except:
        # Exceptions will occur if the device disconnects but is still powered
        return False
    else:
        return True

def do_a_wiggle():
    # Moving 1 over and 1 back is enough to wake a PC without moving the cursor
    result = mouse_move_safe(x=1) and mouse_move_safe(x=-1)
    if result:
        # Do a little flash
        led.blink([0.05])
    return result

def read_settings():
    global settings
    try:
        with open(SETTINGS_FILE_PATH, 'r') as f:
            settings = json.load(f)
    except Exception as e:
        print(e)

def write_settings():
    global settings
    try:
        os.mkdir(SETTINGS_DIR)
    except:
        pass
    try:
        with open(SETTINGS_FILE_PATH, 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print(e)
        
def set_wiggling_setting(value):
    settings['wiggling'] = value
    write_settings()
    
def main():
    global mouse
    global settings
    
    mouse_init()
    button.wait_for(wait_for_pressed=False)
    read_settings()

    while True:
        if settings['wiggling']:
            if button.wait_for(wait_for_pressed=True, timeout_seconds=1.0):
                # Button was pressed - cancel automatic wiggle
                set_wiggling_setting(False)
                led.set(on=False)
                # Wait for button to be released before proceeding
                button.wait_for(wait_for_pressed=False)
            else:
                if not do_a_wiggle():
                    # USB likely disconnected - wait for reconnect before continuing.
                    # The only way I can find to determine if we are reconnected is
                    # to keep trying to contol the mouse until it works!
                    util.wait_for_event(lambda: mouse_move_safe(x=1))
        else:
            # Wait indefinitely until button is pressed
            button.wait_for(wait_for_pressed=True)
            # Single wiggle
            if not do_a_wiggle():
                # USB likely disconnected - wait for button release and loop again
                button.wait_for(wait_for_pressed=False)
            # If button is held for at least 1 second, turn on automatic wiggle
            elif not button.wait_for(wait_for_pressed=False, timeout_seconds=1.0):
                set_wiggling_setting(True)
                # Turn on LED and wait until button is released before proceeding
                led.set(on=True)
                button.wait_for(wait_for_pressed=False)
                time.sleep(0.5)
                led.set(on=False)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        led.blink[0.5, 0.5, 0.5, 0.5, 3.0]
        raise e
        
