import cv2
import numpy as np
import os
import subprocess
import random
import time

# Hàm lấy danh sách thiết bị Android kết nối qua ADB
def get_connected_devices():
    result = subprocess.check_output(["adb", "devices"]).decode("utf-8")
    devices = [line.split("\t")[0] for line in result.strip().splitlines()[1:] if line]
    return devices

# Hàm chụp màn hình từ một thiết bị Android cụ thể
def capture_screen(device_id, output_path="screenshot.png"):
    os.system(f"adb -s {device_id} shell screencap /sdcard/screenshot.png")
    os.system(f"adb -s {device_id} pull /sdcard/screenshot.png {output_path}")
    screen = cv2.imread(output_path)
    if screen is None:
        print(f"Không thể đọc ảnh màn hình từ {output_path}")
    return screen

# Hàm tìm template (mẫu ảnh) trên màn hình
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
        positions.append((pt[0], pt[1], pt[0] + w, pt[1] + h))  # (x_min, y_min, x_max, y_max)
    return positions

# Hàm click ngẫu nhiên trong phạm vi một vùng tọa độ
def click_template(device_id, position):
    x_min, y_min, x_max, y_max = position
    x_random = random.randint(x_min, x_max)
    y_random = random.randint(y_min, y_max)
    os.system(f"adb -s {device_id} shell input tap {x_random} {y_random}")
    print(f"Đã click ngẫu nhiên tại ({x_random}, {y_random}) trên {device_id}")

# Hàm lấy độ phân giải màn hình thực tế của thiết bị
def get_screen_resolution(device_id):
    result = subprocess.check_output(f"adb -s {device_id} shell wm size").decode("utf-8")
    resolution = result.split(":")[1].strip().split("x")
    width, height = int(resolution[0]), int(resolution[1])
    return width, height

# Hàm vuốt màn hình từ dưới lên trên (một lần vuốt thẳng)
def swipe_screen(device_id):
    screen_width, screen_height = get_screen_resolution(device_id)
    start_y = random.randint(int(screen_height * 0.80), int(screen_height * 0.95))  # Gần đáy hơn
    end_y = random.randint(int(screen_height * 0.05), int(screen_height * 0.20))    # Gần đỉnh hơn
    x_start = int(screen_width * 0.5)  # Cố định ở giữa màn hình
    
    os.system(f"adb -s {device_id} shell input swipe {x_start} {start_y} {x_start} {end_y} 200")
    print(f"Đã vuốt màn hình trên {device_id} từ ({x_start}, {start_y}) đến ({x_start}, {end_y})")

# Hàm xử lý từng thiết bị với vòng lặp tìm template
def process_device(device_id, template_path, max_swipes=5):
    screenshot_path = f"screenshot_{device_id}.png"
    swipe_count = 0

    while swipe_count < max_swipes:
        print(f"\nXử lý thiết bị {device_id} - Lần kiểm tra {swipe_count + 1}")
        
        # Vuốt màn hình trước khi tìm template, không delay trước vuốt
        swipe_screen(device_id)
        
        # Chụp màn hình sau khi vuốt
        screen = capture_screen(device_id, screenshot_path)
        if screen is None:
            print(f"Không thể xử lý thiết bị {device_id}")
            break

        # Tìm các vị trí của template trên màn hình
        positions = find_template(screen, template_path)

        if positions:
            print(f"Đã tìm thấy {len(positions)} template trên {device_id} tại các tọa độ:")
            for i, pos in enumerate(positions):
                print(f"[{i}] Top-left: ({pos[0]}, {pos[1]}), Bottom-right: ({pos[2]}, {pos[3]})")
            
            total_positions = len(positions)
            skip_start = int(total_positions * 0.20)  # Bỏ qua 20% đầu
            skip_end = int(total_positions * 0.15)    # Bỏ qua 15% cuối
            valid_range = total_positions - skip_start - skip_end
            
            if valid_range > 0:
                random_index = random.randint(skip_start, total_positions - skip_end - 1)
                selected_position = positions[random_index]
                print(f"Chọn template tại index {random_index}: Top-left: ({selected_position[0]}, {selected_position[1]}), Bottom-right: ({selected_position[2]}, {selected_position[3]})")
                
                # Thêm độ trễ trước khi click (5-10 giây)
                delay_before_click = random.uniform(5, 10)
                print(f"Chờ {delay_before_click:.2f} giây trước khi click...")
                time.sleep(delay_before_click)
                
                click_template(device_id, selected_position)
                
                # Thêm độ trễ sau khi click (5-10 giây)
                delay_after_click = random.uniform(5, 10)
                print(f"Chờ {delay_after_click:.2f} giây sau khi click...")
                time.sleep(delay_after_click)
                
                swipe_count += 1
            else:
                print("Danh sách positions quá ngắn, không đủ để bỏ qua 20% đầu và 15% cuối, tiếp tục vuốt...")
                swipe_count += 1
        else:
            print(f"Không tìm thấy template trên {device_id}")
            swipe_count += 1

    if swipe_count >= max_swipes:
        print(f"Đã vuốt {max_swipes} lần nhưng không tìm thấy template đủ điều kiện trên {device_id}")
        delay = random.uniform(5, 10)
        print(f"Chờ {delay:.2f} giây trước khi chuyển thiết bị tiếp theo...")
        time.sleep(delay)

# Chương trình chính
def main():
    template_path = "like.png"
    devices = get_connected_devices()

    if not devices:
        print("Không tìm thấy thiết bị Android nào.")
        return

    print(f"Đã tìm thấy {len(devices)} thiết bị: {devices}")

    for idx, device_id in enumerate(devices):
        print(f"\nBắt đầu xử lý thiết bị {idx + 1}: {device_id}")
        process_device(device_id, template_path, max_swipes=5)

if __name__ == "__main__":
    main()