import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- 1. SETUP CAMERA & MEDIAPIPE ---
# Dùng cách import chuẩn
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# --- 2. SETUP ÂM THANH (Bản chuẩn) ---
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Lấy dải âm lượng
    vol_range = volume.GetVolumeRange()
    min_vol = vol_range[0]
    max_vol = vol_range[1]
except Exception as e:
    print("Lỗi khởi tạo âm thanh:", e)
    print("Hãy chắc chắn bạn đã chạy lệnh pip install comtypes==1.1.14 pycaw==20181226")
    exit()

# --- 3. VÒNG LẶP CHÍNH ---
while True:
    success, img = cap.read()
    if not success:
        break
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    lm_list = []
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

    if len(lm_list) != 0:
        # Lấy tọa độ ngón cái (4) và ngón trỏ (8)
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Vẽ hình
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Tính toán độ dài
        length = math.hypot(x2 - x1, y2 - y1)

        # Chuyển đổi độ dài tay sang âm lượng
        # 50 là chụm tay, 200 là duỗi tay (tùy chỉnh theo khoảng cách cam)
        vol = np.interp(length, [50, 200], [min_vol, max_vol])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Volume Control", img)
    
    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()