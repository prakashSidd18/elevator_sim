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





### Events



### Scheduling







## Future work
