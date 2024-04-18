import threading
import time
import sys

def background():
    while True:
        time.sleep(3)
        print('disarm me by typing disarm')


def other_function():
    print('You disarmed me! Dying now.')


data = []


def get_input():
    data.append(input())


input_thread = threading.Thread(target=get_input)
input_thread.daemon = True
input_thread.start()

input_thread.join()
while True:
    if data[-1] == 'q':
        print('Final queue', data)
        print('Ending input!')
        sys.exit()
    else:
        print(data)
        get_input()