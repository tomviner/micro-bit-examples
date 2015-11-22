import microbit as mb

set = mb.display.set_pixel
get = mb.display.get_pixel

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def proj(src_scale, dest_scale, x):
    a, b = src_scale
    prop = 1.0 * (x - a) / (b - a)
    a, b = dest_scale
    return prop * (b - a) + a
res = proj((-100, 100), (10, 20), 80)
assert round(res) == 19, res

def light(b, when=lambda x,y: True):
    # print(b, end=' - ')
    b = clamp(0, round(b), 9)
    # print(b)
    for col in range(5):
        for row in range(5):
            if when(col, row):
                set(col, row, b)

def fade_display():
    for col in range(5):
        for row in range(5):
            n = get(col, row)
            n = max(0, n - 1)
            set(col, row, n)

while True:
    X, Y, Z = mb.accelerometer.get_values()
    print(X, Y, Z)
    M = proj((-1024, 1024), (-5, 5), X)
    def when(x, y):
        m = M
        upside_down = Y < 0
        u = -1 if upside_down else 1
        if upside_down:
            y = 4 - y
        # print((-y+2), m * (x-2))
        # print((-y+2), m * (x-2), end=' ')
        return (-y+2) < m * (x-2)
    light(9, when)

    mb.sleep(100)
    fade_display()
