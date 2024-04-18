import threading
import time
import sys

data = []


def get_input():
    data.append(input())


input_thread = threading.Thread(target=get_input)
input_thread.daemon = True
input_thread.start()

input_thread.join()
while True:
    if data[-1] == 'q':
        print('Final queue', data[:-1])
        print('Ending input!')
        sys.exit()
    else:
        print(data)
        get_input()