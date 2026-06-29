# ui/step_ai_guide_en.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt


class StepAIGuideEn(QWidget):
    """
    AI Generation Guide (English)
    - How to use Gemini / Copilot / Pika
    - How to copy prompts
    - How to generate images/videos
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("AI Generation Guide")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("AI Generation Guide")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28pt; font-weight: bold;")
        layout.addWidget(title)

        guide = QTextEdit()
        guide.setReadOnly(True)
        guide.setStyleSheet("font-size: 16pt;")
        guide.setText(self._build_guide_text())
        layout.addWidget(guide)

        btn_back = QPushButton("Back")
        btn_back.setStyleSheet("font-size: 20pt; padding: 10px;")
        btn_back.clicked.connect(self.on_back)
        layout.addWidget(btn_back)

    # ---------------------------------------------------------
    def _build_guide_text(self):
        return (
            "■ How to Generate Images / Videos\n"
            "\n"
            "1. Open Gemini, Copilot, or Pika using the buttons.\n"
            "2. Copy the English Prompt from the prompt list.\n"
            "3. Paste it into the AI tool.\n"
            "4. Adjust style, lighting, or camera angle if needed.\n"
            "\n"
            "■ Recommended Tools\n"
            "• Gemini: Best for detailed illustrations.\n"
            "• Copilot: Stable and consistent image generation.\n"
            "• Pika: Best for video generation.\n"
            "\n"
            "■ Tips\n"
            "• Use high-quality prompts.\n"
            "• Add camera angle (e.g., 'front view', 'side view').\n"
            "• Add lighting (e.g., 'soft lighting', 'studio light').\n"
            "• Add background (e.g., 'clean background').\n"
            "\n"
            "■ About Prompts\n"
            "Prompts are automatically generated based on your pet profile.\n"
            "You can edit the pet profile anytime from the Edit Menu.\n"
        )

    # ---------------------------------------------------------
    def on_back(self):
        self.close()
        self.controller.show_stepAllPromptsView()
