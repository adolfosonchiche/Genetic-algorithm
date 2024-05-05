

class LineOb:
    def __init__(self):
        print("ff")

    @staticmethod
    def draw_line(x1, y1, x2, y2, canvas, node, other_node, id_street):
        line = canvas.create_line(x1, y1, x2, y2, width=2, arrow="last", tags=("connection_line",))
        canvas.tag_bind(line, "<Button-1>", lambda e: node.remove_line(line, canvas, id_street))
        canvas.tag_bind(line, "<Button-3>",
                        lambda e: node.show_connection_properties(node, canvas, line, other_node, id_street))
        canvas.itemconfig(line, fill="blue")
        return line

    @staticmethod
    def draw_label_line(min_capacity, max_capacity, street, canvas, line):
        x1, y1, x2, y2 = canvas.coords(line)
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        label_text = f"min: {min_capacity}\n máx: {max_capacity} \n car: {street.cars} \n traffic%: {street.traffic_lights}"

        if street.label_text:
            canvas.delete(street.label_text)
        canvas.label = canvas.create_text(x_center, y_center, text=label_text, font=("Arial", 10), )
        street.label_text = canvas.label
        canvas.itemconfig(canvas.label, fill="red")
