from sense_hat import SenseHat
import time

s = SenseHat()

red = (255, 0, 0)
green = (0, 255, 0)
nothing = (0, 0, 0)
print(s.get_compass())


def raspi_logo():
    G = green
    R = red
    O = nothing
    logo = [
        O, G, G, O, O, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, R, R, R, R, O, O,
        O, R, R, R, R, R, R, O,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        O, R, R, R, R, R, R, O,
        O, O, R, R, R, R, O, O,
    ]
    return logo


def heart():
    P = ((255 - 4 * int(s.get_temperature())) % 255, 0, 10)
    if (s.get_temperature() < 0):
        P = (0, 0, (255 - 4 * abs(int(s.get_temperature()))) % 255)
    O = nothing
    logo = [
        O, O, O, O, O, O, O, O,
        O, P, P, O, P, P, O, O,
        P, P, P, P, P, P, P, O,
        P, P, P, P, P, P, P, O,
        O, P, P, P, P, P, O, O,
        O, O, P, P, P, O, O, O,
        O, O, O, P, O, O, O, O,
        O, O, O, O, O, O, O, O,
    ]
    return logo


images = [raspi_logo, heart]
count = 0

while True:
    index = count % len(images)
    s.set_pixels(images[index]())
    time.sleep(1)
    if (images[index] == raspi_logo):
        s.show_message(
            "WAT",
            text_colour=[int(s.get_compass()) % 255, int(s.get_pressure()) % 255, int(s.get_humidity()) % 255],
            scroll_speed=0.15
        )

    count += 1
