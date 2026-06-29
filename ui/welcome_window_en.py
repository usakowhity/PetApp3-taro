# ui/welcome_window_en.py
import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class WelcomeWindow(QWidget):
    """
    Welcome screen (English version for PetApp3)
    - Play with your pet
    - Edit pet information (StepEditMenu)
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Welcome")
        self.setFixedSize(600, 600)

        # Center the window on screen
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

        self._build_ui()

    # ---------------------------------------------------------
    # UI Build
    # ---------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ---------------------------------------------------------
        # hero.png path
        # ---------------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))  # ui/
        root_dir = os.path.dirname(base_dir)                   # PetApp3/
        hero_path = os.path.join(root_dir, "assets", "ui", "hero.png")

        # ---------------------------------------------------------
        # hero image
        # ---------------------------------------------------------
        if os.path.exists(hero_path):
            hero_label = QLabel()
            pix = QPixmap(hero_path)
            pix = pix.scaledToWidth(300, Qt.SmoothTransformation)
            hero_label.setPixmap(pix)
            hero_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(hero_label)
        else:
            print("[WelcomeWindow EN] hero.png not found:", hero_path)

        # Title
        title = QLabel("Welcome!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        # Play with pet
        btn_play = QPushButton("Play with your pet")
        btn_play.setStyleSheet("font-size: 24px; padding: 14px;")
        btn_play.clicked.connect(self.on_play_clicked)   # ←★ 修正ポイント
        layout.addWidget(btn_play)

        # Edit pet information
        btn_edit = QPushButton("Edit pet information")
        btn_edit.setStyleSheet("font-size: 24px; padding: 14px;")
        btn_edit.clicked.connect(self.controller.show_stepEditMenu)
        layout.addWidget(btn_edit)

        layout.addStretch()

    # ---------------------------------------------------------
    # ★ Play ボタンを押したときに音声認識と顔検出を開始する
    # ---------------------------------------------------------
    def on_play_clicked(self):
        # Start Whisper listener
        try:
            self.controller.start_voice_listener()
        except Exception as e:
            print("[WelcomeWindow] start_voice_listener error:", e)

        # Start Face Detector
        try:
            self.controller.start_face_detector()
        except Exception as e:
            print("[WelcomeWindow] start_face_detector error:", e)

        # Then show PlayWindow
        self.controller.show_play()

    # ---------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
