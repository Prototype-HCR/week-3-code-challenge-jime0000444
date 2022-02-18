# Write your code here :-)
import time
import neopixel
import board
import digitalio
from rainbowio import colorwheel

# make a neopixel object for 10 pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1, auto_write=False)

# declare some inputs for button a and b
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# declare some color constants
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
RAINBOW = None

colors = [OFF, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]


# declare a function to do a rainbow animation
def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)

# declare a function to cycle the rainbow
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        #time.sleep(wait)


button_a_pre = button_A.value
button_b_pre = button_B.value
press_count = 1
press_time = time.monotonic()
hold_mode = False
brightness_val = 0.5
brightness_inc = 0
pixel_mode = False
counter = 0
while True:
    # gather input values
    button_a_read = button_A.value
    button_b_read = button_B.value
    # print out the current and previous values
    print("ButtonA Read is:", button_a_read)
    print("ButtonA Prev is:", button_a_pre, '\n')
    print("ButtonB Read is:", button_b_read)
    print("ButtonB Prev is:", button_b_pre, '\n')

    # check for change in the button state
    if button_a_read != button_a_pre:
        if button_a_read ==  True:
        # the button has changed...
            counter+=1
            # the button has changed from False to True
            press_time = time.monotonic()
            if counter % 2 == 1:
                pixel_mode = True
                print(counter, 'is open')
            else:
                pixel_mode = False
                print(counter,'is off')
            #time.sleep(1)
    elif button_b_read != button_b_pre:
        if pixel_mode == True:
            if button_b_read:
                 press_count += 1
                 if press_count > 7:
                    press_count = 0
                    print(press_count)

    #     else:
    #         pixels.fill(0)
    # do ouput
    if pixel_mode:
        if hold_mode:
            brightness_val += brightness_inc
            if brightness_val <= 0:
                brightness_val = 0.5
            elif brightness_val >= 1.0:
                brightness_val = 1.0
            pixels.brightness = brightness_val
        else:
            pixels.fill(colors[press_count])
    else:
       pixels.fill(OFF)
    pixels.show()
    # save the button_a_read value for next time
    button_a_pre = button_a_read
    button_b_pre = button_b_read
    time.sleep(0.1)
