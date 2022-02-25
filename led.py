import digitalio
import board
import microcontroller
import time

class Led:
    def __init__(self, gp: microcontroller.Pin, is_active_low: bool) -> None:
        """
        Initialize Led
        Inputs - gp : Pin where LED is located
                 is_active_low : True if LED is on when low; False if LED is on when high
        """
        self.led = digitalio.DigitalInOut(gp)
        self.led.direction = digitalio.Direction.OUTPUT
        self.is_active_low = is_active_low
    
    def set(self, on: bool) -> None:
        """
        Sets the LED on or off
        Inputs - on : True to turn on or False to turn off
        """
        self.led.value = (on != self.is_active_low)
        
    def toggle(self):
        """
        Toggles the LED state
        """
        self.led.value = not self.led.value
        
    def blink(self, periods: list) -> None:
        """
        Blinks the LED based on a set list of periods (blocks until complete)
        Inputs - periods : List of times in seconds [on time, off time, on time, etc.]
        """
        self.set(on=True)
        for x in periods:
            time.sleep(x)
            self.toggle()
        self.set(on=False)
        
# The one and only LED
my_led = Led(gp=board.GP25, is_active_low=False)

def set(on: bool) -> None:
    my_led.set(on)
    
def toggle() -> None:
    my_led.toggle()
    
def blink(periods: list) -> None:
    my_led.blink(periods)