import random
from four_buttons import four_buttons


class Button:
    def is_pressed(self):
        return random.choice((False, True))

class Pin:
    def read_analog(self):
        return random.randint(0, 1024)

class Pixel:
    def __init__(self, mb):
        self.mb = mb

    def set_pixel(self, x, y, brightness):
        self.mb.screen[(x, y)] = brightness
        self.mb.show()

class FakeMicrobit:
    screen = {}

    @property
    def button(self):
        return Button()
    button_a = button_b = button

    @property
    def pin(self):
        return Pin()
    pin0 = pin1 = pin2 = pin

    @property
    def display(self):
        return Pixel(self)

    def show(self):
        for row in range(5):
            for col in range(5):
                print(self.screen.get((col, row), '-'), end='')
            print()
        print()


def test_four_buttons(mocker):
    mocker.patch('four_buttons.microbit', new=FakeMicrobit())
    four_buttons()
