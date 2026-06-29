# ui/step_media_view_en.py

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class StepMediaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Edit / Add Images & Videos")
        self.setMinimumSize(1000, 800)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Media for Each State")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        layout.addWidget(title)

        body = QHBoxLayout()
        layout.addLayout(body)

        # Left: state list
        self.list_states = QListWidget()
        self.list_states.setStyleSheet("font-size: 18pt;")
        body.addWidget(self.list_states, 1)

        # Right: preview
        right = QVBoxLayout()
        body.addLayout(right, 2)

        # Image preview
        self.preview_image = QLabel()
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setMinimumSize(320, 320)
        self.preview_image.setStyleSheet("border: 1px solid #ccc; background: #fafafa;")

        # Video preview
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(320, 320)
        self.video_widget.hide()

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)

        right.addWidget(self.preview_image)
        right.addWidget(self.video_widget)

        # Buttons
        btn_row = QHBoxLayout()
        right.addLayout(btn_row)

        btn_open_folder = QPushButton("Open generated folder")
        btn_open_folder.setStyleSheet("font-size: 20pt; padding: 8px;")
        btn_open_folder.clicked.connect(self.on_open_folder)
        btn_row.addWidget(btn_open_folder)

        btn_back = QPushButton("Back to Edit Menu")
        btn_back.setStyleSheet("font-size: 20pt; padding: 8px;")
        btn_back.clicked.connect(self.on_back)
        btn_row.addWidget(btn_back)

        # Populate state list
        self.populate_states()
        self.list_states.currentItemChanged.connect(self.on_state_changed)

    # ---------------------------------------------------------
    def populate_states(self):
        self.list_states.clear()

        # Use controller.media
        for state in sorted(self.controller.media.keys()):
            self.list_states.addItem(QListWidgetItem(state))

        if self.list_states.count() > 0:
            self.list_states.setCurrentRow(0)

    # ---------------------------------------------------------
    def on_state_changed(self, current, _prev):
        if not current:
            return

        state = current.text()
        path = self.controller.media.get(state)

        # Stop video
        self.player.stop()
        self.video_widget.hide()
        self.preview_image.show()

        if not path or not os.path.exists(path):
            self.preview_image.setPixmap(QPixmap())
            self.preview_image.setText("No media available")
            return

        # Video
        if path.lower().endswith(".mp4"):
            self.preview_image.hide()
            self.video_widget.show()

            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.play()
            return

        # Image
        pix = QPixmap(path)
        if not pix.isNull():
            scaled = pix.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_image.setPixmap(scaled)
            self.preview_image.setText("")
        else:
            self.preview_image.setPixmap(QPixmap())
            self.preview_image.setText("Failed to load image")

    # ---------------------------------------------------------
    def on_open_folder(self):
        folder = self.controller.generated_dir
        if os.path.exists(folder):
            import subprocess
            subprocess.Popen(f'explorer "{folder}"')

    # ---------------------------------------------------------
    def on_back(self):
        self.close()
        self.controller.show_stepEditMenu()
