from ui.draw.node_ob import NodeOb
from ui.draw.line_ob import LineOb


class LoadModel:
    def __init__(self):
        self.node_ob = NodeOb()
        self.line_ob = LineOb()
        print("")

    def load(self, nodes, canvas, code_n_bugs):
        for node in nodes:
            node.oval = self.node_ob.draw_oval(node, canvas, code_n_bugs)
            node.label = self.node_ob.draw_label(node, canvas)
            canvas.tag_bind(node.oval, "<Button-3>", code_n_bugs.show_node_context_menu)
            canvas.bind("<B1-Motion>", code_n_bugs.move_node)
        for node in nodes:
            self.filter_connection(node, node.connections, canvas)

    def filter_connection(self, node, connections, canvas):
        for street in connections:
            if not street.its_input and street.its_output and street.its_connection:
                print(street.id_street)
                street.line = self.line_ob.draw_line(street.x1, street.y1, street.x2, street.y2, canvas,
                                                     node, street.other_node, street.id_street)
                self.line_ob.draw_label_line(street.min_capacity, street.max_capacity, street, canvas, street.line)
            elif not street.its_connection and (street.its_input or street.its_output):
                print("taf")
                street.line = self.line_ob.draw_line(street.x1, street.y1, street.x2, street.y2, canvas,
                                                     node, street.other_node, street.id_street)
                self.line_ob.draw_label_line(street.min_capacity, street.max_capacity, street, canvas, street.line)
