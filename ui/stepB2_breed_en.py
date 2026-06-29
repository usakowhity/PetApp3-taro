from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt


class StepB2BreedWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.profile = self.controller.pet_profile

        self.setWindowTitle("Edit Pet Profile")
        self.setMinimumSize(900, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll.setWidget(container)
        form = QVBoxLayout(container)
        form.setSpacing(8)

        def add_labeled_row(label_text, widget):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 18pt;")
            row.addWidget(lbl, 1)
            row.addWidget(widget, 3)
            form.addLayout(row)

        # Species (English)
        self.cmb_species = QComboBox()
        self.cmb_species.addItems(["", "Dog", "Cat", "Rabbit"])
        self.cmb_species.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Species:", self.cmb_species)

        # Breed (English)
        self.cmb_breed = QComboBox()
        self.cmb_breed.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Breed:", self.cmb_breed)

        # Name
        self.txt_name = QLineEdit()
        self.txt_name.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Name:", self.txt_name)

        # Gender
        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(["", "Male", "Female"])
        self.cmb_gender.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Gender:", self.cmb_gender)

        # Age
        self.txt_age = QLineEdit()
        self.txt_age.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Age:", self.txt_age)

        # Color
        self.cmb_color = QComboBox()
        self.cmb_color.addItems(["", "White", "Black", "Brown", "Gray", "Other"])
        self.cmb_color.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Color:", self.cmb_color)

        self.txt_color_free = QLineEdit()
        self.txt_color_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Color (free text):", self.txt_color_free)

        # Fur length
        self.cmb_fur = QComboBox()
        self.cmb_fur.addItems(["", "Short", "Medium", "Long"])
        self.cmb_fur.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Fur length:", self.cmb_fur)

        # Ear
        self.cmb_ear = QComboBox()
        self.cmb_ear.addItems(["", "Upright", "Droopy", "Other"])
        self.cmb_ear.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Ear shape:", self.cmb_ear)

        self.txt_ear_free = QLineEdit()
        self.txt_ear_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Ear (free text):", self.txt_ear_free)

        # Tail
        self.cmb_tail = QComboBox()
        self.cmb_tail.addItems(["", "Short", "Long", "Round", "Curled", "Other"])
        self.cmb_tail.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Tail:", self.cmb_tail)

        self.txt_tail_free = QLineEdit()
        self.txt_tail_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Tail (free text):", self.txt_tail_free)

        # Pattern
        self.cmb_pattern = QComboBox()
        self.cmb_pattern.addItems(["", "Solid", "Spotted", "Striped", "Color-tipped", "Other"])
        self.cmb_pattern.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Pattern:", self.cmb_pattern)

        self.txt_pattern_free = QLineEdit()
        self.txt_pattern_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Pattern (free text):", self.txt_pattern_free)

        # Memo
        lbl_memo = QLabel("Memo:")
        lbl_memo.setStyleSheet("font-size: 22pt; font-weight: bold;")
        form.addWidget(lbl_memo)

        self.txt_memo = QTextEdit()
        self.txt_memo.setStyleSheet("font-size: 22pt;")
        form.addWidget(self.txt_memo)

        # Affection Word
        self.txt_affection_word = QLineEdit()
        self.txt_affection_word.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("Affection Word:", self.txt_affection_word)

        # Affection Action
        lbl_affection_action = QLabel("Gesture when reacting to Affection Word:")
        lbl_affection_action.setStyleSheet("font-size: 22pt; font-weight: bold;")
        form.addWidget(lbl_affection_action)

        self.txt_affection_action = QTextEdit()
        self.txt_affection_action.setStyleSheet("font-size: 22pt;")
        form.addWidget(self.txt_affection_action)

        main_layout.addWidget(scroll)

        # Buttons
        btn_row = QHBoxLayout()
        btn_back = QPushButton("Back to Welcome")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_back.clicked.connect(self.on_back)
        btn_row.addWidget(btn_back)

        btn_save = QPushButton("Save and Generate Prompts")
        btn_save.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_save.clicked.connect(self.save_and_next)
        btn_row.addWidget(btn_save)

        main_layout.addLayout(btn_row)

        # Connect species change
        self.cmb_species.currentTextChanged.connect(self.on_species_changed)

        # Load profile
        self.load_profile_to_ui()

        # Initialize breed list
        self.on_species_changed(self.cmb_species.currentText())

    # =========================================================
    # Load profile into UI
    # =========================================================
    def load_profile_to_ui(self):
        p = self.profile

        self.cmb_species.setCurrentText(p.get("species", ""))

        self.txt_name.setText(p.get("name", ""))
        self.cmb_gender.setCurrentText(p.get("gender", ""))
        self.txt_age.setText(p.get("age", ""))

        self.cmb_color.setCurrentText(p.get("color", ""))
        self.txt_color_free.setText(p.get("color_free", ""))

        self.cmb_fur.setCurrentText(p.get("fur_length", ""))

        self.cmb_ear.setCurrentText(p.get("ear", ""))
        self.txt_ear_free.setText(p.get("ear_free", ""))

        self.cmb_tail.setCurrentText(p.get("tail", ""))
        self.txt_tail_free.setText(p.get("tail_free", ""))

        self.cmb_pattern.setCurrentText(p.get("pattern", ""))
        self.txt_pattern_free.setText(p.get("pattern_free", ""))

        self.txt_memo.setPlainText(p.get("memo", ""))

        self.txt_affection_word.setText(p.get("magic_word", ""))
        self.txt_affection_action.setPlainText(p.get("magic_action_free", ""))

        breed = p.get("breed", "")
        self._restore_breed_after_species = breed

    # =========================================================
    # Species changed → update breed list
    # =========================================================
    def on_species_changed(self, species):
        breeds = self.controller.BREED_DICT_BY_SPECIES.get(species.lower(), [])
        current = getattr(self, "_restore_breed_after_species", "")

        self.cmb_breed.clear()
        self.cmb_breed.addItem("")

        added = set()
        if current:
            self.cmb_breed.addItem(current)
            added.add(current)

        for b in breeds:
            if b not in added:
                self.cmb_breed.addItem(b)
                added.add(b)

        if current:
            self.cmb_breed.setCurrentText(current)

        self._restore_breed_after_species = ""

    # =========================================================
    # Save profile
    # =========================================================
    def save_and_next(self):
        p = self.profile

        p["species"] = self.cmb_species.currentText().strip()
        new_breed = self.cmb_breed.currentText().strip()
        if new_breed:
            p["breed"] = new_breed

        p["name"] = self.txt_name.text().strip()
        p["gender"] = self.cmb_gender.currentText().strip()
        p["age"] = self.txt_age.text().strip()

        p["color"] = self.cmb_color.currentText().strip()
        p["color_free"] = self.txt_color_free.text().strip()

        p["fur_length"] = self.cmb_fur.currentText().strip()

        p["ear"] = self.cmb_ear.currentText().strip()
        p["ear_free"] = self.txt_ear_free.text().strip()

        p["tail"] = self.cmb_tail.currentText().strip()
        p["tail_free"] = self.txt_tail_free.text().strip()

        p["pattern"] = self.cmb_pattern.currentText().strip()
        p["pattern_free"] = self.txt_pattern_free.text().strip()

        p["memo"] = self.txt_memo.toPlainText().strip()

        # Affection Word
        p["magic_word"] = self.txt_affection_word.text().strip()
        p["magic_action_free"] = self.txt_affection_action.toPlainText().strip()

        self.controller.pet_profile = p
        self.controller.save_profile()
        self.controller.prepare_voice_commands()
        self.controller.generate_all_prompts()

        self.close()
        self.controller.show_stepAllPromptsView()

    # =========================================================
    # Back
    # =========================================================
    def on_back(self):
        self.close()
        self.controller.show_welcome()
