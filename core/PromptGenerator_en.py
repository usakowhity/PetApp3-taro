from dataclasses import dataclass
from typing import Optional, Dict


# ---- Constants ----------------------------------------------------------------

STATE_NAME_EN: Dict[str, str] = {
    "n1": "Normal",
    "n2": "Sit",
    "n3": "Sleep",

    "p1": "Play",
    "p2": "Joy",
    "p3": "Down",
    "p4": "Paw",
    "p5": "Meal",
    "p6": "Water",
    "p7": "Toilet",
    "p8": "Fetch",
    "p9": "House",
    "p10": "Stand",
    "p11": "Bath",

    "p12": "Affection",
}

# One-sentence behaviors for static image prompts (n1–n3, p1, p3–p11)
STATIC_BEHAVIORS: Dict[str, str] = {
    "n1": "looks at me calmly with a relaxed expression",
    "n2": "sits still in front of me, waiting quietly",
    "n3": "lies down and rests peacefully near me",

    "p1": "looks at me with playful energy, inviting me to interact",
    "p3": "lies down in front of me as if following a 'down' command",
    "p4": "raises one paw toward me as if giving me a paw",
    "p5": "eats its food while occasionally glancing up at me",
    "p6": "drinks water while staying close to me",
    "p7": "uses its toilet area while occasionally looking toward me",
    "p8": "holds a toy or ball in its mouth as if bringing it back to me",
    "p9": "stays inside its house or bed while looking toward me",
    "p10": "stands up on its hind legs as if responding to my command",
    "p11": "is being washed or brushed while looking at me calmly",
}

# p2 is species-specific
P2_BEHAVIORS: Dict[str, str] = {
    "dog": (
        "runs toward me happily, wagging its tail energetically, "
        "with its ears slightly back and eyes softened, "
        "as if it is about to jump up to greet me"
    ),
    "cat": (
        "narrows its eyes happily and raises its tail, "
        "gently rubbing its head against me to show affection"
    ),
    "rabbit": (
        "performs a joyful binky near me, twisting its body slightly "
        "in the air with excitement"
    ),
}

# Default affectionate gesture for p12 (Usako-based)
DEFAULT_GESTURE_P12: str = (
    "stands up against my chest and lovingly licks my chin"
)


# ---- Data model ----------------------------------------------------------------

@dataclass
class PromptContext:
    state_code: str          # e.g. "n1", "p2", "p12"
    species: str             # "dog", "cat", "rabbit"
    appearance: str          # user description
    gesture_p12: Optional[str] = None  # optional, for p12 only


# ---- Prompt generator ----------------------------------------------------------

class PromptGeneratorEn:
    """
    English prompt generator for PetApp3.
    - Does NOT modify state definitions.
    - Uses first-person perspective (my / me) consistently.
    """

    def __init__(self) -> None:
        pass

    def generate(self, ctx: PromptContext) -> str:
        state = ctx.state_code

        if state == "p12":
            return self._build_p12_video_prompt(
                species=ctx.species,
                appearance=ctx.appearance,
                gesture=ctx.gesture_p12 or DEFAULT_GESTURE_P12,
            )

        if state == "p2":
            return self._build_p2_species_prompt(
                species=ctx.species,
                appearance=ctx.appearance,
            )

        # All other states: static image prompt
        return self._build_static_prompt(
            state_code=state,
            species=ctx.species,
            appearance=ctx.appearance,
        )

    # ---- Builders --------------------------------------------------------------

    def _normalize_species(self, species: str) -> str:
        s = species.strip().lower()
        if s in ("dog", "cat", "rabbit"):
            return s
        # Fallback: use as-is (for future expansion)
        return s

    def _build_static_prompt(
        self,
        state_code: str,
        species: str,
        appearance: str,
    ) -> str:
        behavior = STATIC_BEHAVIORS.get(
            state_code,
            "looks at me calmly with a neutral expression",
        )
        species_norm = self._normalize_species(species)

        prompt = f"""
Create a realistic image of a {species_norm}.
The pet has the following appearance: {appearance}.
It {behavior}.
The background should be simple with soft natural light.
""".strip()
        return prompt

    def _build_p2_species_prompt(
        self,
        species: str,
        appearance: str,
    ) -> str:
        species_norm = self._normalize_species(species)
        behavior = P2_BEHAVIORS.get(
            species_norm,
            "shows joyful behavior toward me with an affectionate expression",
        )

        prompt = f"""
Create a realistic image of a {species_norm} showing joyful praise behavior.
The pet has the following appearance: {appearance}.
It {behavior}.
The background should be simple with soft natural light.
""".strip()
        return prompt

    def _build_p12_video_prompt(
        self,
        species: str,
        appearance: str,
        gesture: str,
    ) -> str:
        species_norm = self._normalize_species(species)

        prompt = f"""
Create a short, heartwarming video of a {species_norm}.
The pet has the following appearance: {appearance}.

Scene:
The pet reacts with deep affection after receiving loving words from me.
It performs the following affectionate gesture: {gesture}.
The movement should feel natural, gentle, and emotionally expressive.

Environment:
A cozy indoor setting with soft natural light.

Mood:
Tender, emotional, heartwarming.

Camera:
Close-up or medium shot, smooth motion, eye-level.

Length:
3–5 seconds.
""".strip()
        return prompt


# ---- Example usage (for reference / testing) -----------------------------------
if __name__ == "__main__":
    gen = PromptGeneratorEn()

    ctx_static = PromptContext(
        state_code="n1",
        species="dog",
        appearance="a small mixed-breed dog with soft brown fur",
    )
    print("=== n1 example ===")
    print(gen.generate(ctx_static))
    print()

    ctx_p2_dog = PromptContext(
        state_code="p2",
        species="dog",
        appearance="a cheerful medium-sized dog with fluffy white fur",
    )
    print("=== p2 dog example ===")
    print(gen.generate(ctx_p2_dog))
    print()

    ctx_p12 = PromptContext(
        state_code="p12",
        species="rabbit",
        appearance="a gentle white rabbit with long ears and soft fur",
        gesture_p12=None,  # will use DEFAULT_GESTURE_P12
    )
    print("=== p12 example ===")
    print(gen.generate(ctx_p12))
