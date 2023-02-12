# picar-controller
A simple controller for Sunfounder PiCar robot kit
#### How to use:
1. Get an ip for your raspberry pi car: <ip>
2. Copy **server_control.py** and **car_controller.py** inside a folder **SunFounder_PiCar-S/example** on the raspberry pi.
3. Run the server_control.py script by typing
    ```python3 server_control.py```
4. Locally, on your desktop run a client by:
    ```python3 client_control.py --host <ip>```

The **client_control.py** script will create a small window (with tkinter package) and will start passing certain keystrokes as actions on the server.

#### Buttons
| key | action                                                        |
|-----|---------------------------------------------------------------|
| d   | turn right 45 degrees                                         |
| a   | turn left 45 degrees                                          |
| w   | change_speed: +50 (max: 100)                                  |
| s   | change_speed: -50 (min: -100)                                 |
| e   | stop the car                                                  |
| q   | exit the script and close the window                          |
| [   | turn on ultrasonic module and stop before an obstacle (20 cm) |
| ]   | turn off ultrasonic module                                    |
