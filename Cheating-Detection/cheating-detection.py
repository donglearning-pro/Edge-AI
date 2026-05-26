import cv2
from ultralytics import YOLO
import winsound
import os
import time

# 1. Tạo thư mục 'canh_bao' nếu chưa có
if not os.path.exists('canh_bao'):
    os.makedirs('canh_bao')

model = YOLO('yolo11s.pt') 
cap = cv2.VideoCapture(0)

last_saved_time = 0  # Biến ghi lại lần cuối chụp ảnh

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame, conf=0.25, verbose=False) 
    found_phone = False

    for r in results:
        for box in r.boxes:
            name = model.names[int(box.cls[0])]
            if name in ['cell phone', 'remote']:
                found_phone = True
                break
    
    if found_phone:
        current_time = time.time()
        
        # Cảnh báo âm thanh và chữ
        winsound.Beep(1000, 200)
        cv2.putText(frame, "DA CHUP ANH BANG CHUNG!", (50, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 2. KIỂM TRA: Nếu cách lần chụp trước hơn 2 giây thì mới chụp tiếp
        if current_time - last_saved_time > 2:
            # Tạo tên file theo ngày giờ: ví dụ phone_17123456.jpg
            file_name = f"canh_bao/phone_{int(current_time)}.jpg"
            
            # Lệnh chụp và lưu ảnh
            cv2.imwrite(file_name, frame)
            
            print(f"--- Đã lưu bằng chứng: {file_name} ---")
            last_saved_time = current_time # Cập nhật thời điểm chụp cuối

    cv2.imshow('AI Evidence Collector', results[0].plot())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()