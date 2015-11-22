import microbit as mb

set = mb.display.set_pixel
get = mb.display.get_pixel

def light_column(col):
    for row in range(5):
        set(col, row, 9)

def fade_display():
    for col in range(5):
        for row in range(5):
            n = get(col, row)
            n = max(0, n - 1)
            set(col, row, n)


def pin_is_touched(n, cache={}):
    # use a cache to avoid MemoryError
    pin = cache.get(n) or getattr(mb, 'pin{}'.format(n))
    return pin.read_analog() > 300

while True:
    if mb.button_a.is_pressed():
        light_column(0)
    if mb.button_b.is_pressed():
        light_column(4)
    if pin_is_touched(1):
        light_column(1)
    if pin_is_touched(2):
        light_column(3)
    mb.sleep(10)
    fade_display()
