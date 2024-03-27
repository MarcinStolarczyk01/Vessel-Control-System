from gpiozero import Motor
import logging

class VesselMotor():
    _motor: Motor
    _motor_velocity: float

    def __init__(self, gpio_forward: str, gpio_backward: str):
        self._motor = Motor(gpio_forward, gpio_backward, pwm=True)
        
    def set_velocity(self, velocity: float):
        if not -1 < velocity < 1:
            logging.debug(f"Speed value has to be between -1 and 1 but given value is {velocity}. Setting max speed instead.")
        
        direction, speed = self._calculate_speed_and_direction(velocity)
        if direction == 'forward':
            self._motor.forward(speed)
        elif direction == 'backward':
            self._motor.backward(speed)

    def stop(self):
        self._motor.stop()
        self._motor_velocity = 0
        
    def _calculate_speed_and_direction(self, velocity: float) -> tuple[str, float]:
        direction: str
        speed: float
        
        if velocity > 1:
            velocity = 1
        elif velocity < -1:
            velocity = -1
        
        if velocity >= 0:
            direction = 'forward'
        elif velocity < 0:
            direction = 'backward'
        
        self._motor_velocity = velocity
        speed = abs(velocity)
        
        return (direction, speed)
    
    def get_motor_velocity(self) -> float:
        return self._motor_velocity