import time
import storage
import usb_midi
import usb_cdc
import usb_hid
import digitalio
import board
import button
import led
import util

# This code will enable USB drive and serial only if one of the following occurs:
# 1. The debug input (GP1) is shorted to ground on power up
# 2. The button (GP2) is pressed and held for 1 second within the first 2.5 seconds after power up
    
def hardware_init(enable_debug_interfaces):
    # Saved settings will be readonly while the device is in debug mode to avoid drive corruption
    storage.remount('/', readonly=enable_debug_interfaces)
    
    # We don't use MIDI in main at all, so just disable that outright
    usb_midi.disable()
    
    # Enable mouse HID device only, set to boot device only if debug is disabled
    # Something goes wrong if boot device for mouse is enabled when debug interfaces are enabled
    boot_device = 0 if enable_debug_interfaces else 2
    usb_hid.enable([usb_hid.Device.MOUSE], boot_device=boot_device)
    
    if not enable_debug_interfaces:
        # The following are enabled by default
        storage.disable_usb_drive()
        usb_cdc.disable()

def main():
    debug_input = digitalio.DigitalInOut(board.GP1)
    debug_input.switch_to_input(pull=digitalio.Pull.UP)

    # 25 ms sleep to ensure we have reached steady state
    time.sleep(0.025)

    enable_debug_interfaces = True

    # Only do the following checks if the debug input is not shorted to ground
    if debug_input.value:
        # While button is not pressed, do some flashing
        count = 0
        def check():
            nonlocal count
            if count % 15 == 0:
                led.set(on=True)
            else:
                led.set(on=False)
            count += 1
            return button.is_pressed()
        util.wait_for_event(fn=check, timeout_seconds=2.5, check_period=0.025)
        led.set(on=False)
        time.sleep(0.025)
            
        # Enable debug if button is pressed and stays pressed for 1 second
        enable_debug_interfaces = button.is_pressed() and not button.wait_for(wait_for_pressed=False, timeout_seconds=1.0)

        if enable_debug_interfaces:
            # Button was pressed and held; show confirmation
            led.blink([0.025, 0.125, 0.025])
            
    hardware_init(enable_debug_interfaces)
        
if __name__ == "__main__":
    main()
