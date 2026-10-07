# The Mandelbrot set, drawn with characters.
def escape_time(c_re, c_im, limit=40):
    z_re = z_im = 0.0
    for step in range(limit):
        if z_re * z_re + z_im * z_im > 4.0:
            return step
        z_re, z_im = z_re * z_re - z_im * z_im + c_re, 2 * z_re * z_im + c_im
    return limit

shades = " .:-=+*#%@"
for row in range(24):
    y = (row - 12) / 10
    line = ""
    for col in range(72):
        x = (col - 50) / 24
        steps = escape_time(x, y)
        line += shades[min(steps * len(shades) // 41, len(shades) - 1)]
    print(line)
