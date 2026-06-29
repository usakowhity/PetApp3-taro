# voice/whisper_listener.py
# PetApp3 English Edition — WhisperTinyEngine Listener

import threading
import time
from PySide6.QtCore import QObject, Signal

from voice.whisper_tiny_engine import WhisperTinyEngine


class WhisperBridge(QObject):
    """
    Bridge to safely send recognized text to the UI thread
    """
    voice_signal = Signal(str)


class WhisperListener(threading.Thread):
    """
    WhisperTinyEngine listener (English version, thread-safe)
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.running = True

        # ★ Whisper engine is created internally (no external engine argument)
        self.engine = WhisperTinyEngine()

        # Bridge to UI thread
        self.bridge = WhisperBridge()
        self.bridge.voice_signal.connect(self.controller.on_voice_detected)

        self.daemon = True

    # ---------------------------------------------------------
    def run(self):
        print("[WhisperListener] Thread started")

        while self.running:
            # ★ Blocking English speech recognition
            text = self.engine.listen_blocking()

            if text:
                print("[WhisperListener] recognized:", text)
                # Send raw text to controller
                self.bridge.voice_signal.emit(text)

            time.sleep(0.05)

        print("[WhisperListener] Thread ended")

    # ---------------------------------------------------------
    def stop(self):
        self.running = False
        print("[WhisperListener] Stop requested")

