from random import random


class Street:
    def __init__(self, other_node, its_input, its_output, its_connection, min_capacity,
                 max_capacity, traffic_lights, line):
        self.other_node = other_node
        self.cars = 0
        self.its_input = its_input
        self.its_output = its_output
        self.its_connection = its_connection
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity
        self.traffic_lights = traffic_lights
        self.label_text = None
        self.line = line
