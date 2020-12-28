import platform

if platform.platform().lower.find("armv71") > -1:
    import RPi.GPIO as GPIO
else:
    from . import mock as GPIO