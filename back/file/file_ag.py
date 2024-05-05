import pickle


class FileAg:
    def __init__(self):
        print("ff")

    @staticmethod
    def save_model(nodes, filedialog):
        print("save")
        file_name = filedialog.asksaveasfilename(defaultextension=".dkv")
        if file_name:
            with open(file_name, "wb") as file:
                pickle.dump(nodes, file)

    @staticmethod
    def load_model(filedialog):
        print("load")
        file_name = filedialog.askopenfilename(defaultextension=".dkv")
        if file_name:
            with open(file_name, "rb") as file:
                return pickle.load(file)
        return None
