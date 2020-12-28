import os

if os.uname().machine.startswith("arm"):
    import RPi.GPIO as GPIO
else:
    from . import mock as GPIO