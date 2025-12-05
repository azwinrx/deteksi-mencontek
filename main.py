import cv2
import mediapipe as mp
import numpy as np
import time
import os
import winsound
from datetime import datetime
import pickle
import json

#inisialisasi variabel
jumlahMencontek = 0
waktuMulai = None
sebelumnyaCurang = False
waktuTerakhirMencontek = 0
timelineData = []  # untuk grafik timeline

# Setup direktori untuk screenshot dan data
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('data'):
    os.makedirs('data')

# Face Recognition setup
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
known_face_data = None
face_verified = False
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

#function buat ambil screenshot
def ambilScreenshot(frame, alasan):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{timestamp}_{alasan}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[SCREENSHOT] Disimpan: {filename}")
    return filename

#function buat verifikasi wajah
def verifyFace(frame, face_cascade, face_recognizer, known_face_data):
    if known_face_data is None:
        return True, "Unknown"
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return False, "No Face"
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_roi)
        
        # Confidence < 70 berarti match (semakin kecil semakin mirip)
        if confidence < 70:
            return True, user_name
        else:
            return False, "Unknown Person"
    
    return False, "No Match"

#function buat simpan timeline data
def simpanTimelineData(timeline_data, durasi_total, jumlah_mencontek):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data = {
        'timestamp': timestamp,
        'durasi_total': durasi_total,
        'jumlah_mencontek': jumlah_mencontek,
        'timeline': timeline_data,
        'user_name': user_name
    }
    
    filename = f"data/session_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[DATA] Timeline disimpan: {filename}")
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
cap = cv2.VideoCapture(2)

print("[INFO] Cyber Proctor siap. Tekan 'Q' untuk keluar.")

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

            thresh_y = 7
            thresh_x = 3

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
            if curangSekarang and (waktuSekarang - waktuTerakhirMencontek) > 2:
                jumlahMencontek += 1
                waktuTerakhirMencontek = waktuSekarang
                print(f"[WARNING] Terdeteksi mencontek! Total: {jumlahMencontek}x")
                
                # FITUR BARU: Play sound alert
                playAlertSound()
                
                # FITUR BARU: Ambil screenshot
                ambilScreenshot(frame, status_text.replace(" ", "_"))
                
                # FITUR BARU: Catat ke timeline
                timelineData.append({
                    'waktu': hitungDurasiUjian(waktuMulai),
                    'jenis': status_text,
                    'timestamp': datetime.now().isoformat()
                })
            
            sebelumnyaCurang = curangSekarang

            nose_3d_projection, jac = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rot_vec, trans_vec, cam_matrix, dist_matrix)
            p1 = (int(face_2d[2][0]), int(face_2d[2][1]))
            p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
            
            cv2.line(frame, p1, p2, color_status, 3)

    # FITUR BARU: Verifikasi wajah setiap 5 detik
    if waktuMulai is not None and int(hitungDurasiUjian(waktuMulai)) % 5 == 0:
        verified, detected_name = verifyFace(frame, face_cascade, face_recognizer, known_face_data)
        if not verified and known_face_data is not None:
            cv2.putText(frame, "WARNING: WAJAH TIDAK DIKENALI!", (img_w//2 - 250, img_h//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            if int(hitungDurasiUjian(waktuMulai)) % 10 == 0:  # Screenshot setiap 10 detik jika wajah tidak dikenali
                ambilScreenshot(frame, "UNAUTHORIZED_PERSON")
                playAlertSound()
    
    cv2.rectangle(frame, (0,0), (img_w, 120), (0,0,0), -1) 
    cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_status, 2)
    
    # Tampilkan nama user jika face recognition aktif
    if known_face_data is not None:
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

    cv2.imshow('Cyber Proctor - Face Mesh', frame)

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
    
    # FITUR BARU: Simpan timeline data
    if len(timelineData) > 0:
        data_file = simpanTimelineData(timelineData, durasi_total, jumlahMencontek)
        print(f"[INFO] Data sesi tersimpan untuk dashboard")
        print(f"[INFO] Jalankan 'python dashboard.py' untuk melihat dashboard!")