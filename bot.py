import random

# Danh sách từ vựng tiếng Anh cho comment
comment_nouns = [
    "photo", "video", "post", "article", "picture", "music", "voice", "smile", "friend", "family",
    "cat", "dog", "flower", "sea", "sky", "star", "sun", "moon", "dream", "love",
    "time", "work", "trip", "nature", "snow", "rain", "wind", "cherry", "summer", "winter",
    "comment", "question", "reply", "idea", "feeling", "emotion", "surprise", "laugh", "tear", "hope",
    "support", "thanks", "news", "info", "event", "game", "movie", "book", "food", "taste"
]
comment_adjectives = [
    "cute", "pretty", "funny", "fun", "happy", "awesome", "wonderful", "great", "lovely", "touching",
    "tasty", "cool", "kind", "strong", "fast", "beautiful", "favorite", "perfect", "amazing", "genius",
    "surprising", "excited", "joyful", "lonely", "nostalgic", "simple", "complex", "fresh", "rare", "normal",
    "energetic", "tired", "busy", "quiet", "noisy", "bright", "dark", "warm", "cool", "cold",
    "hot", "sweet", "spicy", "sour", "bitter", "soft", "hard", "light", "heavy", "quick"
]
comment_verbs = [
    "see", "hear", "read", "write", "say", "laugh", "cry", "surprise", "feel", "like",
    "support", "wait", "take", "use", "make", "eat", "drink", "play", "sing", "dance",
    "think", "know", "teach", "learn", "remember", "forget", "praise", "try", "enjoy", "start",
    "end", "continue", "change", "grow", "decrease", "send", "receive", "return", "call", "meet",
    "come", "go", "return", "sleep", "wake", "run", "fly", "swim", "draw", "feel"
]
particles_endings = [
    "", "it", "so", "too", "yeah", "wow", "please", "maybe", "ok", "now",
    "and", "or", "but", "for", "with", "at", "on", "in", "to", "up"
]
icons = [
    "😊", "😂", "😍", "😢", "😡", "😱", "😴", "😎", "🥳", "🤗",
    "😘", "😜", "😳", "😇", "🤓", "🥰", "😔", "😤", "😩", "🤔",
    "🌸", "🌹", "🌺", "🌻", "🌼", "🌷", "🍂", "🍁", "🌲", "🌳",
    "🌴", "🌵", "🌾", "🌿", "🍃", "🌊", "🏞️", "⛰️", "🌋", "🏝️",
    "☀️", "🌞", "🌤️", "⛅", "🌥️", "☁️", "🌧️", "⛈️", "🌩️", "⚡",
    "❄️", "☃️", "⛄", "🌬️", "💧", "🌈", "🌪️", "🌫️", "☔", "🌂",
    "🐱", "🐶", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮",
    "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🦅", "🦇", "🐺",
    "🐴", "🦄", "🐝", "🐞", "🦋", "🐌", "🐍", "🦎", "🐢", "🐙",
    "🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍒", "🍍", "🥭",
    "🍑", "🍐", "🥝", "🍅", "🥑", "🍔", "🍕", "🍟", "🌭", "🍜",
    "🍣", "🍤", "🍦", "🍰", "🎂", "🍪", "🍫", "☕", "🍵", "🥤",
    "📚", "✏️", "🖌️", "🎨", "🎧", "🎤", "🎸", "🎹", "🥁", "🎻",
    "📷", "📸", "🎥", "📺", "💻", "📱", "⌚", "⏰", "💡", "🔋",
    "🔧", "🔨", "⚙️", "✂️", "📦", "🎁", "🖼️", "🕯️", "🧸", "🎀",
    "🚗", "🚙", "🚌", "🚐", "🚚", "🚜", "🏍️", "🚲", "🛵", "✈️",
    "🚁", "🚤", "⛵", "🚢", "🚀", "🛸", "🚉", "🚃", "🚅", "🛤️",
    "❤️", "💛", "💚", "💙", "💜", "🖤", "🤍", "💔", "💖", "💞",
    "✨", "⭐", "🌟", "💫", "🔥", "💥", "🎉", "🎊", "🎈", "🎇",
    "💌", "✉️", "📩", "📞", "🔊", "🔇", "🔔", "🚨", "⏳", "⌛",
    "✅", "❌", "✔️", "✖️", "➡️", "⬅️", "⬆️", "⬇️", "🔄", "🔍"
]

# Hàm chọn ngẫu nhiên
def get_random_element(array):
    return random.choice(array)

# Hàm tạo comment ngẫu nhiên
def generate_random_comment():
    structures = [
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)}",
        f"{get_random_element(comment_adjectives)} {get_random_element(particles_endings)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_verbs)}",
        f"{get_random_element(comment_adjectives)} {get_random_element(particles_endings)}",
        f"{get_random_element(comment_verbs)} {get_random_element(particles_endings)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)} {get_random_element(comment_verbs)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)}",
        f"{get_random_element(comment_adjectives)} {get_random_element(comment_nouns)}",
        f"{get_random_element(comment_verbs)} {get_random_element(particles_endings)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)}{get_random_element(comment_adjectives)}"
    ]
    comment = get_random_element(structures)
    return comment

# Test hàm
if __name__ == "__main__":
    comment = generate_random_comment()
    print(f"{comment}")