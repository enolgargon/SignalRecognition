import os
from multiprocessing import Process


def launch_screen_control():
    os.system('python ./screen_control/control.py')


def launch_logic():
    os.system('python ./logic/start.py')


def launch_camera_control():
    os.system('python ./camera_control/control.py')


def main():
    screen_control_process = Process(target=launch_screen_control)
    logic_process = Process(target=launch_logic)
    camera_control_process = Process(target=launch_camera_control)

    screen_control_process.start()
    logic_process.start()
    camera_control_process.start()


if __name__ == '__main__':
    main()
