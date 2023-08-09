# implementation of exercise 2.2.1
# Simulator.py contains specifications for RootCoordinators, Coordinators and Models to simulate DEVS experiments
# comment/TODO:
# - There is something wrong with the Coordinator Implementation. It´s probably something with the imminent_children.

# class RootCoordinator specifies a Root Coordinator for DEVS
class RootCoordinator:
    def __init__(self):
        self.child = None  # := child of Root Coordinator Object, meaning a Coupled DEVS Object
        self.t: int = 0  # := internal Clock t of Root Coordinator Object
        self.message_port = None  # := message port of Root Coordinator Object to communicate with child

    # method that resets parameters of Root Coordinator Object, used for multiple runs in an experiment
    def reset(self):
        self.t = 0
        self.message_port = None
        self.child.reset()

    # method that specifies what happens if the Root Coordinator receives a message
    def received_message(self, message):
        # message is an array of 3-4 elements
        message_type = message[0]  # := Type of message, can be x, y or *
        message_content = message[1]  # := Content of message, usually empty string or output of a simulator
        message_time = message[2]  # := Time of creation, Objects append their own internal time to message on creation

        match message_type:
            case "*":
                self.child.message_port_for_parent = ["*", "", message_time]
            case "x":
                self.child.message_port_for_parent = ["x", message_content, message_time]
            case "y":
                message_sender = message[3]
                empty_x_message = ["x", message_content, message_time, message_sender]
                self.child.message_port_for_parent = empty_x_message
            case "d":
                self.t = message_time

        # always flushes message port after receiving a message
        self.message_port = None

    # method to run a simulation step for Root Coordinator Object
    def run(self):
        if self.t == 0:
            i_message = ["i", "i", self.t, None]
            self.child.message_port_for_parent = i_message
        else:
            if self.message_port is not None:
                self.received_message(self.message_port)
            else:
                self.child.message_port_for_parent = ["*", "", self.t]
        self.t += 1
        self.child.run()


# class Coordinator that specifies a Coordinator for DEVS
class Coordinator:

    def __init__(self, parent, children, coupledDEVS):
        self.coupledDEVS = coupledDEVS  # := stores a coupled DEVS model Object
        self.parent = parent  # := a Root Coordinator Object
        self.children = children  # := contains at least one Simulator Object
        self.message_port_for_parent = None  # := used to communicate with parent
        self.message_port_for_children = None  # := used to communicate with children
        self.t_last_event: int = 0  # := Time of Last Event
        self.t_next_event: int = 0  # := Time of Next Event
        self.imminent_child = None  # := stores imminent child
        self.event_list = []  # := used for obtaining an imminent child

    # method that resets the Coordinator Object parameters
    def reset(self):
        self.message_port_for_parent = None
        self.message_port_for_children = None
        self.t_last_event: int = 0
        self.t_next_event: int = 0
        self.imminent_child = None
        self.event_list = []

        for child in self.children:
            child.reset()

    # method that specifies what happens if Coordinator Object receives a message
    def received_message(self, message):
        message_type = message[0]
        message_content = message[1]
        message_time = message[2]

        # get list of next and last events of children
        children_last_event = []
        children_next_event = []
        for child in self.children:
            children_last_event.append(child.t_last_event)
            children_next_event.append(child.t_next_event)

        match message_type:
            case "i":
                i_message = ["i", "", message_time]
                self.event_list = []
                for child in self.children:
                    child.message_port = i_message
                    x = (child, child.atomicDEVS.pos, child.t_next_event)
                    self.event_list.append(x)

                self.event_list = self.coupledDEVS.select(self.event_list)

                self.t_last_event = max(children_last_event)
                self.t_next_event = min(children_next_event)

                self.message_port_for_parent = None
            case "*":
                self.imminent_child = self.event_list[0]
                sim = self.imminent_child[0]
                pos = self.imminent_child[1]
                time = self.imminent_child[2]
                star_message = ["*", message_content, message_time, None]
                sim.message_port = star_message
                self.event_list.remove((sim, pos, time))
                self.event_list.append((sim, pos, sim.t_next_event))
                self.event_list = self.coupledDEVS.select(self.event_list)

                self.t_last_event = message_time
                self.t_next_event = min(children_next_event)

                self.message_port_for_parent = None
            case "x":
                message_sender = message[3]
                empty_x_message = ["x", "", message_time, message_sender]
                x_message = ["x", message_content, message_time, message_sender]

                receivers = self.coupledDEVS.children_getting_input_by_child(message_sender)

                for child in self.children:
                    if child.atomicDEVS.name in receivers:
                        child.message_port = x_message
                    else:
                        child.message_port = empty_x_message

                self.event_list = self.coupledDEVS.select(self.event_list)
                self.t_last_event = message_time
                self.t_next_event = min(children_next_event)

                self.message_port_for_parent = None
            case "y":
                message_sender = message[3]
                y_message = ["y", message_content, message_time, message_sender]
                self.parent.message_port = y_message

                self.message_port_for_children = None
            case "d":
                d_message = ["d", "", message_time]
                self.parent.message_port = d_message

                self.message_port_for_children = None

    # method that runs a simulation step of the Coordinator Object
    def run(self):
        if self.message_port_for_parent is not None:
            self.received_message(self.message_port_for_parent)

        if self.message_port_for_children is not None:
            self.received_message(self.message_port_for_children)

        for child in self.children:
            child.run()


# class Simulator specifies the DEVS Simulator
class Simulator:
    def __init__(self, atomicDEVS):
        self.parent = None # := Parent of Simulator, a Coordinator Object
        self.t: int = 0 # := internal clock t
        self.t_last_event: int = 0 # := Time of Last Event
        self.t_next_event: int = 0 # := Time of Next Event
        self.message_port = None # := used to communicate with parent
        self.atomicDEVS = atomicDEVS # := contains atomic DEVS model Object of Simulator Object
        self.name = atomicDEVS.name # := contains name of atomic DEVS model Object
        self.current_state = atomicDEVS.initial_state # := stores the state of atomic DEVS model Object

    # method that resets Simulator Object parameters
    def reset(self):
        self.t: int = 0
        self.t_last_event: int = 0
        self.t_next_event: int = 0
        self.message_port = None
        self.current_state = self.atomicDEVS.initial_state
        self.atomicDEVS.current_state = self.atomicDEVS.initial_state

    # method that specifies what happens if the Simulator Object receives a message
    def received_message(self, message):
        message_type = message[0]
        message_content = message[1]
        message_time = message[2]

        match message_type:
            case "i":
                pass
            case "*":
                y = self.atomicDEVS.lambda_()
                if y != "":
                    y_message = ["y", y, message_time, self]
                    self.parent.message_port_for_children = y_message
                else:
                    d_message = ["d", "d", self.t_next_event]
                    self.parent.message_port_for_children = d_message
                self.current_state = self.atomicDEVS.deltaInt()
            case "x":
                elapsed_time = message_time - self.t_last_event
                self.current_state = self.atomicDEVS.deltaExt(elapsed_time, message_content)

                d_message = ["d", "d", self.t_next_event]
                self.parent.message_port_for_children = d_message

        self.t = message_time
        self.t_last_event = message_time
        self.t_next_event = self.t_last_event + self.atomicDEVS.ta()

        self.message_port = None

    # method that simulates one step of the Simulator Object
    def run(self):
        if self.message_port is not None:
            self.received_message(self.message_port)
            self.message_port = None

# function that simulate a RootCoordinator Object and returns the state of all Simulators
def devs_simulator(rootCoordinator):
    status = {}
    for c in rootCoordinator.child.children:
        status[c.atomicDEVS.name] = c.atomicDEVS.current_state
    rootCoordinator.run()
    # print(status)
    return status

# function that simulates a RootCoordinator Object for a number of specified steps
def simulator_loop(rootCoordinator, max_steps):
    for x in range(max_steps):
        devs_simulator(rootCoordinator)
