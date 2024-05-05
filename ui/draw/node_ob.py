class NodeOb:
    def __init__(self):
        print("node")

    @staticmethod
    def draw_oval(node, canvas, code_n_bugs):
        oval = canvas.create_oval(node.x - node.radius, node.y - node.radius,
                                  node.x + node.radius, node.y + node.radius,
                                  fill="white", outline="black", tags="node")
        canvas.tag_bind(oval, "<Button-3>", code_n_bugs.show_node_context_menu)
        canvas.bind("<B1-Motion>", code_n_bugs.move_node)
        return oval

    @staticmethod
    def draw_label(node, canvas):
        return canvas.create_text(node.x, node.y, text="nodo " + str(node.id), tags="node_label")
