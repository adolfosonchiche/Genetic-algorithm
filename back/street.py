from random import random


class Street:
    def __init__(self, other_node, its_input, its_output, its_connection, min_capacity,
                 max_capacity, traffic_lights, line, x1, y1, x2, y2, id_street):
        self.other_node = other_node
        self.cars = 0
        self.max_car = 0
        self.its_input = its_input
        self.its_output = its_output
        self.its_connection = its_connection
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity
        self.traffic_lights = traffic_lights
        self.label_text = None
        self.line = line
        self.id_street = id_street
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
