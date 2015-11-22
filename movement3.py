import microbit

# Some maths function to help us

def clamp(minimum, n, maximum):
    """Return the near value to n, that's in (minimum, maximum)
    """
    return max(minimum, min(n, maximum))

def rescale(src_scale, dest_scale, x):
    """Map one number scale to another

    For example, to convert a score 4 starts out of 5 into a percentage:
    >>> rescale((0, 5), (0, 100), 4)
    80.0

    Great for mapping different input values into LED pixel brightnesses!
    """
    a, b = src_scale
    proportion = 1.0 * (x - a) / (b - a)
    c, d = dest_scale
    return proportion * (d - c) + c

# Helpers for controling the display

def light(brightness, filter):
    """Light up all pixels matching the filter function
    """
    brightness = clamp(0, round(brightness), 9)
    for col in range(5):
        for row in range(5):
            if filter(col, row):
                microbit.display.set_pixel(col, row, brightness)

def fade_display():
    """Reduce every pixel by 1 brightness level

    This means as we draw new things, the old ones will fade away
    """
    for col in range(5):
        for row in range(5):
            brightness = microbit.display.get_pixel(col, row)
            # reduce by one, but make sure it's still in 0 to 9
            brightness = clamp(0, brightness - 1, 9)
            microbit.display.set_pixel(col, row, brightness)


def paint_water():
    """Use the accelerometer to paint a water level on the display
    """
    # read the current orientation values from the accelerometer
    X, Y, Z = microbit.accelerometer.get_values()

    # map the force in the X-axis to a turn factor from -2 to 2
    # -1024 is button A at the top, 1024 is button B at the top
    turn_factor = rescale((-1024, 1024), (-2, 2), X)

    # map the force in the Z-axis to a spill factor from -3 to 3
    # this allows the water to cover the whole display when it's flat
    spill_factor = rescale((1024, -1024), (-3, 3), Z)

    # use the variables above to make a filter function, customised for the
    # current orientation of the micro:bit
    def filter(col, row):
        """For a given pixel position, decide if it should be on or not
        """
        if Y < 0:
            # we're upside down, so reverse the y-axis value
            row = 4 - row
        # remember rows count down from the top, so we want to light up all
        # the rows below the water line (when the micro:bit is help up stright)
        # The forumula here is of the form y = m*x + c
        # We have a couple of "- 2"s to centre the water level in the middle
        return row - 2 > -turn_factor * (col - 2) - spill_factor

    # we want the water to "dilute" when spread out across the whole display
    overall_brightness = rescale((0, 1024), (9, 4), abs(Z))

    # light up the pixels when filter returns true, to the given bright level
    light(overall_brightness, filter)


while True:
    paint_water()

    microbit.sleep(100)

    # fade all pixels by one brightness level
    fade_display()