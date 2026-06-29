# voice/whisper_tiny_engine.py
# PetApp3 English Edition — WhisperTinyEngine

import pyaudio
import numpy as np
import importlib

whisper = importlib.import_module("whisper")


class WhisperTinyEngine:
    """
    Simple blocking Whisper tiny engine for English speech recognition.
    """

    def __init__(self, device_index=None, rate=16000, chunk=16000):
        """
        chunk=16000 → 1秒録音
        """
        self.rate = rate
        self.chunk = chunk

        # Load Whisper tiny model
        self.model = whisper.load_model("tiny")

        # PyAudio
        self.pa = pyaudio.PyAudio()

        # Auto-select device
        if device_index is None:
            try:
                device_index = self.pa.get_default_input_device_info().get("index", 0)
                print("[WhisperTiny] Using default input device:", device_index)
            except Exception as e:
                print("[WhisperTiny] Could not get default device:", e)
                device_index = 0

        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=device_index
        )

    # ---------------------------------------------------------
    # Blocking 1-second recording
    # ---------------------------------------------------------
    def listen_blocking(self):
        """
        Record 1 second of audio and return recognized English text.
        """
        try:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
        except Exception as e:
            print("[WhisperTiny] read error:", e)
            return ""

        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

        # Silence filter (English speech is louder)
        if np.abs(audio).mean() < 0.0012:
            return ""

        return self.transcribe(audio)

    # ---------------------------------------------------------
    # Whisper transcription (English)
    # ---------------------------------------------------------
    def transcribe(self, audio):
        try:
            result = self.model.transcribe(
                audio,
                fp16=False,
                language="en",          # ★ 英語版
                temperature=0.2,
                no_speech_threshold=0.5,
                condition_on_previous_text=False
            )
            return result.get("text", "").strip()
        except Exception as e:
            print("[WhisperTiny] transcribe error:", e)
            return ""

