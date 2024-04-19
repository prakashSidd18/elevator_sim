import elevator
import random
if __name__ == '__main__':
    elevator = elevator.Elevator()
    print('Elevator created!')
    elevator.info()
    print('***************************************')

    '''
    ## provide the elevator calls for simulation
    ## FORMAT:
    ## input_floors(list of str)[required]: <floor_called><direction><destination_floor>
    ## ex: "4u6" means elevator called on floor 4, to go up, with destination floor 6
    ## timestamps(list of floats): call[i] made at timestamps[i]
    ## if timestamps specified as None, random timestamps will be generated for each call
    '''

    calls = [{'input_floors': ["0u9"],
              'timestamps': None},
             {'input_floors': ["3d0", "5u7"],
              'timestamps': None},
             {'input_floors': ["4u6", "3d0", "0u9", "5u7"],
              'timestamps': list(range(0, 4*10, 10))},
             {'input_floors': ["4u6", "3d0", "0u9", "5u7"],
              'timestamps': None},
             {'input_floors': ["4u6", "3d0", "0u9", "5u7", "3d2", "4u7", "9d2"],
              'timestamps': list(range(0, 7*3, 3))},
             {'input_floors': ["4u6", "3d0", "0u9", "5u7", "3d2", "4u7", "9d2"],
              'timestamps': [8, 20, 30, 32, 45, 50, 57]},
             {'input_floors': ["4u6", "3d0", "0u9", "5u7", "3d2", "4u7", "9d2"],
              'timestamps': None},
             ]

    for call in calls:
        print('***********New Sim**************')
        input_floors = call['input_floors']
        timestamps = call['timestamps']
        # Generate random timestamps for each call if not specified
        if timestamps is None:
            timestamps = sorted(random.sample(range(0, 10*len(input_floors)), len(input_floors)))

        print('Calls: ', input_floors)
        print('Made at times: ', timestamps)
        input('Press [Enter] to start simulation...')
        elevator.schedule_calls(input_floors, timestamps)

        elevator.run_elevator()

        elevator.reset()






