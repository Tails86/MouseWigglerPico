import digitalio
import board
import time
import microcontroller
import util

class Button:
    def __init__(self, gp: microcontroller.Pin, is_active_low: bool) -> None:
        """
        Button init
        Inputs - gp : Pin where button is located
                 is_active_low : True if input is low when pressed; False if input is high when pressed
        """
        self.button = digitalio.DigitalInOut(gp)
        if is_active_low:
            pull = digitalio.Pull.UP
        else:
            pull = digitalio.Pull.DOWN
        self.button.switch_to_input(pull=pull)
        self.is_active_low = is_active_low
        
    def is_pressed(self) -> bool:
        """
        Returns True if button is pressed or False if button is not pressed
        """
        return (self.button.value != self.is_active_low)
    
    def wait_for(self, wait_for_pressed, timeout_seconds=-1) -> None:
        """
        Blocks until button is or is no longer pressed
        Inputs - wait_for_pressed : True to wait until pressed or False to wait until released
                 timeout_seconds : Timeout in seconds or -1 for infinite
        Returns True iff the button was released before timeout
        """
        # Wait for 2 consecutive senses
        count = 0
        def is_released():
            nonlocal count
            nonlocal self
            if self.is_pressed() != wait_for_pressed:
                count = 0
            else:
                count += 1
            return (count >= 2)
        return util.wait_for_event(is_released, timeout_seconds, 0.025)
    
# The one and only button
my_button = Button(gp=board.GP2, is_active_low=True)

def is_pressed():
    return my_button.is_pressed()

def wait_for(wait_for_pressed, timeout_seconds=-1):
    return my_button.wait_for(wait_for_pressed, timeout_seconds)
