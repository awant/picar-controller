import socket
import json
import argparse
from car_controller import CarController

BUFSIZE = 1024


def process_next_buffer(conn, car):
    buffer = conn.recv(BUFSIZE)
    if not buffer:
        return False
    data = buffer.decode('utf-8').split('\n')
    for action in data:
        if action:
            action_dict = json.loads(action)
            car.execute_action(action_dict)
    return True


def start_server(car, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                if not process_next_buffer(conn, car):
                    break


def main():
    parser = argparse.ArgumentParser(description='PiCar controller server')
    parser.add_argument('--port', type=int, default=21567,
                        help='a port to connect')
    args = parser.parse_args()

    car = CarController()
    start_server(car, args.port)


main()
