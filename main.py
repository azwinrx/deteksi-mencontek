import cv2
import mediapipe as mp
import numpy as np
import time
import os
import winsound
from datetime import datetime
import pickle
import json
import webbrowser
import threading
import pyautogui

#inisialisasi variabel
jumlahMencontek = 0
waktuMulai = None
sebelumnyaCurang = False
waktuTerakhirMencontek = 0

# Setup direktori untuk screenshot
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# User info
user_name = "Peserta"


#function buat format waktu
def formatWaktu(detik):
    menit = int(detik // 60)
    sisa_detik = int(detik % 60)
    return f"{menit:02d}:{sisa_detik:02d}"

#function buat ngitung durasi ujian
def hitungDurasiUjian(waktu_mulai):
    if waktu_mulai is None:
        return 0
    return time.time() - waktu_mulai

#function buat play sound alert
def playAlertSound():
    try:
        # Beep sound: frequency, duration
        winsound.Beep(1000, 300)  # 1000Hz, 300ms
    except:
        print("[WARNING] Sound tidak bisa dimainkan")

#function buat trigger auto-submit dengan buka tutup tab browser
def triggerAutoSubmit():
    """
    Buka dan tutup tab browser 1x untuk trigger
    sistem auto-submit di web quiz yang sudah deployed
    """
    def buka_tutup_tab():
        try:
            # URL quiz kamu
            url_target = 'http://localhost:5173/'
            
            # Buka tab baru
            webbrowser.open_new_tab(url_target)
            time.sleep(0.3)  # Tunggu tab kebuka
            
            # Tutup tab dengan Ctrl+W
            pyautogui.hotkey('ctrl', 'w')
                
            print("[ACTION] Buka-tutup 1 tab browser untuk trigger auto-submit!")
        except Exception as e:
            print(f"[WARNING] Gagal buka/tutup browser: {e}")
    
    # Jalankan di thread terpisah agar tidak blocking detection
    thread = threading.Thread(target=buka_tutup_tab)
    thread.daemon = True
    thread.start()

#function buat ambil screenshot
def ambilScreenshot(frame, alasan):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{timestamp}_{alasan}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[SCREENSHOT] Disimpan: {filename}")
    return filename

#face mesh setuup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#pilih kemera deffault
cap = cv2.VideoCapture(0)

# Setup window dengan size yang bisa diatur
window_name = 'Deteksi Menoncontek'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 360, 240)  # Ubah size sesuai kebutuhan (width, height)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # Always on top

print("[INFO] Deteksi Menoncontek siap. Tekan 'Q' untuk keluar.")

#loop utama program
while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = face_mesh.process(rgb_frame)
    
    img_h, img_w, _ = frame.shape
    
    status_text = "MENCARI WAJAH..."
    color_status = (200, 200, 200)

    if results.multi_face_landmarks:
        if waktuMulai is None:
            waktuMulai = time.time()
            print("[INFO] Ujian dimulai!")
        
        for face_landmarks in results.multi_face_landmarks:
            
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            face_3d = []
            face_2d = []

            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = 1 * img_w
            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            rmat, jac = cv2.Rodrigues(rot_vec)

            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            x_angle = angles[0] * 360
            y_angle = angles[1] * 360

            thresh_y = 15  # Naikin threshold tengok kiri/kanan (default: 7)
            thresh_x = 8   # Naikin threshold nunduk (default: 3)

            curangSekarang = False

            if y_angle < -thresh_y:
                status_text = "TENGOK KIRI (CURANG!)"
                color_status = (0, 0, 255)
                curangSekarang = True
            elif y_angle > thresh_y:
                status_text = "TENGOK KANAN (CURANG!)"
                color_status = (0, 0, 255)
                curangSekarang = True
            elif x_angle < -thresh_x:
                status_text = "NUNDUK (LIHAT HP?)"
                color_status = (0, 0, 255)
                curangSekarang = True
            else:
                status_text = "AMAN (FOKUS)"
                color_status = (0, 255, 0)
            
            waktuSekarang = time.time()
            if curangSekarang and (waktuSekarang - waktuTerakhirMencontek) > 2:  # Cooldown 2 detik (default: 2)
                jumlahMencontek += 1
                waktuTerakhirMencontek = waktuSekarang
                print(f"[WARNING] Terdeteksi mencontek! Total: {jumlahMencontek}x")
                
                # FITUR BARU: Play sound alert
                playAlertSound()
                
                # FITUR BARU: Ambil screenshot
                ambilScreenshot(frame, status_text.replace(" ", "_"))
                
                # FITUR BARU: Trigger auto-submit di web quiz
                triggerAutoSubmit()
            
            sebelumnyaCurang = curangSekarang

            nose_3d_projection, jac = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rot_vec, trans_vec, cam_matrix, dist_matrix)
            p1 = (int(face_2d[2][0]), int(face_2d[2][1]))
            p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
            
            cv2.line(frame, p1, p2, color_status, 3)

    cv2.rectangle(frame, (0,0), (img_w, 120), (0,0,0), -1) 
    cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_status, 2)
    cv2.putText(frame, f"User: {user_name}", (img_w - 250, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    if waktuMulai is not None:
        durasi = hitungDurasiUjian(waktuMulai)
        waktu_text = f"Durasi: {formatWaktu(durasi)}"
        cv2.putText(frame, waktu_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        mencontek_text = f"Mencontek: {jumlahMencontek}x"
        cv2.putText(frame, mencontek_text, (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        screenshot_text = f"Screenshots: {len([f for f in os.listdir('screenshots') if f.endswith('.jpg')])}"
        cv2.putText(frame, screenshot_text, (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if waktuMulai is not None:
    durasi_total = hitungDurasiUjian(waktuMulai)
    print("\n" + "="*50)
    print("RINGKASAN UJIAN")
    print("="*50)
    print(f"User: {user_name}")
    print(f"Durasi Total: {formatWaktu(durasi_total)}")
    print(f"Jumlah Mencontek: {jumlahMencontek}x")
    print(f"Screenshots Diambil: {len([f for f in os.listdir('screenshots') if f.endswith('.jpg')])}")
    print("="*50)