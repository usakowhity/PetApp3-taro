# controller.py (Final English Edition for PetApp3 Taro)

import os
import json
import webbrowser

from PySide6.QtCore import QObject, Signal

# Breed dictionary (English)
from data.breeds_en import (
    DOG_BREEDS,
    CAT_BREEDS,
    RABBIT_BREEDS,
    BREED_DICT_EN,
)

# State metadata
from data.states_en import STATE_META_EN, STATE_LIST
from data.states_alias_en import STATE_ALIAS_EN


class Controller(QObject):
    voice_signal = Signal(str)

    def __init__(self, BASE_DIR):
        super().__init__()
        self.BASE_DIR = BASE_DIR

        # Breed dictionary for StepB2
        self.BREED_DICT_BY_SPECIES = {
            "dog": DOG_BREEDS,
            "cat": CAT_BREEDS,
            "rabbit": RABBIT_BREEDS,
        }

        # Directories
        self.generated_dir = os.path.join(BASE_DIR, "generated")
        self.assets_dir = os.path.join(BASE_DIR, "assets")
        self.profile_path = os.path.join(BASE_DIR, "pet_profile.json")

        # Load profile
        self.pet_profile = self.load_profile()

        # Media dictionary
        self.media = {}
        self.scan_generated_folder()

        # Flags
        self.is_playing = False

    # ---------------------------------------------------------
    # Profile
    # ---------------------------------------------------------
    def load_profile(self):
        if not os.path.exists(self.profile_path):
            return {
                "species": "",
                "breed": "",
                "name": "",
                "gender": "",
                "age": "",
                "color": "",
                "fur_length": "",
                "ear": "",
                "tail": "",
                "pattern": "",
                "memo": "",
                "magic_word": "",
                "magic_action_free": "",
                "color_free": "",
                "ear_free": "",
                "tail_free": "",
                "pattern_free": ""
            }

        try:
            with open(self.profile_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print("[Controller] pet_profile loaded:", data)
                return data
        except Exception as e:
            print("[Controller] load_profile error:", e)
            return {}

    def save_profile(self):
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(self.pet_profile, f, ensure_ascii=False, indent=2)
            print("[Controller] pet_profile saved:", self.pet_profile)
        except Exception as e:
            print("[Controller] save_profile error:", e)

    # ---------------------------------------------------------
    # Media
    # ---------------------------------------------------------
    def scan_generated_folder(self):
        self.media = {}
        if not os.path.exists(self.generated_dir):
            return

        for fname in os.listdir(self.generated_dir):
            name, ext = os.path.splitext(fname)
            if ext.lower() in (".png", ".jpg", ".jpeg", ".mp4"):
                self.media[name] = os.path.join(self.generated_dir, fname)

        print("[Controller] generated folder scanned:", self.media)

    # ---------------------------------------------------------
    # UI Navigation
    # ---------------------------------------------------------

    def prepare_voice_commands(self):
        """
        PetApp2 互換のダミー関数。
        StepB2BreedWindow が呼び出すため、空でも必ず存在させる。
        PetApp3 では STATE_ALIAS_EN により音声コマンドは自動処理される。
        """
        print("[Controller] prepare_voice_commands (dummy) called")

    def show_welcome(self):
        from ui.welcome_window_en import WelcomeWindow
        self.win = WelcomeWindow(self)
        self.win.show()
        print("[Controller] WelcomeWindow started")

    def show_stepEditMenu(self):
        from ui.step_edit_menu_en import StepEditMenu
        self.win = StepEditMenu(self)
        self.win.show()
        print("[Controller] StepEditMenu started")

    def show_stepB2(self):
        from ui.stepB2_breed_en import StepB2BreedWindow
        self.win = StepB2BreedWindow(self)
        self.win.show()
        print("★★ StepB2BreedWindow (EN) started ★★")

    def show_stepMediaView(self):
        from ui.step_media_view_en import StepMediaView
        self.win = StepMediaView(self)
        self.win.show()

    def show_stepAllPromptsView(self):
        from ui.step_all_prompts_view_en import StepAllPromptsView
        self.win = StepAllPromptsView(self)
        self.win.show()
        print("[Controller] StepAllPromptsView started")

    def show_play(self):
        from ui.play_window_en import PlayWindow
        self.win = PlayWindow(self)
        self.win.show()
        print("[Controller] PlayWindow started")

    # ---------------------------------------------------------
    # Extra UI helpers
    # ---------------------------------------------------------
    def open_url(self, url: str):
        try:
            webbrowser.open(url)
        except Exception as e:
            print("[Controller] open_url error:", e)

    def show_stepAIGuideForMedia(self):
        from ui.step_ai_guide_en import StepAIGuideEn
        self.win = StepAIGuideEn(self)
        self.win.show()
        print("[Controller] StepAIGuideForMedia started")


    # ---------------------------------------------------------
    # Whisper Listener
    # ---------------------------------------------------------
    def start_voice_listener(self):
        try:
            from voice.whisper_listener import WhisperListener
            self.whisper = WhisperListener(self)
            self.whisper.start()
        except Exception as e:
            print("[Controller] WhisperListener start error:", e)

    def on_voice_detected(self, text):
        text = text.lower().strip()
        for key, state in STATE_ALIAS_EN.items():
            if key in text:
                self.voice_signal.emit(state)
                return

    # ---------------------------------------------------------
    # Face Detector
    # ---------------------------------------------------------
    def start_face_detector(self):
        try:
            from voice.face_detector import FaceDetector
            self.face = FaceDetector(self)
            self.face.start()
        except Exception as e:
            print("[Controller] FaceDetector start error:", e)

    def on_face_detected(self):
        self.voice_signal.emit("p1")

    # ---------------------------------------------------------
    # Prompt Generation
    # ---------------------------------------------------------
    def generate_all_prompts(self):
        prompts_dir = os.path.join(self.generated_dir, "prompts")
        os.makedirs(prompts_dir, exist_ok=True)

        for state in STATE_LIST:
            text = self.build_prompt_for_state(state)
            path = os.path.join(prompts_dir, f"{state}.txt")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                print("[Controller] Prompt saved:", path)
            except Exception as e:
                print("[Controller] Prompt save error:", state, e)

        print("[Controller] All prompts generated.")

    # ---------------------------------------------------------
    # Prompt Builder
    # ---------------------------------------------------------
    def build_prompt_for_state(self, state: str) -> str:
        p = self.pet_profile

        name = p.get("name", "this pet")
        species = p.get("species", "").lower()
        breed = p.get("breed", "")
        color = p.get("color", "")
        color_free = p.get("color_free", "")
        fur = p.get("fur_length", "")
        ear = p.get("ear", "")
        ear_free = p.get("ear_free", "")
        tail = p.get("tail", "")
        tail_free = p.get("tail_free", "")
        pattern = p.get("pattern", "")
        pattern_free = p.get("pattern_free", "")
        memo = p.get("memo", "")

        breed_en = BREED_DICT_EN.get(breed, breed)

        if breed_en:
            intro = f"A detailed, high-quality illustration of a {breed_en} named {name}, "
        else:
            intro = f"A detailed, high-quality illustration of a {species} named {name}, "

        appearance = (
            f"with {fur.lower()} fur, {color.lower()} color, {pattern.lower()} pattern. "
        )
        if color_free: appearance += f"{color_free} "
        if ear_free: appearance += f"{ear_free} "
        if tail_free: appearance += f"{tail_free} "
        if pattern_free: appearance += f"{pattern_free} "
        if memo: appearance += f"{memo} "

        meta = STATE_META_EN.get(state, {})
        base_desc = meta.get("description", "")

        if state == "p12":
            affection = p.get("magic_word", "")
            action = p.get("magic_action_free", "")
            return (
                f"{intro}"
                f"showing a special gesture in response to the owner's affection word '{affection}'. "
                f"{action} "
                f"{appearance}"
                "Natural colors, soft lighting, cute and expressive, clean background."
            )

        if state == "p2":
            if species == "dog":
                detail = meta.get("description_dog", base_desc)
            elif species == "cat":
                detail = meta.get("description_cat", base_desc)
            elif species == "rabbit":
                detail = meta.get("description_rabbit", base_desc)
            else:
                detail = base_desc

            return (
                f"{intro}"
                f"showing joyful behavior: {detail}. "
                f"{appearance}"
                "Natural colors, soft lighting, cute and expressive, clean background."
            )

        return (
            f"{intro}"
            f"showing the following state: {base_desc}. "
            f"{appearance}"
            "Natural colors, soft lighting, cute and expressive, clean background."
        )

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------
    def stop_all(self):
        try:
            if hasattr(self, "whisper"):
                self.whisper.stop()
        except Exception:
            pass

        try:
            if hasattr(self, "face"):
                self.face.stop()
        except Exception:
            pass


# ---------------------------------------------------------
# Main entry
# ---------------------------------------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    c = Controller(BASE_DIR)
    c.show_welcome()
