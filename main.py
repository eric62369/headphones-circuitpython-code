import adafruit_dotstar as dotstar
import neopixel
import board
import time
from digitalio import DigitalInOut, Direction, Pull

dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

led_pin = board.D1  # Which pin your pixels are connected to
num_leds = 10  # How many LEDs you have
strip = neopixel.NeoPixel(led_pin, num_leds, brightness=1, auto_write=False)
b1 = DigitalInOut(board.D2)
b1.direction = Direction.INPUT
b1.pull = Pull.UP
b2 = DigitalInOut(board.D0)
b2.direction = Direction.INPUT
b2.pull = Pull.UP

SOFTCYAN = (0, 85, 85)
SOFTYELLOW = (85, 76, 0)
WHEEL = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 230, 0)
RED = (255, 10, 30)
BLUE = (30, 10, 255)
GREEN = (30, 255, 10)

COLORS = [SOFTCYAN, SOFTYELLOW, WHEEL, WHITE, CYAN, YELLOW, RED, BLUE, GREEN]

######################### HELPERS ##############################
# Helper to give us a nice color swirl
def wheel(pos):
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

def pulse(pos, color):
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    mod = 0.5
    if (pos < 128):
        mod = pos / 127
    else:
        pos -= 128
        mod = (127 - pos) / 127
    return [int(mod * color[0]), int(mod * color[1]), int(mod * color[2])]

def wave(pos, color):
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    leadIndex = 0 
    if (pos < 128):
        leadIndex = int(pos/2) % num_leds
    else:
        pos -= 128
        leadIndex = (127 - int(pos/2)) % num_leds

    emptyState = []
    for i in range(num_leds):
        emptyState.append([0, 0, 0])
    emptyState[leadIndex] = color
    preLeadIndex2 = (leadIndex + 2) % num_leds
    preLeadIndex1 = (leadIndex + 1) % num_leds
    followIndex1 = (leadIndex - 1) % num_leds
    followIndex2 = (leadIndex - 2) % num_leds
    brt1 = 0.4
    brt2 = 0.1
    emptyState[preLeadIndex2] = [int(brt2 * color[0]), int(brt2 * color[1]), int(brt2 * color[2])]
    emptyState[preLeadIndex1] = [int(brt1 * color[0]), int(brt1 * color[1]), int(brt1 * color[2])]
    emptyState[followIndex1] = [int(brt1 * color[0]), int(brt1 * color[1]), int(brt1 * color[2])]
    emptyState[followIndex2] = [int(brt2 * color[0]), int(brt2 * color[1]), int(brt2 * color[2])]

    return emptyState

def pixelsFill(pixelColors):
    for i in range(len(pixelColors)):
        strip[i] = pixelColors[i]
    strip.show()

def fullFill(color):
    for i in range(num_leds):
        strip[i] = color
    strip.show()
######################### MAIN LOOP ##############################
i = 225
wheelPos = 225
colorIndex = 0
num_color = len(COLORS)
patternIndex = 0
num_pattern = 3
b1Held = False
b1Press = False
b2Held = False
b2Press = False
while True:
    # spin internal LED around!
    dot[0] = wheel(wheelPos)
    dot.show()

    targetColor = COLORS[colorIndex]
    if (targetColor == WHEEL):
        targetColor = wheel(wheelPos)
    if (patternIndex == 0):
        fullFill(pulse(wheelPos, targetColor))
    elif (patternIndex == 1):
        pixelsFill(wave(wheelPos, targetColor))
    else:
        fullFill(targetColor)
    

    curB1 = not b1.value
    if (curB1 is True):
        if (curB1 is not b1Held):
            b1Press = True
            b1Held = True
    else:
        b1Held = False
    if (b1Press is True and b1Held is True):
        b1Press = False
        colorIndex += 1
        colorIndex = colorIndex % num_color

    curB2 = not b2.value
    if (curB2 is True):
        if (curB2 is not b2Held):
            b2Press = True
            b2Held = True
    else:
        b2Held = False
    if (b2Press is True and b2Held is True):
        b2Press = False
        patternIndex += 1
        patternIndex = patternIndex % num_pattern

    wheelPos = int(i) % 256  # run from 0 to 255
    i += 1
    i = i % 256
