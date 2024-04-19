# Elevator Simulator

This is the code for a simple elevator simulation to schedule elevator calls as it occurs.

## Requirements

* Python 3.7+

To run the simulator, please use Python 3.x. The code is tested on Python 3.10, 3.11

## Deployment

```python3 main.py```

You can run the `main.py` script and the simulator will start running.

### Input 

The input to the program is a set of elevator calls and their corresponding timestamps as specified in `main.py`

```
# provide the elevator calls for simulation
# FORMAT:
# input_floors(list of str)[required]: <floor_called><direction><destination_floor>
# ex: "4u6" means elevator called on floor 4, to go up, with destination floor 6
# timestamps(list of floats): call[i] made at timestamps[i]
# if timestamps specified as None, random timestamps will be generated for each call
```


A few test cases are already provided and the script will start executing them. 
You can also create your own test cases as specified above to test on them.

## Program Flow

At the core of the simulator are the 2 classes `Elevator` and `Events`.
1. The `main.py` script starts with creating an object of class `Elevator`. 
2. Next each test case is called, and the `Elevator` checks if the calls are valid.
3. If all calls are valid, the simulation starts from time `t=0secs.` until all the calls are made. Each call is instantiated as an object of `Events` class and stored in the global queue of `Elevator` object.
4. Once the calls are instantiated, the simulation starts running automatically taking in account the `time_elapsed` since start. You get a verbose description of the events happening and also the status of elevator (its current floor).
5. After the simulation is finished, the script displays the order of floors visited based on the input calls and their timestamps.

> **_NOTE:_**  While the input specify the destination floors in the calls, the calls are made available to be considered only at the timestamp corresponding to it. 
> The destination events are also created only after the elevator has reached that floor as scheduled. 


### Elevator

The `Elevator` class stores properties of the elevator such as number of floors in the elevator, global events queue, call queue, destination queue etc.
The simulation starts by calling the `run_elevator` function. The execution follows the following order:
1. Start clock
2. Wait until a call is available
3. If a call is available, put it on the call queue
4. If call queue is populated and the elevator is stopped, pick next event
5. Else wait until next floor is reached, concurrently updating the queue as the calls are made
6. If the next floor is reached, add more calls are remove current call if it was a destination call
7. Repeat from Step 3 until call queue is not empty and all calls on the global stack are not executed
8. If done, display the final order of floors visited


### Scheduling

To update the state of call queue, we make a call to `rearrange_call_queue` function which takes into account both the call queues and any events on the destination queue.

Currently, the scheduling prioritizes calls made from nearby floors in order of their occurrences.
If a call occurred, either internally or externally, the queue is reorganized to serve calls from nearby floors where the elevator is located at that time instant. 
The current floor of elevator is also updated as it moves to destination floors.


## Future work

While this is not an optimal implementation to simulate a real world elevator simulator, more things could be built on the current implementation to simulate real world scenarios. Some examples can be:

1. As it stands, the elevator places a low priority on the destination events once the elevator has been boarded on a floor. 
Implementing a timer to compute the time since elevator has been boarded at a certain floor, the criteria to schedule calls can be updated to penalize large wait times to destination floors.
2. We assume the elevator has infinite capacity and we do not take the capacity into account while scheduling. 
In practice every elevator has a maximum limit, and this needs to be taken in account while boarding, de-boarding and scheduling the elevator calls. 
For example, if max capacity is reached, de-boarding will take priority over serving calls.
3. While the calls are added as soon as they are made available, this needs to be done on a separate thread since it modifies the current call queue. 
Similarly, the reorganization of calls should be done on a separate thread, de-coupled from execution of the next call in a thread-safe manner. 