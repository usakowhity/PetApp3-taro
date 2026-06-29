# ui/step_all_prompts_view_en.py

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from controller import STATE_LIST, STATE_META_EN


class StepAllPromptsView(QWidget):
    """
    English version:
    View all prompts for all 15 states
    - Thumbnail
    - English-only UI
    - English Description + English Prompt
    - Buttons for Gemini / Copilot / Pika / Google Translate
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.base_dir = controller.BASE_DIR
        self.prompts_dir = os.path.join(controller.generated_dir, "prompts")
        self.assets_dir = controller.assets_dir

        self.init_ui()

    # ---------------------------------------------------------
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(15)

        title = QLabel("All Prompts (15 States)")
        title.setStyleSheet("font-size: 32pt; font-weight: bold;")
        root.addWidget(title)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        root.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        inner = QVBoxLayout(container)
        inner.setSpacing(25)

        # Create block for each state
        for state in STATE_LIST:
            block = self.create_state_block(state)
            inner.addLayout(block)

        inner.addStretch()

        # Bottom buttons
        bottom = QHBoxLayout()
        bottom.setSpacing(20)
        root.addLayout(bottom)

        btn_gemini = QPushButton("Open Gemini")
        btn_gemini.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_gemini.clicked.connect(lambda: self.controller.open_url("https://gemini.google.com"))
        bottom.addWidget(btn_gemini)

        btn_copilot = QPushButton("Open Copilot")
        btn_copilot.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_copilot.clicked.connect(lambda: self.controller.open_url("https://copilot.microsoft.com"))
        bottom.addWidget(btn_copilot)

        btn_pika = QPushButton("Open Pika")
        btn_pika.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_pika.clicked.connect(lambda: self.controller.open_url("https://pika.art"))
        bottom.addWidget(btn_pika)

        btn_translate = QPushButton("Google Translate (JP → EN)")
        btn_translate.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_translate.clicked.connect(
            lambda: self.controller.open_url("https://translate.google.com/?sl=ja&tl=en")
        )
        bottom.addWidget(btn_translate)

        btn_guide = QPushButton("Open AI Generation Guide")
        btn_guide.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_guide.clicked.connect(self.on_guide)
        root.addWidget(btn_guide)

        btn_back = QPushButton("Back to Edit Menu")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_back.clicked.connect(self.on_back)
        root.addWidget(btn_back)

    # ---------------------------------------------------------
    def create_state_block(self, state: str):
        """
        Block for one state (thumbnail + description + prompts)
        """
        meta_en = STATE_META_EN.get(state, {})
        name_en = meta_en.get("name", state)

        layout = QVBoxLayout()
        layout.setSpacing(5)

        header = QLabel(f"■ {state} : {name_en}")
        header.setStyleSheet("font-size: 24pt; font-weight: bold;")
        layout.addWidget(header)

        # Upper row: thumbnail + English description
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        layout.addLayout(top_row)

        # Thumbnail
        thumb_label = QLabel()
        thumb_label.setFixedSize(160, 160)
        thumb_label.setStyleSheet("background-color: #dddddd;")
        thumb_label.setAlignment(Qt.AlignCenter)

        thumb_path = os.path.join(self.assets_dir, "states", f"{state}.png")
        if os.path.exists(thumb_path):
            pix = QPixmap(thumb_path)
            if not pix.isNull():
                thumb_label.setPixmap(pix.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                thumb_label.setText("No Image")
        else:
            thumb_label.setText("No Image")

        top_row.addWidget(thumb_label)

        # English description
        desc_en_label = QLabel(meta_en.get("description", ""))
        desc_en_label.setStyleSheet("font-size: 18pt;")
        desc_en_label.setWordWrap(True)
        top_row.addWidget(desc_en_label, 1)

        # Load prompt text (English only)
        jp_text, en_text = self.load_prompt_texts(state)

        # English Prompt
        lbl_en = QLabel("【English Prompt】")
        lbl_en.setStyleSheet("font-size: 18pt; font-weight: bold; margin-top: 5px;")
        layout.addWidget(lbl_en)

        txt_en = QTextEdit()
        txt_en.setReadOnly(True)
        txt_en.setStyleSheet("font-size: 16pt;")
        txt_en.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        txt_en.setMinimumHeight(80)
        txt_en.setText(en_text)
        layout.addWidget(txt_en)

        return layout

    # ---------------------------------------------------------
    def load_prompt_texts(self, state: str):
        """
        PetApp3: prompt file contains English only.
        Japanese description comes from STATE_META_EN.
        """
        path = os.path.join(self.prompts_dir, f"{state}.txt")
        if not os.path.exists(path):
            return "", ""

        # English prompt (full text)
        with open(path, "r", encoding="utf-8") as f:
            en = f.read().strip()

        # Japanese description = STATE_META_EN
        jp = STATE_META_EN.get(state, {}).get("description", "")

        return jp, en

    # ---------------------------------------------------------
    def on_guide(self):
        self.controller.show_stepAIGuideForMedia()

    def on_back(self):
        self.controller.show_stepEditMenu()
