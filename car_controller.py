import threading
import time
from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance


class CarController(object):
    ULTRASONIC_AVOIDANCE_CHANNEL = 20
    MAX_SPEED = 100
    ZERO_ANGLE = 90  # '90' is straight wheels
    MAX_ANGLE = 45  # from 45 to 135

    def __init__(self, config='config', ultrasonic_distance_stop_cm=20):
        self._ultrasonic_distance_stop_cm = ultrasonic_distance_stop_cm
        self._speed = 0
        self._angle = 0
        self._fws = front_wheels.Front_Wheels(db=config)
        self._bws = back_wheels.Back_Wheels(db=config)
        self.reset_wheels()

        self._ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(CarController.ULTRASONIC_AVOIDANCE_CHANNEL)
        self._ua_is_on = False
        self._ultrasonic_thread = threading.Thread(target=self.stop_if_obstacle_nearby, daemon=True).start()

    def reset_wheels(self):
        self._fws.turn(CarController.ZERO_ANGLE)
        self._angle = 0
        self._speed = 0

    def change_speed(self, diff):
        new_speed = self._speed + diff
        new_speed = min(max(new_speed, -CarController.MAX_SPEED), CarController.MAX_SPEED)
        if new_speed == 0:
            self.stop()
        elif new_speed * self._speed <= 0:
            if new_speed >= 0:
                self._bws.forward()
            else:
                self._bws.backward()
        self._bws.speed = abs(new_speed)
        self._speed = new_speed

    def change_angle(self, diff):
        new_angle = self._angle + diff
        new_angle = min(max(new_angle, -CarController.MAX_ANGLE), CarController.MAX_ANGLE)
        self._angle = new_angle
        self._fws.turn(CarController.ZERO_ANGLE + self._angle)

    def stop(self):
        self._bws.stop()
        self._speed = 0

    def stop_if_obstacle_nearby(self):
        while True:
            if self._ua_is_on:
                distance = self._ua.get_distance()
                if (self._speed > 0) and (distance < self._ultrasonic_distance_stop_cm):
                    self.stop()
            else:
                time.sleep(1)

    def change_ultrasonic_state(self, state):
        self._ua_is_on = state == 'on'

    def execute_action(self, action):
        print(f'action: {action}')
        if action['action'] == 'turn':
            self.change_angle(action['diff'])
        elif action['action'] == 'change_speed':
            self.change_speed(action['diff'])
        elif action['action'] == 'stop':
            self.stop()
        elif action['action'] == 'ultrasonic_on':
            self.change_ultrasonic_state('on')
        elif action['action'] == 'ultrasonic_off':
            self.change_ultrasonic_state('off')
        else:
            print(f'Not supported action: {action}')
