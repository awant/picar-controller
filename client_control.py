from tkinter import *
import socket
import json
import argparse

TURN_ANGLE = 45
CHANGE_SPEED_UP = 50
CHANGE_SPEED_DOWN = 50

BTN_ACTIONS = {
    'd': {'action': 'turn', 'diff': TURN_ANGLE},
    'a': {'action': 'turn', 'diff': -TURN_ANGLE},
    'w': {'action': 'change_speed', 'diff': CHANGE_SPEED_UP},
    's': {'action': 'change_speed', 'diff': -CHANGE_SPEED_DOWN},
    'e': {'action': 'stop'},
    '[': {'action': 'ultrasonic_on'},
    ']': {'action': 'ultrasonic_off'}
}
EXIT_BTN = 'q'


def send_action(event, sock):
    action = BTN_ACTIONS[event.char]
    print(f'action: {action}')
    if sock is not None:
        sock.send((json.dumps(action)+'\n').encode())


def bind_btn_actions(window, sock):
    for button_key in BTN_ACTIONS.keys():
        window.bind(button_key, lambda event: send_action(event, sock))
    window.bind(EXIT_BTN, lambda event: window.quit())


def draw_controller(sock, title='Car controller'):
    root = Tk()
    root.title(title)
    bind_btn_actions(root, sock)
    return root


def start_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        root = draw_controller(sock)
        root.mainloop()


def main():
    parser = argparse.ArgumentParser(description='PiCar controller client')
    parser.add_argument('--host', type=str, required=True,
                        help='an ip address of the car')
    parser.add_argument('--port', type=int, default=21567,
                        help='a port to connect')
    args = parser.parse_args()
    start_client(args.host, args.port)


main()
