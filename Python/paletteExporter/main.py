
from PIL import Image

SAVE_PATH = 'C:/Users/charl/Documents/Scripts/portfolio/public/Cars/palette.png'

def run(data):

    img = Image.new('RGB', (len(data), 1))
    img.putdata(data)
    img.save(SAVE_PATH)

    return img

run([
    (255, 255, 255),
    (20, 20, 20),
    (128, 128, 128),
    (192, 192, 192),
    (40, 60, 120),
    (180, 30, 30),
    (70, 70, 70),
    (210, 210, 200),
    (0, 90, 140),
    (110, 0, 0),
    (160, 160, 150),
    (30, 80, 40),
    (190, 170, 120),
    (200, 140, 40),
    (255, 140, 0),
]).show()
