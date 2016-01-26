import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def analyze(image):
    i = Image.open(image)
    width, height = i.size
    pixels = i.load()

    f = []
    U = []

    for x in range(0, width):
        for y in range(0, height):
            red, green, blue, alpha = pixels[x, y]
            if blue > 240 and red < 100:
                f.append(x)
                U.append(-y+height)
                break
    return np.array((f, U))
header = 'arbitrary units \nln(f) U'
np.savetxt('daten/a1_raw.txt', analyze('daten/a1.png').T, header=header)
np.savetxt('daten/a2_raw.txt', analyze('daten/a2.png').T, header=header)

