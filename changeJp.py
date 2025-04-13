import google.generativeai as genai

# Thay bằng API KEY của bạn
API_KEY = "AIzaSyARv0WwzI817I27XRCRvX7SzjzoZe0luPs"
genai.configure(api_key=API_KEY)

# Chọn model (Gemini Pro)
model = genai.GenerativeModel('gemini-1.5-flash')

# Gửi câu hỏi
response = model.generate_content(
                                        """
                                        Generate one optimistic comment in English for a random TikTok video.
                                            The comment must:
                                            - Be exactly 5-8 words long.
                                            - Be positive, casual, and TikTok-friendly (e.g., "This video is super fun vibe").
                                            - Be unique and creative each time, avoiding repetition.
                                            - Avoid special characters like quotes (' or "), exclamation marks (!), or punctuation other than spaces.
                                            - Be safe for all audiences.
                                            Examples:
                                            - "Really cool dance moves"
                                            - "Your vibe is amazing"
                                            - "This video rocks big time"
                                            - "Super fun content keep it up"
                                        """, generation_config=genai.types.GenerationConfig(
                                            temperature=1.0,  # Tăng sáng tạo
                                            max_output_tokens=50  # Giới hạn độ dài
                                        )
                                        )

# In kết quả
print(response.text)
