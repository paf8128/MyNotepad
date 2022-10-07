import sys
from Edit import *
class Manager(QWidget):
    def __init__(self):
        super().__init__()
        self.Edits = list()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = Manager()
    edit = Edit(manager)
    if len(sys.argv) == 2:
        edit.textEdit.open(sys.argv[1])
    sys.exit(app.exec_())
