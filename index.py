import cv2
import numpy as np
import os
import subprocess
import random
import time
import threading

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
    threshold = 0.8
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
    print(f"Đã vuốt màn hình trên {device_id} từ ({x_start}, {start_y}) đến ({x_end}, {end_y})")

def process_device(device_id, template_configs, duration_minutes=15):
    screenshot_path = f"screenshot_{device_id}.png"
    swipe_count = 0
    
    skip_counts = {"like": 0, "save": 0, "follow": 0}
    min_skips = {
        "like": random.randint(1, 3),
        "save": random.randint(5, 8),
        "follow": random.randint(3, 10)
    }
    
    swipe_direction = random.choice(["left", "right"])
    #print(f"Thiết bị {device_id} sẽ vuốt chéo theo hướng: {swipe_direction}")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        remaining_minutes = (end_time - time.time()) / 60
        print(f"\nXử lý thiết bị {device_id} - Lần kiểm tra {swipe_count + 1} (Còn {remaining_minutes:.2f} phút)")
        
        swipe_screen(device_id, swipe_direction)
        
        # Delay ngẫu nhiên sau khi vuốt (3-7 giây)
        delay_after_swipe = random.uniform(3, 7)
        print(f"Chờ {delay_after_swipe:.2f} giây sau khi vuốt...")
        time.sleep(delay_after_swipe)
        
        screen = capture_screen(device_id, screenshot_path)
        if screen is None:
            print(f"Không thể xử lý thiết bị {device_id}")
            break

        for action, config in template_configs.items():
            positions = find_template(screen, config["path"])
            
            if positions:
                #print(f"Đã tìm thấy {len(positions)} template {action} trên {device_id} tại các tọa độ:")
                #for i, pos in enumerate(positions):
                    #print(f"[{i}] Top-left: ({pos[0]}, {pos[1]}), Bottom-right: ({pos[2]}, {pos[3]})")
                
                total_positions = len(positions)
                skip_start = int(total_positions * 0.20)
                skip_end = int(total_positions * 0.15)
                valid_range = total_positions - skip_start - skip_end
                
                if valid_range > 0:
                    should_action = random.random() < config["probability"]
                    if should_action and skip_counts[action] >= min_skips[action]:
                        random_index = random.randint(skip_start, total_positions - skip_end - 1)
                        selected_position = positions[random_index]
                        #print(f"Chọn template {action} tại index {random_index}: Top-left: ({selected_position[0]}, {selected_position[1]}), Bottom-right: ({selected_position[2]}, {selected_position[3]})")
                        
                        delay_before_click = random.uniform(8, 15)
                        print(f"Chờ {delay_before_click:.2f} giây trước khi {action}...")
                        time.sleep(delay_before_click)
                        
                        click_template(device_id, selected_position, action)
                        
                        delay_after_click = random.uniform(8, 15)
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

    print(f"Đã chạy hết {duration_minutes} phút trên {device_id}, kết thúc xử lý. Tổng cộng {swipe_count} lần vuốt.")
    delay = random.uniform(3, 5)
    print(f"Chờ {delay:.2f} giây trước khi kết thúc xử lý thiết bị {device_id}...")
    time.sleep(delay)

def main():
    template_configs = {
        "like": {"path": "like.png", "probability": 0.4, "min_skip_range": (1, 3)},
        "save": {"path": "save.png", "probability": 0.1, "min_skip_range": (5, 10)},
        "follow": {"path": "follow.png", "probability": 0.25, "min_skip_range": (3, 8)}
    }
    
    devices = get_connected_devices()
    if not devices:
        print("Không tìm thấy thiết bị Android nào.")
        return

    print(f"Đã tìm thấy {len(devices)} thiết bị: {devices}")

    duration_minutes = 15  # Có thể thay đổi thành 10, 20, 30, v.v.

    threads = []
    for idx, device_id in enumerate(devices):
        thread = threading.Thread(target=process_device, args=(device_id, template_configs, duration_minutes))
        threads.append(thread)
        print(f"Đã tạo luồng cho thiết bị {idx + 1}: {device_id}")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Đã hoàn thành xử lý tất cả các thiết bị.")

if __name__ == "__main__":
    main()