import cv2
import numpy as np
import os
import subprocess
import random
import time
import threading
import json
from bot import generate_random_comment
import google.generativeai as genai
import re

API_KEY = "AIzaSyARv0WwzI817I27XRCRvX7SzjzoZe0luPs"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_connected_devices():
    result = subprocess.check_output(["adb", "devices"]).decode("utf-8")
    devices = [line.split("\t")[0] for line in result.strip().splitlines()[1:] if line]
    return devices

def capture_screen(device_id, output_path="screenshot.png"):
    os.system(f"adb -s {device_id} shell screencap /sdcard/screenshot.png")
    os.system(f"adb -s {device_id} pull /sdcard/screenshot.png {output_path}")
    screen = cv2.imread(output_path)
    if screen is None:
        print(f"Không thể đọc ảnh màn hình từ {output_path}")
    return screen

def find_template(screen, template_path):
    if not os.path.exists(template_path):
        print(f"Không tìm thấy file template tại: {template_path}")
        return []
    
    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"Không thể đọc file template: {template_path}")
        return []
    
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    #threshold = 0.5 # Ngưỡng phát hiện template của J7pro
    threshold = 0.8 # Ngưỡng phát hiện template của A600
    loc = np.where(result >= threshold)
    positions = []
    for pt in zip(*loc[::-1]):
        positions.append((pt[0], pt[1], pt[0] + w, pt[1] + h))
    return positions

def click_template(device_id, position, action_name):
    x_min, y_min, x_max, y_max = position
    x_random = random.randint(x_min, x_max)
    y_random = random.randint(y_min, y_max)
    os.system(f"adb -s {device_id} shell input tap {x_random} {y_random}")
    print(f"Đã {action_name} ngẫu nhiên tại ({x_random}, {y_random}) trên {device_id}")

def get_screen_resolution(device_id):
    result = subprocess.check_output(f"adb -s {device_id} shell wm size").decode("utf-8")
    resolution = result.split(":")[1].strip().split("x")
    width, height = int(resolution[0]), int(resolution[1])
    return width, height

def swipe_screen(device_id, direction):
    screen_width, screen_height = get_screen_resolution(device_id)
    
    start_y = random.randint(int(screen_height * 0.60), int(screen_height * 0.70))
    x_start = random.randint(int(screen_width * 0.15), int(screen_width * 0.75))
    
    end_y = random.randint(int(screen_height * 0.15), int(screen_height * 0.25))
    if direction == "right":
        x_end = min(int(screen_width * 0.85), x_start + random.randint(100, 300))
    else:
        x_end = max(int(screen_width * 0.15), x_start - random.randint(100, 300))
    
    os.system(f"adb -s {device_id} shell input swipe {x_start} {start_y} {x_end} {end_y} 200")
    #print(f"Đã vuốt màn hình trên {device_id} từ ({x_start}, {start_y}) đến ({x_end}, {end_y})")

def process_device(device_id, template_configs, duration_minutes=15, results_dict=None):
    screenshot_path = f"screenshot_{device_id}.png"
    swipe_count = 0
    
    skip_counts = {"like": 0, "save": 0, "follow": 0, "share": 0, "comment": 0}
    min_skips = {
        "like": random.randint(1, 3),
        "save": random.randint(5, 8),
        "follow": random.randint(3, 10),
        "share": random.randint(4, 9),
        "comment": random.randint(2, 6)
    }
    # Đếm số lần click cho từng hành động
    action_counts = {"like": 0, "save": 0, "follow": 0, "share": 0, "comment": 0} 
    
    swipe_direction = random.choice(["left", "right"])
    #print(f"Thiết bị {device_id} sẽ vuốt chéo theo hướng: {swipe_direction}")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        remaining_minutes = (end_time - time.time()) / 60
        print(f"\nXử lý thiết bị {device_id} - Lần kiểm tra {swipe_count + 1} (Còn {remaining_minutes:.2f} phút)")
        
        swipe_screen(device_id, swipe_direction)
        
        delay_after_swipe = random.uniform(3, 13)
        print(f"Chờ {delay_after_swipe:.2f} giây sau khi vuốt...")
        time.sleep(delay_after_swipe)
        
        screen = capture_screen(device_id, screenshot_path)
        if screen is None:
            print(f"Không thể xử lý thiết bị {device_id}")
            break

        for action, config in template_configs.items():
            positions = find_template(screen, config["path"])
            
            if positions:                
                total_positions = len(positions)
                skip_start = int(total_positions * 0.20)
                skip_end = int(total_positions * 0.15)
                valid_range = total_positions - skip_start - skip_end
                
                if valid_range > 0:
                    should_action = random.random() < config["probability"]
                    if should_action and skip_counts[action] >= min_skips[action]:
                        random_index = random.randint(skip_start, total_positions - skip_end - 1)
                        selected_position = positions[random_index]
                        print(f"Chọn template {action} tại index {random_index}: Top-left: ({selected_position[0]}, {selected_position[1]}), Bottom-right: ({selected_position[2]}, {selected_position[3]})")
                        
                        delay_before_click = random.uniform(2, 3)
                        print(f"Chờ {delay_before_click:.2f} giây trước khi {action}...")
                        time.sleep(delay_before_click)
                        
                        click_template(device_id, selected_position, action)
                        action_counts[action] += 1  # Tăng số lần click

                        # Xử lý đặc biệt cho "comment"
                        if action == "comment":
                            # response = model.generate_content(
                            #                 """
                            #                 Generate one optimistic comment in English for a random TikTok video.
                            #                     The comment must:
                            #                     - Be exactly 5-8 words long.
                            #                     - Be positive, casual, and TikTok-friendly (e.g., "This video is super fun vibe").
                            #                     - Be unique and creative each time, avoiding repetition.
                            #                     - Avoid special characters like quotes (' or "), exclamation marks (!), or punctuation other than spaces.
                            #                     - Be safe for all audiences.
                            #                     Examples:
                            #                     - "Really cool dance moves"
                            #                     - "Your vibe is amazing"
                            #                     - "This video rocks big time"
                            #                     - "Super fun content keep it up"
                            #                 """, generation_config=genai.types.GenerationConfig(
                            #                     temperature=1.0,  # Tăng sáng tạo
                            #                 ))
                            # if response:
                            #     comment = response.text.strip()
                            #     comment = re.sub(r'\n|\r', '', comment)  # Loại bỏ xuống dòng (\n, \r)
                            # else:
                            #     fallback_comments = [
                            #     "This video is super cool",
                            #     "Love your awesome vibe",
                            #     "Really fun content keep going",
                            #     "Great moves in this clip",
                            #     "Your video rocks big time"
                            #     ]
                            #     comment = random.choice(fallback_comments)

                            # Chụp màn hình sau khi bấm comment
                            delay_before_icon = random.uniform(4, 6)
                            print(f"Chờ {delay_before_icon:.2f} giây trước khi tìm icon...")
                            time.sleep(delay_before_icon)
                            
                            screen_after_comment = capture_screen(device_id, screenshot_path)
                            icon_positions = find_template(screen_after_comment, "./template/icon.png")
                            
                            if icon_positions:
                                icon_index = random.randint(0, len(icon_positions) - 1)
                                icon_position = icon_positions[icon_index]
                                print(f"Tìm thấy template icon tại: Top-left: ({icon_position[0]}, {icon_position[1]})")
                                
                                delay_before_icon_click = random.uniform(1, 1.5)
                                print(f"Chờ {delay_before_icon_click:.2f} giây trước khi click icon...")
                                time.sleep(delay_before_icon_click)
                                
                                click_template(device_id, icon_position, "click icon")
                                
                                # Kiểm tra send.png
                                delay_before_send = random.uniform(1, 1.5)
                                print(f"Chờ {delay_before_send:.2f} giây trước khi tìm send...")
                                time.sleep(delay_before_send)
                                
                                screen_after_icon = capture_screen(device_id, screenshot_path)
                                send_positions = find_template(screen_after_icon, "./template/send.png")
                                
                                if send_positions:
                                    send_index = random.randint(0, len(send_positions) - 1)
                                    send_position = send_positions[send_index]
                                    print(f"Tìm thấy template send tại: Top-left: ({send_position[0]}, {send_position[1]})")                              
                                    # Nhập giá trị vào input
                                    comment = generate_random_comment()
                                    if not comment:
                                        comment = "This video is really cool"
                                        print("Comment rỗng, dùng giá trị mặc định")
                                    escaped_comment = comment.replace("'", "\\'").replace(" ", "\\ ")
                                    os.system(f"adb -s {device_id} shell input text '{comment}'")
                                    print(f"Đã nhập '{comment}' vào input")
                                    
                                    delay_before_cmt = random.uniform(1.5, 2.5)
                                    print(f"Chờ {delay_before_cmt:.2f} giây trước khi tìm cmt...")
                                    time.sleep(delay_before_cmt)
                                    
                                    screen_after_input = capture_screen(device_id, screenshot_path)
                                    cmt_positions = find_template(screen_after_input, "./template/cmt.png")
                                    
                                    if cmt_positions:
                                        cmt_index = random.randint(0, len(cmt_positions) - 1)
                                        cmt_position = cmt_positions[cmt_index]
                                        print(f"Tìm thấy template cmt tại: Top-left: ({cmt_position[0]}, {cmt_position[1]})")
                                        
                                        delay_before_cmt_click = random.uniform(1.5, 2)
                                        print(f"Chờ {delay_before_cmt_click:.2f} giây trước khi click cmt...")
                                        time.sleep(delay_before_cmt_click)
                                        
                                        click_template(device_id, cmt_position, "click cmt")
                                        action_counts["comment"] += 1
                                    
                                    # Thoát khung comment sau khi hoàn tất (bấm cmt hoặc không tìm thấy cmt)
                                    delay_before_x = random.uniform(1, 1.5)
                                    print(f"Chờ {delay_before_x:.2f} giây trước khi tìm x để thoát comment...")
                                    time.sleep(delay_before_x)
                                    
                                    screen_after_cmt = capture_screen(device_id, screenshot_path)
                                    x_positions = find_template(screen_after_cmt, "./template/x.png")
                                    
                                    if x_positions:
                                        x_index = random.randint(0, len(x_positions) - 1)
                                        x_position = x_positions[x_index]
                                        print(f"Tìm thấy template x tại: Top-left: ({x_position[0]}, {x_position[1]})")
                                        
                                        delay_before_x_click = random.uniform(1, 1.5)
                                        print(f"Chờ {delay_before_x_click:.2f} giây trước khi click x...")
                                        time.sleep(delay_before_x_click)
                                        
                                        click_template(device_id, x_position, "click x")
                                    else:
                                        print("Không tìm thấy template x.png, thoát khung comment bằng cách bấm ngoài màn hình...")
                                        screen_width, screen_height = get_screen_resolution(device_id)
                                        escape_x = random.randint(int(screen_width * 0.25), int(screen_width * 0.75))
                                        escape_y = random.randint(0, int(screen_height * 0.5))
                                        escape_position = (escape_x, escape_y, escape_x, escape_y)
                                        
                                        delay_before_escape1 = random.uniform(1, 2)
                                        print(f"Chờ {delay_before_escape1:.2f} giây trước khi click thoát lần 1...")
                                        time.sleep(delay_before_escape1)
                                        click_template(device_id, escape_position, "thoát khung comment lần 1")
                                        
                                        delay_between_escape = random.uniform(1, 2)
                                        print(f"Chờ {delay_between_escape:.2f} giây trước khi click thoát lần 2...")
                                        time.sleep(delay_between_escape)
                                        click_template(device_id, escape_position, "thoát khung comment lần 2")
                                else:
                                    print("Không tìm thấy template send.png, thoát khung comment...")
                                    delay_before_x = random.uniform(1, 1.5)
                                    print(f"Chờ {delay_before_x:.2f} giây trước khi tìm x để thoát comment...")
                                    time.sleep(delay_before_x)
                                    
                                    screen_after_icon = capture_screen(device_id, screenshot_path)
                                    x_positions = find_template(screen_after_icon, "./template/x.png")
                                    
                                    if x_positions:
                                        x_index = random.randint(0, len(x_positions) - 1)
                                        x_position = x_positions[x_index]
                                        print(f"Tìm thấy template x tại: Top-left: ({x_position[0]}, {x_position[1]})")
                                        
                                        delay_before_x_click = random.uniform(1, 1.5)
                                        print(f"Chờ {delay_before_x_click:.2f} giây trước khi click x...")
                                        time.sleep(delay_before_x_click)
                                        
                                        click_template(device_id, x_position, "click x")
                                    else:
                                        print("Không tìm thấy template x.png, thoát khung comment bằng cách bấm ngoài màn hình...")
                                        screen_width, screen_height = get_screen_resolution(device_id)
                                        escape_x = random.randint(int(screen_width * 0.25), int(screen_width * 0.75))
                                        escape_y = random.randint(0, int(screen_height * 0.5))
                                        escape_position = (escape_x, escape_y, escape_x, escape_y)
                                        
                                        delay_before_escape1 = random.uniform(1, 2)
                                        print(f"Chờ {delay_before_escape1:.2f} giây trước khi click thoát lần 1...")
                                        time.sleep(delay_before_escape1)
                                        click_template(device_id, escape_position, "thoát khung comment lần 1")
                                        
                                        delay_between_escape = random.uniform(1, 2)
                                        print(f"Chờ {delay_between_escape:.2f} giây trước khi click thoát lần 2...")
                                        time.sleep(delay_between_escape)
                                        click_template(device_id, escape_position, "thoát khung comment lần 2")
                            else:
                                print("Không tìm thấy template icon.png sau khi bấm comment")
                        # Xử lý đặc biệt cho "share"
                        if action == "share":
                            # Chụp màn hình lại sau khi bấm share
                            delay_before_link = random.uniform(1, 1.5)
                            print(f"Chờ {delay_before_link:.2f} giây trước khi tìm link...")
                            time.sleep(delay_before_link)
                            
                            screen_after_share = capture_screen(device_id, screenshot_path)
                            link_positions = find_template(screen_after_share, "./template/link.png")
                            x_positions = find_template(screen_after_share, "./template/x.png")
                            if link_positions:
                                link_index = random.randint(0, len(link_positions) - 1)
                                link_position = link_positions[link_index]
                                print(f"Tìm thấy template link tại: Top-left: ({link_position[0]}, {link_position[1]})")
                                
                                delay_before_link_click = random.uniform(1.5, 2.5)
                                print(f"Chờ {delay_before_link_click:.2f} giây trước khi click link...")
                                time.sleep(delay_before_link_click)
                                
                                click_template(device_id, link_position, "click link")
                                action_counts["share"] += 1  # Tăng thêm lần nữa nếu bấm link thành công
                            elif x_positions:
                                delay_before_x = random.uniform(1.5, 2.5)
                                time.sleep(delay_before_x)
                                print("Không tìm thấy template link.png chờ {delay_before_x:.2f} giây trước khi click x...")
                                click_template(device_id, x_positions, "click link")
                            else:
                                screen_width, screen_height = get_screen_resolution(device_id)
                                escape_x = random.randint(int(screen_width * 0.25), int(screen_width * 0.75))
                                escape_y = random.randint(0, int(screen_height * 0.85))  # Nửa trên màn hình
                                escape_position = (escape_x, escape_y, escape_x, escape_y)  # Định dạng tương
                                delay_before_escape = random.uniform(1.5, 2)
                                print(f"Không tìm thấy link.png và x.png, chờ {delay_before_escape:.2f} giây trước khi click thoát tại ({escape_x}, {escape_y})...")
                                time.sleep(delay_before_escape)
                                
                                click_template(device_id, escape_position, "thoát popup share")
                        delay_after_click = random.uniform(2.5, 4.5)
                        print(f"Chờ {delay_after_click:.2f} giây sau khi {action}...")
                        time.sleep(delay_after_click)
                        
                        skip_counts[action] = 0
                        min_skips[action] = random.randint(config["min_skip_range"][0], config["min_skip_range"][1])
                    else:
                        print(f"Chưa {action}: Đã vuốt qua {skip_counts[action]}/{min_skips[action]} video, tỷ lệ chưa đạt ({config['probability']*100}%)")
                        skip_counts[action] += 1
                else:
                    print(f"Danh sách positions của {action} quá ngắn, không đủ để bỏ qua 20% đầu và 15% cuối")
                    skip_counts[action] += 1
            else:
                print(f"Không tìm thấy template {action} trên {device_id}")
                skip_counts[action] += 1
        
        swipe_count += 1

    # Lưu kết quả vào results_dict
    results_dict[device_id] = {
        "like": action_counts["like"],
        "save": action_counts["save"],
        "follow": action_counts["follow"],
        "share": action_counts["share"],
        "comment": action_counts["comment"],
        "total_swipes": swipe_count
    }
    
    delay = random.uniform(2, 3)
    print(f"Chờ {delay:.2f} giây trước khi kết thúc xử lý thiết bị {device_id}...")
    time.sleep(delay)

def main():
    template_configs = {
        "like": {"path": "./template/like.png", "probability": 0.4, "min_skip_range": (1, 3)},
        "save": {"path": "./template/save.png", "probability": 0.2, "min_skip_range": (5, 10)},
        "follow": {"path": "./template/follow.png", "probability": 0.25, "min_skip_range": (3, 8)},
        "share": {"path": "./template/share.png", "probability": 0.1, "min_skip_range": (2, 6)},
        "comment": {"path": "./template/comment.png", "probability": 0.3, "min_skip_range": (3, 7)} 
    }
    
    devices = get_connected_devices()
    if not devices:
        print("Không tìm thấy thiết bị Android nào.")
        return

    print(f"Đã tìm thấy {len(devices)} thiết bị: {devices}")

    duration_minutes = 30  # Có thể thay đổi thành 10, 20, 30, v.v.
    results = {}  # Dictionary để lưu kết quả từ tất cả các thiết bị
    threads = []
    for idx, device_id in enumerate(devices):
        thread = threading.Thread(target=process_device, args=(device_id, template_configs, duration_minutes, results))
        threads.append(thread)
        print(f"Đã tạo luồng cho thiết bị {idx + 1}: {device_id}")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
# Ghi kết quả vào file JSON
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print("Đã lưu kết quả vào file 'results.json'.")
    print("Đã hoàn thành xử lý tất cả các thiết bị.")

if __name__ == "__main__":
    main()