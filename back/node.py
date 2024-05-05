from back.street import Street
from ui.draw.node_ob import NodeOb
from ui.node_properties_dialog import NodePropertiesDialog
from ui.street_properties_dialog import StreetProperties
from ui.draw.line_ob import LineOb


class Node:
    def __init__(self, x, y, id_number, radius=25):
        self.x = x
        self.y = y
        self.id = id_number
        self.radius = radius
        self.weight = 0
        self.time_percentage = 0
        self.load = 0
        self.connections = []
        self.oval = None
        self.label = None
        self.line_ob = LineOb()
        self.node_ob = NodeOb()
        self.id_street = 1

    def draw(self, canvas, code_n_bugs):
        self.oval = self.node_ob.draw_oval(self, canvas, code_n_bugs)
        self.label = self.node_ob.draw_label(self, canvas)

    def connect_node(self, other_node, canvas):
        dx = other_node.x - self.x
        dy = other_node.y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = self.x + self.radius * dx
        y1 = self.y + self.radius * dy
        x2 = other_node.x - other_node.radius * dx
        y2 = other_node.y - other_node.radius * dy
        line = self.line_ob.draw_line(x1, y1, x2, y2, canvas, self, other_node, self.id_street)
        other_street = Street(self, True, False, True,
                              0, 0, 0, line, x1, y1, x2, y2, self.id_street
                              )
        other_node.connections.append(other_street)
        node_street = Street(other_node, False, True, True,
                             0, 0, 0, line, x1, y1, x2, y2, self.id_street
                             )
        self.connections.append(node_street)
        self.id_street = self.id_street + 1

    def connect_out(self, canvas, x, y):
        dx = x - self.x
        dy = y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = self.x + self.radius * dx
        y1 = self.y + self.radius * dy
        x2 = x
        y2 = y
        line = self.line_ob.draw_line(x1, y1, x2, y2, canvas, self, None, self.id_street)
        node_street = Street(None, False, True, False,
                             0, 0, 0, line, x1, y1, x2, y2, self.id_street
                             )
        self.connections.append(node_street)
        self.id_street = self.id_street + 1

    def connect_in(self, canvas, x, y):
        dx = self.x - x
        dy = self.y - y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = x
        y1 = y
        x2 = self.x - self.radius * dx
        y2 = self.y - self.radius * dy
        line = self.line_ob.draw_line(x1, y1, x2, y2, canvas, self, None, self.id_street)
        node_street = Street(None, True, False, False,
                             0, 0, 0, line, x1, y1, x2, y2, self.id_street
                             )
        self.connections.append(node_street)
        self.id_street = self.id_street + 1

    def edit_properties(self, canvas):
        dialog = NodePropertiesDialog(canvas.master, self)
        canvas.wait_window(dialog)
        canvas.itemconfig(self.oval, fill="cyan")

    def show_connection_properties(self, node, canvas, line, other_node, id_street):
        connection_properties = StreetProperties(node, canvas, line, other_node, id_street, self.line_ob)
        canvas.wait_window(connection_properties)

    def remove_line(self, line, canvas, id_street):
        found_street = self.find_street_by_other_line(id_street, line)
        if found_street:
            canvas.delete(found_street.label_text)
            canvas.delete(found_street.line)
            self.connections.remove(found_street)

    def find_street_by_other_line(self, id_street, line):
        street = next(
            (street for street in self.connections if isinstance(street, Street) and (street.id_street == id_street
                                                                                      and street.line == line)),
            None)
        return street

    def remove_streets_from_the_node(self, canvas):
        for connection in self.connections:
            if connection.line:
                canvas.delete(connection.label_text)
                canvas.delete(connection.line)
        self.connections.clear()
