import time
import math

def wait_for_event(fn, timeout_seconds=-1, check_period=0.025):
    """
    Wait for event to occur or timeout.
    Inputs - fn : Function which returns True once event occurs
             timeout_seconds : Timeout in seconds or -1 for infinite
             check_period : How long to wait before lamda_fn is polled again
    Returns True iff the event occurred before timeout
    """
    if timeout_seconds < 0:
        loop_count = 1
        decrement_value = 0
    else:
        loop_count = int(math.ceil(timeout_seconds / check_period))
        decrement_value = 1
    while loop_count > 0 and not fn():
        time.sleep(check_period)
        loop_count -= decrement_value
    return (loop_count > 0)
        