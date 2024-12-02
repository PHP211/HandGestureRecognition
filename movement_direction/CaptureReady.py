import cv2
import mediapipe as mp
import os
import numpy as np

# Khởi tạo Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Danh sách lưu tọa độ ngón trỏ qua các frame
finger_positions = []

# Đường dẫn đến thư mục chứa các frame ảnh
folder_path = 'movement_direction/extracted_frames'  # Thay thế với đường dẫn thư mục của bạn

# Lấy danh sách tất cả các tệp ảnh trong thư mục (đảm bảo rằng các tệp là ảnh .jpg, .png, v.v.)
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Sắp xếp các tệp ảnh theo thứ tự (nếu cần thiết)
image_files.sort()  # Sắp xếp theo tên tệp, có thể cần thay đổi nếu tên tệp không theo thứ tự số

# Kiểm tra xem có đủ 15 frame không
print(f"Total number of frames found: {len(image_files)}")

# Biến lưu tọa độ ngón trỏ của frame đầu tiên (để chuẩn hóa)
first_finger_position = None

# Xử lý từng frame
for i, image_file in enumerate(image_files):
    # Đọc frame từ file
    frame_path = os.path.join(folder_path, image_file)
    frame = cv2.imread(frame_path)
    
    if frame is None:
        print(f"Error reading frame {image_file}")
        continue  # Bỏ qua nếu không thể đọc ảnh
    
    # Chuyển đổi hình ảnh từ BGR (OpenCV) sang RGB (Mediapipe yêu cầu)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Xử lý frame với Mediapipe Hands model
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Lấy tọa độ ngón trỏ (điểm mốc 8)
            index_finger = landmarks.landmark[8]  # Tọa độ ngón trỏ
            x, y = index_finger.x, index_finger.y  # Tọa độ ngón trỏ (tỉ lệ 0-1)
            
            # Nếu chưa có tọa độ ngón trỏ của frame đầu tiên, lưu lại tọa độ đó
            if first_finger_position is None:
                first_finger_position = (x, y)
            
            # Chuẩn hóa tọa độ ngón trỏ so với frame đầu tiên (lấy ngón trỏ ở frame đầu tiên làm (0, 0))
            normalized_x = x - first_finger_position[0]
            normalized_y = y - first_finger_position[1]
            
            # Lưu lại tọa độ ngón trỏ vào danh sách
            finger_positions.append((normalized_x, normalized_y))
            print(f"Frame {i+1}: Finger position {normalized_x:.4f}, {normalized_y:.4f}")
    else:
        print(f"Frame {i+1}: No hand landmarks detected")

# Kiểm tra tổng số phần tử trong finger_positions
print(f"Total number of finger positions: {len(finger_positions)}")

# Lưu dữ liệu sự thay đổi của ngón trỏ (dưới dạng tọa độ chuẩn hóa)
print(finger_positions)
