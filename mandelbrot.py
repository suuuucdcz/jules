import sys

def mandelbrot():
    width = 80
    height = 40
    max_iter = 100

    # Characters ordered by density
    chars = " .:-=+*#%@"

    # Real bounds (x-axis)
    xmin, xmax = -2.5, 1.0
    # Imaginary bounds (y-axis)
    ymin, ymax = -1.5, 1.5

    for y in range(height):
        im = ymin + (ymax - ymin) * y / (height - 1)
        line = ""
        for x in range(width):
            re = xmin + (xmax - xmin) * x / (width - 1)
            c = complex(re, im)
            z = 0.0j
            for i in range(max_iter):
                if abs(z) > 2.0:
                    break
                z = z * z + c

            if i == max_iter - 1:
                line += chars[-1]
            else:
                line += chars[i % (len(chars) - 1)]
        print(line)

if __name__ == "__main__":
    mandelbrot()
