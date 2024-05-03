from back.street import Street
from ui.node_properties_dialog import NodePropertiesDialog
from ui.street_properties_dialog import StreetProperties


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

    def draw(self, canvas):
        self.oval = canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                       self.x + self.radius, self.y + self.radius,
                                       fill="white", outline="black", tags="node")
        self.label = canvas.create_text(self.x, self.y, text="nodo " + str(self.id), tags="node_label")

    def connect(self, other_node, canvas):
        dx = other_node.x - self.x
        dy = other_node.y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = self.x + self.radius * dx
        y1 = self.y + self.radius * dy
        x2 = other_node.x - other_node.radius * dx
        y2 = other_node.y - other_node.radius * dy

        line = canvas.create_line(x1, y1, x2, y2, width=4, arrow="last", tags=("connection_line",))
        other_street = Street(self, True, False, True,
                              0, 0, 0, line, x1, y1, x2, y2
                              )
        other_node.connections.append(other_street)
        node_street = Street(other_node, False, True, True,
                             0, 0, 0, line, x1, y1, x2, y2
                             )
        self.connections.append(node_street)
        canvas.tag_bind(line, "<Button-1>", lambda e: self.remove_line(line, canvas))
        canvas.tag_bind(line, "<Button-3>", lambda e: self.show_connection_properties(self, canvas, line, other_node))

    def connect_out(self, canvas, x, y):
        dx = x - self.x
        dy = y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = self.x + self.radius * dx
        y1 = self.y + self.radius * dy
        x2 = x #* dx
        y2 = y #* dy

        line = canvas.create_line(x1, y1, x2, y2, width=4, arrow="last", tags=("connection_line",))
        node_street = Street(None, False, True, False,
                             0, 0, 0, line, x1, y1, x2, y2
                             )
        self.connections.append(node_street)
        canvas.tag_bind(line, "<Button-1>", lambda e: self.remove_line(line, canvas))
        canvas.tag_bind(line, "<Button-3>",
                        lambda e: self.show_connection_properties(self, canvas, line, None))

    def connect_in(self, canvas, x, y):
        dx = self.x - x
        dy = self.y - y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        dx /= dist
        dy /= dist
        x1 = x #+ 25 * dx
        y1 = y #+ 25 * dy
        x2 = self.x - self.radius * dx
        y2 = self.y - self.radius * dy

        line = canvas.create_line(x1, y1, x2, y2, width=4, arrow="last", tags=("connection_line",))
        node_street = Street(None, True, False, False,
                             0, 0, 0, line, x1, y1, x2, y2
                             )
        self.connections.append(node_street)
        canvas.tag_bind(line, "<Button-1>", lambda e: self.remove_line(line, canvas))
        canvas.tag_bind(line, "<Button-3>",
                        lambda e: self.show_connection_properties(self, canvas, line, None))

    def edit_properties(self, canvas):
        dialog = NodePropertiesDialog(canvas.master, self)
        canvas.wait_window(dialog)
        canvas.itemconfig(self.oval, fill="cyan")

    @staticmethod
    def show_connection_properties(self, canvas, line, other_node):
        connection_properties = StreetProperties(self, canvas, line, other_node)
        canvas.wait_window(connection_properties)

    def find_street_by_other_node(self, other_node):
        street = next(
            (street for street in self.connections if isinstance(street, Street) and street.other_node == other_node),
            None)
        return street

    def remove_line(self, line, canvas):
        found_street = self.find_street_by_other_line(line)
        canvas.delete(line)
        if found_street:
            canvas.delete(found_street.label_text)
            self.connections.remove(found_street)

    def find_street_by_other_line(self, line):
        street = next(
            (street for street in self.connections if isinstance(street, Street) and street.line == line),
            None)
        return street

    def remove_streets_from_the_node(self, canvas):
        for connection in self.connections:
            if connection.line:
                canvas.delete(connection.label_text)
                canvas.delete(connection.line)
        self.connections.clear()
