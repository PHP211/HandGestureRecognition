import cv2
import mediapipe as mp

# Khởi tạo các mô-đun của MediaPipe
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Mở camera
cap = cv2.VideoCapture(0)

# Khởi tạo mô hình MediaPipe Hands và Pose
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands, \
     mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    
    while cap.isOpened():
        # Đọc khung ảnh từ camera
        success, frame = cap.read()
        if not success:
            print("Không thể nhận diện được khung ảnh")
            break
        
        # Lấy kích thước của khung ảnh
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        
        # Chuyển đổi màu khung ảnh sang RGB (MediaPipe yêu cầu RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Xử lý ảnh để phát hiện bàn tay và tư thế cơ thể
        hand_results = hands.process(frame_rgb)
        pose_results = pose.process(frame_rgb)
        
        # Nếu phát hiện bàn tay
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Chuẩn hóa các điểm mốc theo tâm của khung hình
                for i, lm in enumerate(hand_landmarks.landmark):
                    # Chuyển đổi tọa độ từ tỷ lệ (0-1) sang tọa độ pixel
                    lm_x, lm_y = int(lm.x * width), int(lm.y * height)
                    
                    # Chuẩn hóa tọa độ theo tâm của khung hình
                    normalized_x = lm_x - center_x
                    normalized_y = lm_y - center_y
                    
                    # Hiển thị tọa độ chuẩn hóa (trung tâm)
                    normalized_text = f"Norm: ({normalized_x}, {normalized_y})"
                    
                    # Vẽ các tọa độ lên khung hình
                    cv2.putText(frame, normalized_text, (lm_x + 10, lm_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                
                # Vẽ các điểm landmarks và các đường nối lên ảnh
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Nếu phát hiện pose (tư thế cơ thể)
        if pose_results.pose_landmarks:
            # Vẽ các điểm landmarks của pose lên ảnh, không vẽ các đường nối
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), 
                                      mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
        
        # Hiển thị khung ảnh
        cv2.imshow('Hand and Pose Tracking', frame)
        
        # Thoát bằng cách nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Giải phóng bộ nhớ
cap.release()
cv2.destroyAllWindows()
