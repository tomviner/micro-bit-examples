import microbit as mb
import microbit

### define some constants

DISPLAY_WIDTH = 5
DISPLAY_HEIGHT = 5

MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 9

### Some maths functions to help us

def clamp(minimum, n, maximum):
    """Return the nearest value to n, that's within minimum to maximum (incl)
    """
    return max(minimum, min(n, maximum))


### Helpers for controling the display

def light(brightness, filter):
    """Light up all pixels matching the filter function
    """
    brightness = clamp(MIN_BRIGHTNESS, round(brightness), MAX_BRIGHTNESS)
    for col in range(DISPLAY_WIDTH):
        for row in range(DISPLAY_HEIGHT):
            if filter(col, row):
                microbit.display.set_pixel(col, row, brightness)

def light_column(column):
    """Light up a whole column to max brightness
    """
    def filter_column(col, row):
        """For a given pixel position, turn on if it matches our column
        """
        return col == column
    light(MAX_BRIGHTNESS, filter_column)

def light_row(row):
    """Light up a whole row to max brightness
    """
    def filter_row(col, rw):
        """For a given pixel position, turn on if it matches our row
        """
        return rw == row
    light(MAX_BRIGHTNESS, filter_row)

def fade_display():
    """Reduce every pixel by 1 brightness level

    This means as we draw new things, the old ones will fade away
    """
    for col in range(5):
        for row in range(5):
            brightness = microbit.display.get_pixel(col, row)
            # reduce by one, but make sure it's still in 0 to 9
            brightness = clamp(MIN_BRIGHTNESS, brightness - 1, MAX_BRIGHTNESS)
            microbit.display.set_pixel(col, row, brightness)

def pin_is_touched(n, cache={}):
    # use a cache to avoid MemoryError
    # pin = cache.get(n) or getattr(mb, 'pin{}'.format(n))
    pin = getattr(mb, 'pin{}'.format(n))
    return pin.read_analog() > 300

def paint_box(top=0, bottom=DISPLAY_HEIGHT-1, left=0, right=DISPLAY_WIDTH-1):
    def filter_box(col, row):
        """For a given pixel position, turn on if it's with the bounds
        """
        # remember rows count from 0 at the top!
        correct_vertical = top <= row <= bottom
        correct_horizontal = left <= col <= right
        return correct_vertical and correct_horizontal
    light(MAX_BRIGHTNESS, filter_box)

while True:
    a = mb.button_a.is_pressed()
    b = mb.button_b.is_pressed()

    # let's call the two pin-buttons c and d:
    c = pin_is_touched(1)
    d = pin_is_touched(2)

    if a:
        light_row(2)
        paint_box(right=1)
    if b:
        light_row(3)
        paint_box(left=3)
    if c:
        light_column(1)
        paint_box(bottom=1)
    if d:
        light_column(3)
        paint_box(top=3)

    mb.sleep(10)

    # fade all pixels by one brightness level
    fade_display()
