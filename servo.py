import microbit

DUTY_0PC = 0
DUTY_100PC = 1024

def rescale(src_scale, dest_scale, x):
    """Map one number scale to another

    For example, to convert a score of 4 stars out of 5 into a percentage:
    >>> rescale((0, 5), (0, 100), 4)
    80.0

    Great for mapping different input values into LED pixel brightnesses!
    """
    src_start, src_end = src_scale
    # what proportion along src_scale x is:
    proportion = 1.0 * (x - src_start) / (src_end - src_start)

    dest_start, dest_end = dest_scale
    # apply our proportion to the dest_scale
    return proportion * (dest_end - dest_start) + dest_start


PERIOD = 20000  # microseconds
microbit.pin0.set_analog_period_microseconds(PERIOD)
def pulse_burst(pulse_width, on, off):
    rescale((0, PERIOD), (DUTY_0PC, DUTY_100PC), pulse_width)
    pulse_value = int(pulse_width / PERIOD)
    print(pulse_width, pulse_width)
    try:
        microbit.pin0.write_analog(pulse_width)
        microbit.sleep(on)
    finally:
        microbit.pin0.write_analog(0)
    microbit.sleep(off)

on = 90
off = 0
mn = 700  # 35/2024
mx = 2000  # 102/2024
step = 50

def r():
    yield from range(mn, mx, step)
    yield from range(mx, mn, -step)

while 1:
    [pulse_burst(i, on, off) for i in r()]
