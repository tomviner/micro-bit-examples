import time

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def proj(src_scale, dest_scale, x):
    a, b = src_scale
    prop = 1.0 * (x - a) / (b - a)
    a, b = dest_scale
    return prop * (b - a) + a
res = proj((-100, 100), (10, 20), 80)
assert round(res) == 19, res

display = {}
def set(x, y, v):
    display[(x, y)] = int(v)

def show():
    for row in range(5):
        for col in range(5):
            print display.get((col, row), '.'),
        print
    print
    display.clear()

def light(b, when=lambda x, y: True):
    b = clamp(0, round(b), 9)
    for col in range(5):
        for row in range(5):
            if when(col, row):
                set(col, row, b)

for u in 1, -1:
    print '---'
    for n in range(-1024, 1025, 900):
        m = proj((-1024, 1024), (-5, 5), n)
        def when(x, y):
            if u == -1:
                # x = 4 - x
                y = 4 - y
            return (-y+2) <= m * (x-2)

        light(9, when)
        show()
        time.sleep(0)
