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

def light(b, skip_col=None):
    print(b, end=' - ')
    b = clamp(0, round(b), 9)
    print(b)
    for col in range(5):
        col_b = 0 if col==skip_col else b
        for row in range(5):
            set(col, row, col_b)

def fade_display():
    for col in range(5):
        for row in range(5):
            n = get(col, row)
            n = max(0, n - 1)
            set(col, row, n)


while True:

    vs = mb.accelerometer.get_values()
    print('a', vs)
    if not vs:
        continue
    vs = [abs(v) for v in vs]
    idx = {v:i for (i, v) in enumerate(vs)}
    print('b', vs)
    max_v = max(vs)
    max_idx = idx[max_v]
    total = sum(vs)
    print(total)

    n = proj((0, 1024*3), (0, 9), total - 1024)
    # print('mn', m, n)
    light(n, skip_col=max_idx)

    mb.sleep(100)
    fade_display()
