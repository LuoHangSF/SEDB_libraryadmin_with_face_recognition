# -*- coding: utf-8 -*-
"""
管理员人脸登录功能模块：
- 扫描 ./admin_img 目录下的 *.jpg，文件名（不含扩展名）视为管理员账号（即 administer.a_name）
- 使用 face_recognition 读取并编码人脸
- 打开摄像头进行实时检测，10 秒内如识别到任一已知人脸，等待 1 秒后关闭窗口并返回账号
- 若 10 秒未识别到，返回 None
"""
import os
import time
import glob
from typing import List, Tuple, Optional

import cv2
import numpy as np
import face_recognition


ADMIN_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "admin_img")
ADMIN_IMG_DIR = os.path.normpath(ADMIN_IMG_DIR)


def ensure_admin_img_dir() -> None:
    """确保管理员人脸图片目录存在"""
    os.makedirs(ADMIN_IMG_DIR, exist_ok=True)


def _load_known_faces() -> Tuple[List[np.ndarray], List[str]]:
    """
    扫描 ADMIN_IMG_DIR 下所有 .jpg 图片，构建人脸编码列表与对应账号名称列表。
    仅取首个人脸编码；若图片中未检测到人脸则跳过。
    """
    ensure_admin_img_dir()
    encodings: List[np.ndarray] = []
    names: List[str] = []

    jpg_files = glob.glob(os.path.join(ADMIN_IMG_DIR, "*.jpg"))
    for file_path in jpg_files:
        try:
            base = os.path.basename(file_path)
            name, ext = os.path.splitext(base)
            if ext.lower() != ".jpg":
                continue
            image = face_recognition.load_image_file(file_path)
            face_encs = face_recognition.face_encodings(image)
            if len(face_encs) == 0:
                # 跳过无可用人脸的图片
                continue
            encodings.append(face_encs[0])
            names.append(name)  # name 即管理员账号
        except Exception:
            # 单个文件失败不影响整体流程
            continue

    return encodings, names


def run_admin_face_login(timeout_seconds: int = 10, hold_on_recognition_seconds: float = 1.0) -> Optional[str]:
    """
    打开摄像头进行管理员人脸识别。
    成功：返回识别到的管理员账号（与 ./admin_img/<account>.jpg 文件名一致）
    失败：返回 None
    """
    known_face_encodings, known_face_names = _load_known_faces()
    if not known_face_encodings:
        # 没有任何可用人脸
        return None

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return None

    process_this_frame = True
    recognized_account: Optional[str] = None
    recognized_at: float = 0.0

    face_locations = []
    face_names = []

    start_time = time.time()

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            if process_this_frame:
                # 缩放到 1/4 加速
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    if len(face_distances) > 0:
                        best_match_index = int(np.argmin(face_distances))
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            if recognized_account is None:
                                recognized_account = name
                                recognized_at = time.time()
                    face_names.append(name)

            process_this_frame = not process_this_frame

            # 标注框（放大至原始尺寸）
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                color = (0, 128, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            cv2.imshow("Admin Face Login", frame)

            # 成功后等待 hold_on_recognition_seconds 秒再退出
            if recognized_account is not None and (time.time() - recognized_at) >= hold_on_recognition_seconds:
                break

            # 超时失败
            if (time.time() - start_time) >= timeout_seconds:
                recognized_account = None
                break

            # 允许按 'q' 快速退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                recognized_account = None
                break

    finally:
        video_capture.release()
        cv2.destroyAllWindows()

    return recognized_account