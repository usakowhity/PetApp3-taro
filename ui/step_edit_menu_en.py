from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class StepEditMenu(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Edit Menu")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("Edit Pet Profile / Media / Prompts")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28pt; font-weight: bold;")
        layout.addWidget(title)

        # Edit Profile
        btn_profile = QPushButton("Edit Pet Profile")
        btn_profile.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_profile.clicked.connect(self.on_edit_profile)
        layout.addWidget(btn_profile)

        # View All Prompts
        btn_prompts = QPushButton("View All Prompts")
        btn_prompts.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_prompts.clicked.connect(self.on_view_prompts)
        layout.addWidget(btn_prompts)

        # Edit Media
        btn_media = QPushButton("Edit / Add Images & Videos")
        btn_media.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_media.clicked.connect(self.on_edit_media)
        layout.addWidget(btn_media)

        # Back to Welcome
        btn_back = QPushButton("Back to Welcome")
        btn_back.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_back.clicked.connect(self.on_back)
        layout.addWidget(btn_back)

    # ---------------------------------------------------------
    def on_edit_profile(self):
        self.close()
        self.controller.show_stepB2()

    def on_view_prompts(self):
        self.close()
        self.controller.show_stepAllPromptsView()

    def on_edit_media(self):
        self.close()
        self.controller.show_stepMediaView()

    def on_back(self):
        self.close()
        self.controller.show_welcome()
