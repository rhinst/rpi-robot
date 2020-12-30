from unittest.mock import Mock, patch

from app.subsystem.motor.driver import Driver, MotorPins, MotorState, MotorDirection


def test_initialize():
    m_message_bus = Mock()
    m_gpio = Mock()
    m_gpio.BOARD = 123
    m_gpio.OUT = 2
    pins = MotorPins(
        front_left_dir=1,
        front_left_speed=2,
        front_right_dir=3,
        front_right_speed=4,
        rear_left_dir=5,
        rear_left_speed=6,
        rear_right_dir=7,
        rear_right_speed=8,
    )
    driver = Driver(m_message_bus, pins)
    with patch("app.subsystem.motor.driver.GPIO", m_gpio):
        driver.initialize()
    m_gpio.setmode.assert_called_once_with(m_gpio.BOARD)
    m_gpio.setup.assert_called_once_with([pin for pin in range(1, 9)], m_gpio.OUT)
    m_gpio.PWM.assert_called()


def test_drive():
    m_message_bus = Mock()
    pins = MotorPins(
        front_left_dir=1,
        front_left_speed=2,
        front_right_dir=3,
        front_right_speed=4,
        rear_left_dir=5,
        rear_left_speed=6,
        rear_right_dir=7,
        rear_right_speed=8,
    )
    driver = Driver(m_message_bus, pins)
    fl_state = MotorState(speed=0.5, direction=MotorDirection.FORWARD)
    fr_state = MotorState(speed=0.4, direction=MotorDirection.BACKWARD)
    rl_state = MotorState(speed=0.3, direction=MotorDirection.BACKWARD)
    rr_state = MotorState(speed=0.2, direction=MotorDirection.FORWARD)
    m_gpio = Mock()
    m_gpio.HIGH = 1
    m_gpio.LOW = 0
    m_gpio.PWM.side_effect = [Mock(), Mock(), Mock(), Mock()]
    with patch("app.subsystem.motor.driver.GPIO", m_gpio):
        driver.initialize()
        driver.drive(fl_state, fr_state, rl_state, rr_state)
    driver.fl_pwm.start.assert_called_once_with(50)
    driver.fr_pwm.start.assert_called_once_with(40)
    driver.rl_pwm.start.assert_called_once_with(30)
    driver.rr_pwm.start.assert_called_once_with(20)
    m_gpio.output.assert_any_call(1, m_gpio.HIGH)
    m_gpio.output.assert_any_call(3, m_gpio.LOW)
    m_gpio.output.assert_any_call(5, m_gpio.LOW)
    m_gpio.output.assert_any_call(7, m_gpio.HIGH)


def test_stop():
    m_message_bus = Mock()
    pins = MotorPins(
        front_left_dir=1,
        front_left_speed=2,
        front_right_dir=3,
        front_right_speed=4,
        rear_left_dir=5,
        rear_left_speed=6,
        rear_right_dir=7,
        rear_right_speed=8,
    )
    driver = Driver(m_message_bus, pins)
    m_gpio = Mock()
    m_gpio.PWM.side_effect = [Mock(), Mock(), Mock(), Mock()]
    with patch("app.subsystem.motor.driver.GPIO", m_gpio):
        driver.initialize()
        driver.stop()
    driver.fl_pwm.stop.assert_called_once()
    driver.fr_pwm.stop.assert_called_once()
    driver.rl_pwm.stop.assert_called_once()
    driver.rr_pwm.stop.assert_called_once()
