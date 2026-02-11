from machine import Pin, PWM
import utime
import sys
import select
from pid import PID


import sys

# ... (your other setup code)

while True:
    # Check if there is data waiting in the "Serial" buffer
    line = sys.stdin.readline().strip()
    if line:
        # This is the line to add!
        print("Pico received data:", line) 
        
        # Then your code converts it to a number
        try:
            target = float(line)
            # update your PID here...
        except:
            print("Error: Could not understand the data")

# IBT-2 Wiring
rpwm = PWM(Pin(14), freq=1000)
lpwm = PWM(Pin(15), freq=1000)
en_pin = Pin(16, Pin.OUT, value=1) 

# Encoder setup
encoder_count = 0
def handle_encoder(pin):
    global encoder_count
    encoder_count += 1 
Pin(10, Pin.IN, Pin.PULL_UP).irq(trigger=Pin.IRQ_RISING, handler=handle_encoder)

motor_pid = PID(0.05, 0.0, 0.01) 
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

while True:
    # Check if Flask sent new data
    if poll.poll(0):
        line = sys.stdin.readline().strip()
        try:
            import json
            data = json.loads(line)
            if "pid" in data and data["pid"]:
                motor_pid.p_value = data["pid"]["p"]
                motor_pid.i_value = data["pid"]["i"]
                motor_pid.d_value = data["pid"]["d"]
            if "dist_ft" in data:
                # Assuming 1000 ticks per foot for now
                motor_pid.set_set_point(data["dist_ft"] * 1000)
        except:
            pass

    power = motor_pid.update_pid(encoder_count)
    duty = int(abs(power) * 65535)
    
    if power > 0:
        lpwm.duty_u16(0); rpwm.duty_u16(duty)
    elif power < 0:
        rpwm.duty_u16(0); lpwm.duty_u16(duty)
    else:
        lpwm.duty_u16(0); rpwm.duty_u16(0)

    # Send status back to Flask
    print(f"TRG:{motor_pid.set_point}|CUR:{encoder_count}|PWR:{power:.2f}")
    utime.sleep(0.05)


    
    