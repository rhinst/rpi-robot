BOARD = 1
OUT = 1
IN = 1
LOW = 0
HIGH = 1


def setmode(a):
    print(a)


def setup(a, b):
    print(a)


def output(a, b):
    print(a)


def cleanup():
    print("a")


def setwarnings(flag):
    print("False")


class PWM:

    def __init__(self, pin: int, frequency: int):
        pass

    def start(self, duty_cycle: float):
        pass

    def stop(self):
        pass