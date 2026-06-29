# states_en.py
# English state metadata for PetApp3 Taro

STATE_META_EN = {
    "n1": {
        "name": "Normal",
        "description": "The pet is in a normal idle state.",
        "category": "neutral",
        "thumbnail": "states/n1.png"
    },

    "n2": {
        "name": "Sit",
        "description": "The pet sits down in response to the owner's command such as 'sit' or 'wait'.",
        "category": "neutral",
        "thumbnail": "states/n2.png"
    },

    "n3": {
        "name": "Sleep",
        "description": "The pet lies down and rests or sleeps when tired or bored.",
        "category": "neutral",
        "thumbnail": "states/n3.png"
    },

    "p1": {
        "name": "Play",
        "description": "Active behavior such as playing, running, or walking.",
        "category": "positive",
        "thumbnail": "states/p1.png"
    },

    "p2": {
        "name": "Joy",
        "description": "Joyful behavior. Detailed actions vary depending on the species.",
        "description_dog": "The dog happily wags its tail, lowers its ears slightly, narrows its eyes, and hops lightly toward the owner as if about to jump with excitement.",
        "description_cat": "The cat narrows its eyes happily, raises its tail with a small twitch at the tip, and rubs its head and body affectionately against the owner.",
        "description_rabbit": "The rabbit shakes its head and ears with excitement and performs a big binky jump, twisting its body to express joy.",
        "category": "positive",
        "thumbnail": "states/p2.png"
    },

    "p3": {
        "name": "Down",
        "description": "The pet lies down in response to the owner's 'down' command.",
        "category": "positive",
        "thumbnail": "states/p3.png"
    },

    "p4": {
        "name": "Paw",
        "description": "The pet raises one paw and places it on the owner's hand in response to the 'paw' command.",
        "category": "positive",
        "thumbnail": "states/p4.png"
    },

    "p5": {
        "name": "Meal",
        "description": "Eating behavior or gestures related to wanting food.",
        "category": "positive",
        "thumbnail": "states/p5.png"
    },

    "p6": {
        "name": "Water",
        "description": "Drinking behavior or gestures related to wanting water.",
        "category": "positive",
        "thumbnail": "states/p6.png"
    },

    "p7": {
        "name": "Toilet",
        "description": "The pet sits or stays in the pet toilet.",
        "category": "positive",
        "thumbnail": "states/p7.png"
    },

    "p8": {
        "name": "Fetch",
        "description": "The pet brings back a ball or toy in response to the owner's 'fetch' command.",
        "category": "positive",
        "thumbnail": "states/p8.png"
    },

    "p9": {
        "name": "House",
        "description": "The pet enters or stays inside its house.",
        "category": "positive",
        "thumbnail": "states/p9.png"
    },

    "p10": {
        "name": "Stand",
        "description": "The pet stands up on its hind legs in response to the owner's command.",
        "category": "positive",
        "thumbnail": "states/p10.png"
    },

    "p11": {
        "name": "Bath",
        "description": "Bathing, grooming, or brushing behavior.",
        "category": "positive",
        "thumbnail": "states/p11.png"
    },

    "p12": {
        "name": "Affection",
        "description": "The pet reacts to the owner's custom affection word and shows a special gesture.",
        "description_dog": "The dog responds to the owner's affection word with a unique dog-like affectionate gesture (user-defined).",
        "description_cat": "The cat responds to the owner's affection word with a unique cat-like affectionate gesture (user-defined).",
        "description_rabbit": "The rabbit responds to the owner's affection word with a unique rabbit-like affectionate gesture (user-defined).",
        "category": "special",
        "thumbnail": "states/p12.png"
    }
}

# List of all states
STATE_LIST = list(STATE_META_EN.keys())
