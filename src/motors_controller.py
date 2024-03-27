from vessel_motor import VesselMotor
import warnings

class MotorsController():
    
    def __init__(self, left_motor_gpios: tuple[str, str], right_motor_gpios: tuple[str, str]):
        self._left_motor = VesselMotor(left_motor_gpios[0], left_motor_gpios[1])
        self._right_motor = VesselMotor(right_motor_gpios[0], right_motor_gpios[1])
        self._engines_usage = 0.0
        self._balance = 0.0
    
    def stop_all_engines(self):
        self._left_motor.stop()
        self._right_motor.stop()
        
    def set_speed(self, motor_sign: str, slider_velocity: float):
        if not -100 < slider_velocity < 100:
            warnings.warn("Value should be between (-100 and 100)")
        velocity = slider_velocity / 100
        match motor_sign:
            case 'LEFT':
               self._left_motor.set_velocity(velocity)
            case 'RIGHT':
               self._right_motor.set_velocity(velocity)
            case _:
                raise ValueError(f"There is no motor: {motor_sign}")
    
    def get_motors_speed(self) -> tuple[float, float]:
        return (self._left_motor.get_motor_velocity(), self._right_motor.get_motor_velocity())
    
    def set_balance_from_slider(self, slider_balance: int):
        if not -100 <= slider_balance <= 100:
            raise ValueError(f"Balance slider value has to be in range <-100, 100>")
        self._balance = slider_balance/100
        self._update_motors_speed()
        
    def set_engines_usage_from_slider(self, slider_engines_usage: int):
           if not 0 <= slider_engines_usage <= 100:
               raise ValueError(f"Engines usage slider value has to be in range <0, 100>")
           self._engines_usage = slider_engines_usage/100
           self._update_motors_speed()
    
    # to update motors speed
    def _update_motors_speed(self):
        left_motor_speed = self._engines_usage + 2* self._balance * self._engines_usage
        right_motor_speed = self._engines_usage - 2* self._balance * self._engines_usage
        self._left_motor.set_velocity(left_motor_speed)
        self._right_motor.set_velocity(right_motor_speed)
        
    
        