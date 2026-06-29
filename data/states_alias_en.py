# states_alias_en.py
# English voice command → state mapping for PetApp3 Taro

STATE_ALIAS_EN = {
    # Neutral states
    "normal": "n1",
    "idle": "n1",

    "sit": "n2",
    "wait": "n2",

    "sleep": "n3",
    "go to sleep": "n3",
    "lie down": "n3",

    # Positive states
    "play": "p1",
    "let's play": "p1",
    "come here": "p1",

    "good boy": "p2",
    "good girl": "p2",
    "happy": "p2",
    "joy": "p2",

    "down": "p3",

    "paw": "p4",
    "shake": "p4",
    "hand": "p4",

    "meal": "p5",
    "food": "p5",
    "hungry": "p5",
    "eat": "p5",

    "water": "p6",
    "drink": "p6",
    "thirsty": "p6",

    "toilet": "p7",
    "bathroom": "p7",
    "pee": "p7",
    "poop": "p7",

    "fetch": "p8",
    "bring it": "p8",
    "get the ball": "p8",

    "house": "p9",
    "go home": "p9",
    "your house": "p9",

    "stand": "p10",
    "stand up": "p10",

    "bath": "p11",
    "groom": "p11",
    "brush": "p11",

    # Special affection state (p12)
    # The actual affection word is dynamic, but we include common patterns
    "i love you": "p12",
    "love you": "p12",
    "miss you": "p12",
    "i missed you": "p12",
}
