# bot.py
import random

# Danh sách từ vựng mở rộng
adjectives = [
    "awesome", "cool", "great", "amazing", "fun", "super", "nice", "lovely",
    "fantastic", "perfect", "sweet", "happy", "epic", "brilliant", "fab",
    "stellar", "rad", "groovy", "neat", "vibrant", "dazzling", "snappy",
    "fresh", "lively", "bold", "crisp", "sleek", "sharp", "dynamic",
    "charming", "grand", "classy", "smooth"
]
nouns = [
    "video", "vibe", "dance", "content", "clip", "beat", "style", "energy",
    "move", "song", "art", "moment", "flow", "mood", "groove", "scene",
    "rhythm", "spark", "wave", "jam", "tune", "spirit", "flair", "pulse",
    "journey", "creation", "magic", "vlog", "trend", "blast", "show",
    "story", "craft", "passion"
]
verbs = [
    "love", "like", "enjoy", "dig", "feel", "rock", "shine", "slay",
    "keep", "make", "bring", "share", "spark", "nail", "crush",
    "groove", "vibe", "flow", "dance", "jam", "craft", "build", "push",
    "grow", "light", "kick", "roll", "spin", "blend", "lift",
    "inspire", "create", "drive"
]
intensifiers = [
    "so", "really", "totally", "pretty", "such", "very", "quite",
    "kinda", "mega", "uber", "truly", "mad", "pure", "extra", "",
    "fully", "super", "insanely", "wildly", ""
]
subjects = [
    "this", "your", "that", "the", ""
]
endings = [
    "it up", "going", "this", "that", "on", "it", "",
    "all day", "big time", "for real", "non stop", "like crazy",
    "with style", "so hard", "right now", "every day", ""
]

def generate_random_comment():
    # Nhiều cấu trúc câu để tăng tổ hợp
    structures = [
        lambda: f"{random.choice(subjects).capitalize()} {random.choice(nouns)} is {random.choice(intensifiers)} {random.choice(adjectives)} {random.choice(endings)}",
        lambda: f"{random.choice(verbs).capitalize()} {random.choice(intensifiers)} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(endings)}",
        lambda: f"{random.choice(adjectives).capitalize()} {random.choice(nouns)} {random.choice(verbs)} {random.choice(intensifiers)} {random.choice(endings)}",
        lambda: f"{random.choice(intensifiers).capitalize()} {random.choice(adjectives)} {random.choice(nouns)} is {random.choice(adjectives)} {random.choice(endings)}",
        lambda: f"{random.choice(verbs).capitalize()} this {random.choice(intensifiers)} {random.choice(adjectives)} {random.choice(nouns)}",
        lambda: f"{random.choice(adjectives).capitalize()} {random.choice(nouns)} {random.choice(endings)} {random.choice(adjectives)} {random.choice(endings)}",
        lambda: f"{random.choice(subjects).capitalize()} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(endings)}",
        lambda: f"{random.choice(intensifiers).capitalize()} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(endings)}",
        lambda: f"{random.choice(verbs).capitalize()} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(intensifiers)} {random.choice(endings)}",
        lambda: f"{random.choice(adjectives).capitalize()} {random.choice(nouns)} is {random.choice(verbs)} {random.choice(intensifiers)} {random.choice(adjectives)}"
    ]
    
    comment = random.choice(structures)()
    
    # Làm sạch: chỉ giữ chữ, số, dấu cách
    comment = "".join(c for c in comment if c.isalnum() or c.isspace())
    comment = " ".join(comment.split())  # Loại bỏ dấu cách thừa
    
    # Kiểm tra 5-8 từ
    words = comment.split()
    word_count = len(words)
    if word_count < 5 or word_count > 8:
        # Dự phòng: cấu trúc đơn giản
        comment = f"{random.choice(verbs).capitalize()} this {random.choice(intensifiers)} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(endings)}"
        comment = "".join(c for c in comment if c.isalnum() or c.isspace())
        comment = " ".join(comment.split())
    
    print(f"Đã tạo comment: {comment}")
    return comment

# Test hàm
if __name__ == "__main__":
    print("Bắt đầu test random comment...")
    unique_comments = set()
    for i in range(20):  # Test 20 comment
        comment = generate_random_comment()
        unique_comments.add(comment)
        print(f"Comment {i+1}: {comment}")
    print(f"Số comment duy nhất: {len(unique_comments)}")
    print("Kết thúc test.")