import random

# Danh sách từ vựng cho comment
comment_nouns = [
    "写真", "動画", "投稿", "記事", "絵", "音楽", "声", "笑顔", "友達", "家族",
    "猫", "犬", "花", "海", "空", "星", "太陽", "月", "夢", "愛",
    "時間", "仕事", "旅", "自然", "雪", "雨", "風", "桜", "夏", "冬",
    "コメント", "質問", "返事", "アイデア", "気持ち", "感動", "驚き", "笑い", "涙", "希望",
    "応援", "感謝", "お知らせ", "情報", "イベント", "ゲーム", "映画", "本", "料理", "味"
]
comment_adjectives = [
    "可愛い", "綺麗", "面白い", "楽しい", "嬉しい", "すごい", "素晴らしい", "最高", "素敵", "感動",
    "おいしい", "かっこいい", "優しい", "強い", "速い", "美しい", "大好き", "最高", "完璧", "天才",
    "びっくり", "驚く", "幸せ", "寂しい", "懐かしい", "シンプル", "複雑", "新鮮", "珍しい", "普通",
    "元気", "疲れる", "忙しい", "静か", "騒がしい", "明るい", "暗い", "暖かい", "涼しい", "寒い",
    "熱い", "甘い", "辛い", "酸っぱい", "苦い", "柔らかい", "硬い", "軽い", "重い", "早い"
]
comment_verbs = [
    "見る", "聞く", "読む", "書く", "言う", "笑う", "泣く", "驚く", "感動", "好き",
    "応援", "待つ", "撮る", "使う", "作る", "食べる", "飲む", "遊ぶ", "歌う", "踊る",
    "考える", "知る", "教える", "学ぶ", "覚える", "忘れる", "褒める", "頑張る", "楽しむ", "始める",
    "終わる", "続ける", "変える", "増える", "減る", "送る", "届く", "返す", "呼ぶ", "会う",
    "来る", "行く", "帰る", "寝る", "起きる", "走る", "飛ぶ", "泳ぐ", "描く", "感じる"
]
particles_endings = [
    "が", "を", "に", "で", "ね", "よ", "たい", "かな", "かも", "の",
    "は", "と", "へ", "から", "まで", "より", "だけ", "ほど", "し", "な"
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
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)}{get_random_element(icons)}",
        f"{get_random_element(comment_adjectives)} {get_random_element(particles_endings)}{get_random_element(icons)}{get_random_element(icons)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_verbs)}{get_random_element(icons)}",
        f"{get_random_element(icons)}{get_random_element(comment_adjectives)} {get_random_element(particles_endings)}",
        f"{get_random_element(comment_verbs)} {get_random_element(particles_endings)}{get_random_element(icons)}{get_random_element(icons)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)} {get_random_element(comment_verbs)}{get_random_element(icons)}",
        f"{get_random_element(icons)}{get_random_element(comment_nouns)} {get_random_element(particles_endings)} {get_random_element(comment_adjectives)}",
        f"{get_random_element(comment_adjectives)} {get_random_element(comment_nouns)}{get_random_element(icons)}{get_random_element(icons)}",
        f"{get_random_element(icons)}{get_random_element(comment_verbs)} {get_random_element(particles_endings)}{get_random_element(icons)}",
        f"{get_random_element(comment_nouns)} {get_random_element(particles_endings)}{get_random_element(icons)}{get_random_element(comment_adjectives)}"
    ]
    comment = get_random_element(structures)
    return comment

# Test hàm
if __name__ == "__main__":
    comment = generate_random_comment()
    print(f"{comment}")