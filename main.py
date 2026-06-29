import sys
import os
from PySide6.QtWidgets import QApplication

os.environ["PETAPP_LANG"] = "en"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Load controller dynamically
import importlib.util
controller_path = os.path.join(BASE_DIR, "controller.py")
spec = importlib.util.spec_from_file_location("controller", controller_path)
controller_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller_module)

from controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)

    c = Controller(BASE_DIR)
    c.show_welcome()

    sys.exit(app.exec())
