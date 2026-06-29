# play/play_manager_en.py

import os
from pathlib import Path
os.environ["IMAGEIO_FFMPEG_EXE"] = str(Path(__file__).resolve().parent.parent / "ffmpeg" / "ffmpeg.exe")

from moviepy.editor import VideoFileClip
import pygame
import sys
import json
import time
import datetime


class PlayManager:
    """
    PlayManager (English Edition)

    - Plays images (png/jpg) and videos (mp4) for each state code
    - Monitors WhisperListener → latest_voice_command for state transitions
    """

    def __init__(self, controller):
        pygame.init()

        self.controller = controller  # WhisperListener lives here

        # Window
        self.screen_size = (600, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("PetApp3 - Play Mode (English Edition)")

        # Load state definitions, aliases, and pet info
        self.states = self.load_states()
        self.alias = self.load_alias()
        self.pet_info = self.load_pet_info()
        self.magic_word = self.pet_info.get("magic_word", None)

        # Initial state is always n1
        self.current_state = "n1"

        # Video playback
        self.current_clip = None
        self.current_clip_iter = None
        self.video_end_callback = None

        # Timers
        self.last_stimulus_time = time.time()
        self.smile_cooldown_until = 0.0

        # First playback
        self.play_media_for_state(self.current_state)

    # ============================================================
    # Load external JSON
    # ============================================================
    def load_states(self):
        path = Path("data/states.json")
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def load_alias(self):
        path = Path("data/states_alias.json")
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("states", {})
        return {}

    def load_pet_info(self):
        path = Path("data/pet_info.json")
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"name": "Unknown", "species": "Unknown"}

    # ============================================================
    # p1 / p12 fallback logic
    # ============================================================
    def resolve_play_state(self, state_code: str):
        """
        If p1 or p12 has no media, fallback to p2 (same as PetApp2).
        """
        if self.get_media_path(state_code):
            return state_code

        if state_code in ("p1", "p12"):
            if self.get_media_path("p2"):
                return "p2"

        return None

    # ============================================================
    # State transition
    # ============================================================
    def change_state(self, new_state: str):
        resolved = self.resolve_play_state(new_state)
        if not resolved:
            print(f"[WARN] No media found for state {new_state}")
            return

        print(f"[STATE] {self.current_state} → {resolved}")
        self.current_state = resolved
        self.play_media_for_state(resolved)
        self.last_stimulus_time = time.time()

    # ============================================================
    # Find media in generated/
    # ============================================================
    def get_media_path(self, state_code: str):
        base = os.path.join("generated", state_code)

        if os.path.exists(base + ".mp4"):
            return base + ".mp4"

        for ext in [".png", ".jpg", ".jpeg"]:
            path = base + ext
            if os.path.exists(path):
                return path

        return None

    # ============================================================
    # Media playback
    # ============================================================
    def play_media_for_state(self, state_code: str):
        path = self.get_media_path(state_code)
        if not path:
            print(f"[WARN] Media not found for {state_code}")
            return

        self.current_clip = None
        self.current_clip_iter = None
        self.video_end_callback = None

        if path.endswith(".mp4"):
            self.play_video(path)
        else:
            self.play_image(path)

    # ============================================================
    # Image playback
    # ============================================================
    def play_image(self, path: str):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, self.screen_size)

        self.screen.fill((0, 0, 0))
        self.screen.blit(img, (0, 0))
        pygame.display.update()

        # Non-n1 images return to n1 after 4 seconds
        if self.current_state != "n1":
            pygame.time.set_timer(pygame.USEREVENT + 1, 4000, loops=1)
            self.video_end_callback = self.return_to_n1

    # ============================================================
    # Video playback
    # ============================================================
    def play_video(self, path: str):
        print(f"[VIDEO] Playing: {path}")

        clip = VideoFileClip(path)
        clip = clip.resize(height=600)

        self.current_clip = clip
        self.current_clip_iter = clip.iter_frames(fps=clip.fps, dtype="uint8")

        # Non-n1 videos return to n1 after playback
        if self.current_state != "n1":
            self.video_end_callback = self.return_to_n1

    # ============================================================
    # Return to n1
    # ============================================================
    def return_to_n1(self):
        # Cooldown for p1/p2
        if self.current_state in ("p1", "p2"):
            self.smile_cooldown_until = time.time() + 3.0

        self.current_state = "n1"
        self.play_media_for_state("n1")
        self.last_stimulus_time = time.time()

    # ============================================================
    # Main loop (voice command enabled)
    # ============================================================
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            now = time.time()

            # WhisperListener → latest_voice_command
            if self.controller.latest_voice_command:
                cmd = self.controller.latest_voice_command
                self.controller.latest_voice_command = None

                print(f"[VOICE CMD] Received: {cmd}")
                self.change_state(cmd)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT + 1:
                    if self.video_end_callback:
                        cb = self.video_end_callback
                        self.video_end_callback = None
                        cb()

            # n1 → n3 after 15 seconds of no stimulus
            if self.current_state == "n1":
                if now - self.last_stimulus_time >= 15.0:
                    self.change_state("n3")
                    self.last_stimulus_time = now

            # Video playback loop
            if self.current_clip_iter:
                try:
                    frame = next(self.current_clip_iter)
                    surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                    self.screen.fill((0, 0, 0))
                    x = (600 - surf.get_width()) // 2
                    self.screen.blit(surf, (x, 0))
                    pygame.display.update()

                except StopIteration:
                    self.current_clip_iter = None
                    if self.video_end_callback:
                        cb = self.video_end_callback
                        self.video_end_callback = None
                        cb()

            clock.tick(60)

        pygame.quit()
