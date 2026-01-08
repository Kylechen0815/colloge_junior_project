import cv2
import socket
import os
import importlib
import mediapipe as mp

# 初始化 MediaPipe Pose 模块
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ✅ Socket 設置（目前已註解，如需啟用請取消註解）
host = '127.0.0.1'
port = 6001  # 確保端口號與 Unity 一致

"""
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Connected to Unity server.")
except ConnectionError as e:
    print(f"Failed to connect to Unity server: {e}")
    exit()
"""

# ✅ 定義要傳送的關鍵點索引
important_landmarks = [9, 0, 12, 14, 16, 18, 11, 13, 15, 17, 23, 24, 25, 26, 29, 30]

# ✅ 嘗試開啟影片（修正路徑格式）
video_path = r"D:\college hw\專題\修正slow swing.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise FileNotFoundError(f"❌ 無法開啟影片: {video_path}")

print("✅ 成功開啟影片！")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ 錯誤: 無法擷取畫面。")
        break

    # ✅ 轉換為 RGB（Mediapipe 需要此格式）
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # ✅ 傳送關鍵點資料到 Unity
    if results.pose_landmarks:
        data = ""
        for idx in important_landmarks:
            # ✅ 替換 `9` 為 `23` 和 `24` 的平均點
            if idx == 9:
                landmark_23 = results.pose_landmarks.landmark[23]
                landmark_24 = results.pose_landmarks.landmark[24]
                avg_x = (landmark_23.x + landmark_24.x) / 2
                avg_y = (landmark_23.y + landmark_24.y) / 2
                avg_visibility = (landmark_23.visibility + landmark_24.visibility) / 2
                keypoint_str = f"{avg_x:.4f},{avg_y:.4f},{avg_visibility:.4f}"
            else:
                landmark = results.pose_landmarks.landmark[idx]
                keypoint_str = f"{landmark.x:.4f},{landmark.y:.4f},{landmark.visibility:.4f}"

            print(f"📡 傳送數據: {keypoint_str}")
            data += f"{keypoint_str}\n"

        """
        try:
            client.sendall(data.encode('utf-8'))
            print("📡 數據成功發送到 Unity！")
        except ConnectionError as e:
            print(f"❌ 傳送錯誤: {e}")
            break
        """

    # ✅ 繪製骨架
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose Detection', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
# client.close()  # 若啟用 socket，請取消註解
cv2.destroyAllWindows()
