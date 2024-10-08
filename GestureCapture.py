import cv2
import os

# Tạo thư mục data/pinch nếu chưa tồn tại
output_dir = "data/chop"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Tìm số thứ tự của video mới nhất và đặt tên tiếp theo
def get_next_video_filename(output_dir):
    files = os.listdir(output_dir)
    # Lọc các file video với định dạng .avi
    video_files = [f for f in files if f.startswith("video_") and f.endswith(".avi")]
    
    if not video_files:
        return os.path.join(output_dir, "video_1.avi")
    
    # Tìm số lớn nhất trong các file đã tồn tại
    video_numbers = [int(f.split('_')[1].split('.')[0]) for f in video_files]
    next_number = max(video_numbers) + 1
    return os.path.join(output_dir, f"video_{next_number}.avi")

# Thiết lập các thông số video
video_name = get_next_video_filename(output_dir)
frame_width = 640
frame_height = 480
fps = 20.0  # Frames per second
duration = 3  # Thời gian quay video (giây)

# Mở webcam
cap = cv2.VideoCapture(0)

# Kiểm tra xem webcam có mở được không
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

# Hiển thị webcam và chờ người dùng nhấn Enter
print("Webcam đang hiển thị. Nhấn Enter để bắt đầu quay video...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ webcam.")
        break

    # Hiển thị webcam lên màn hình
    cv2.imshow('Webcam', frame)

    # Đợi người dùng nhấn Enter để bắt đầu quay video
    if cv2.waitKey(1) & 0xFF == 13:  # 13 là mã ASCII của phím Enter
        break

# Định dạng video đầu ra
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_name, fourcc, fps, (frame_width, frame_height))

print(f"Đang quay video trong {duration} giây...")

# Quay video trong thời gian quy định
for i in range(int(fps * duration)):
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ webcam.")
        break
    out.write(frame)  # Ghi lại từng frame vào file video
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video đã lưu tại: {video_name}")
