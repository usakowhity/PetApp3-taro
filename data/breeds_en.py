# breeds_en.py
# English breed list for PetApp3-portable

# -------------------------
# Dog breeds
# -------------------------
DOG_BREEDS = [
    "Mixed breed dog",

    "Shiba Inu", "Akita Inu",
    "Labrador Retriever", "Golden Retriever", "German Shepherd",
    "Poodle", "French Bulldog", "Bulldog", "Beagle",
    "Chihuahua", "Pomeranian", "Yorkshire Terrier", "Maltese",
    "Siberian Husky", "Border Collie", "Australian Shepherd",
    "Corgi", "Dachshund", "Rottweiler", "Doberman",
    "Great Dane", "Boxer", "Shih Tzu", "Papillon",
    "Cavalier King Charles Spaniel", "Boston Terrier",
    "Bichon Frise", "Havanese", "Samoyed",
    "Bernese Mountain Dog", "Newfoundland", "Saint Bernard",
    "Greyhound", "Whippet", "Basenji",
    "Jack Russell Terrier", "Fox Terrier", "Bull Terrier",
    "Miniature Schnauzer", "Giant Schnauzer",
    "English Springer Spaniel", "Cocker Spaniel",
    "Weimaraner", "Vizsla", "Pointer",
    "Irish Setter", "English Setter",
    "Alaskan Malamute", "American Eskimo Dog",
    "Sheltie (Shetland Sheepdog)", "Collie",
    "Pit Bull Terrier", "American Staffordshire Terrier",
    "Staffordshire Bull Terrier",
    "Keeshond", "Shar Pei", "Chow Chow",
    "Lhasa Apso", "Tibetan Spaniel", "Tibetan Terrier",
    "Pekingese", "Japanese Chin",
    "Saluki", "Afghan Hound", "Borzoi",
    "Rhodesian Ridgeback", "Pharaoh Hound",
    "Belgian Malinois", "Belgian Tervuren",
    "Anatolian Shepherd", "Great Pyrenees",
    "Akbash", "Kuvasz"
]

# -------------------------
# Cat breeds
# -------------------------
CAT_BREEDS = [
    "Mixed breed cat",

    "Siamese", "Persian", "Maine Coon",
    "British Shorthair", "American Shorthair",
    "Scottish Fold", "Ragdoll", "Bengal",
    "Sphynx", "Russian Blue", "Norwegian Forest Cat",
    "Abyssinian", "Birman", "Himalayan",
    "Savannah", "Oriental Shorthair",
    "Turkish Angora", "Turkish Van",
    "Manx", "Bombay", "Tonkinese",
    "Chartreux", "Egyptian Mau",
    "Devon Rex", "Cornish Rex",
    "American Curl", "Japanese Bobtail",
    "Singapura", "Selkirk Rex",
    "British Longhair", "American Bobtail",
    "Pixie-bob", "Nebelung", "LaPerm",
    "Munchkin", "Foldex", "Highlander"
]

# -------------------------
# Rabbit breeds
# -------------------------
RABBIT_BREEDS = [
    "Mixed breed rabbit",

    "Netherland Dwarf", "Holland Lop", "Mini Lop",
    "Mini Rex", "Standard Rex",
    "Lionhead", "Flemish Giant",
    "English Angora", "French Angora",
    "American Fuzzy Lop", "Harlequin",
    "Dutch", "Polish", "Havana",
    "Silver Fox", "Champagne d'Argent",
    "English Spot", "Californian",
    "New Zealand", "Mini Satin",
    "Jersey Wooly", "Tan", "Checkered Giant"
]

# -------------------------
# Breed dictionary (English → English)
# -------------------------
BREED_DICT_EN = {}

# Populate dictionary
for b in DOG_BREEDS + CAT_BREEDS + RABBIT_BREEDS:
    BREED_DICT_EN[b] = b
