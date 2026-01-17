SUBJECT_CONCEPTS = [
    "person", "man", "woman", "child",
    "group", "crowd",
    "animal", "dog", "cat", "bird",
    "nature", "tree", "flower", "mountain",
    "object", "car", "building", "food"
]

ENVIRONMENT_CONCEPTS = [
    "indoor", "outdoor",
    "city", "urban", "street",
    "beach", "forest", "mountain",
    "desert", "snow",
    "home", "office", "studio"
]

COMPOSITION_CONCEPTS = [
    "portrait",
    "close-up",
    "wide shot",
    "full body",
    "side view",
    "top view",
    "centered",
    "symmetry",
    "minimal"
]

PHOTOGRAPHY_TYPE_CONCEPTS = [
    "street photography",
    "landscape photography",
    "portrait photography",
    "fashion photography",
    "product photography",
    "food photography",
    "travel photography",
    "wildlife photography"
]

STYLE_CONCEPTS = [
    "cinematic",
    "vintage",
    "modern",
    "minimalist",
    "dramatic",
    "editorial",
    "documentary"
]

LIGHTING_CONCEPTS = [
    "natural light",
    "studio light",
    "low light",
    "backlit",
    "soft light",
    "hard light",
    "golden hour",
    "neon light"
]

COLOR_CONCEPTS = [
    "black and white",
    "monochrome",
    "warm tones",
    "cool tones",
    "pastel colors",
    "vibrant colors",
    "dark tones",
    "earth tones"
]

MOOD_CONCEPTS = [
    "calm",
    "moody",
    "happy",
    "dramatic",
    "serene",
    "mysterious",
    "energetic",
    "romantic"
]

ART_MEDIUM_CONCEPTS = [
    "photograph",
    "digital art",
    "illustration",
    "painting",
    "sketch",
    "3d render"
]

EXPANSION_POOL = list(set(
    SUBJECT_CONCEPTS +
    ENVIRONMENT_CONCEPTS +
    COMPOSITION_CONCEPTS +
    PHOTOGRAPHY_TYPE_CONCEPTS +
    STYLE_CONCEPTS +
    LIGHTING_CONCEPTS +
    COLOR_CONCEPTS +
    MOOD_CONCEPTS +
    ART_MEDIUM_CONCEPTS
))
