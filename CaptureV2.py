import cv2
import os
import time

# Tạo thư mục data/chop nếu chưa tồn tại
output_dir = "data/chop"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Tìm số thứ tự của video mới nhất và đặt tên tiếp theo
def get_next_video_filename(output_dir):
    # Lấy danh sách các file trong thư mục
    files = os.listdir(output_dir)
    # Lọc ra các file có đuôi .avi
    video_files = [f for f in files if f.endswith(".avi")]

    if not video_files:
        # Nếu không có file nào, đặt tên là video_1.avi
        return os.path.join(output_dir, "video_1.avi")

    # Lấy số thứ tự lớn nhất từ các video đã tồn tại
    max_number = max([int(f.split('_')[1].split('.')[0]) for f in video_files])
    next_number = max_number + 1

    # Trả về tên file cho video tiếp theo
    return os.path.join(output_dir, f"video_{next_number}.avi")

# Thiết lập các thông số
frame_width = 640
frame_height = 480
fps = 20.0  # Frames per second
duration = 3  # Độ dài mỗi video (giây)
no_sequences = 20  # Số lượng video cần ghi lại

# Mở webcam
cap = cv2.VideoCapture(0)

# Kiểm tra xem webcam có mở được không
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

# Bắt đầu vòng lặp để capture và lưu video
for sequence in range(no_sequences):
    # Đặt tên video file và khởi tạo VideoWriter
    video_path = get_next_video_filename(output_dir)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Sử dụng codec XVID
    out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))

    # Đọc frame đầu tiên và hiển thị thông báo STARTING COLLECTION
    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, 'STARTING COLLECTION', (120, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
        # cv2.putText(frame, 'Collecting frames for Video Number {}'.format(sequence), (15, 12),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # Hiển thị frame lên màn hình
        cv2.imshow('Webcam', frame)
        cv2.waitKey(2000)  # Đợi 2 giây trước khi bắt đầu thu thập

    # Bắt đầu ghi video trong thời gian xác định (duration)
    start_time = time.time()  # Lưu lại thời điểm bắt đầu quay video

    while int(time.time() - start_time) < duration:
        # Đọc frame từ webcam
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame từ webcam.")
            break

        # Hiển thị thông tin lên frame
        # cv2.putText(frame, 'Collecting frames for Video Number {}'.format(sequence), (15, 12),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # Hiển thị frame lên màn hình
        cv2.imshow('Webcam', frame)

        # Ghi lại từng frame vào file video
        out.write(frame)

        # Kiểm tra nếu nhấn phím 'q' thì thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng VideoWriter cho mỗi video
    out.release()

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()

print("Hoàn thành quá trình thu thập dữ liệu và lưu video.")
