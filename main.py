import cv2
import mediapipe as mp
import numpy as np
import time

#inisialisasi variabel
jumlahMencontek = 0
waktuMulai = None
sebelumnyaCurang = False
waktuTerakhirMencontek = 0

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
            
            sebelumnyaCurang = curangSekarang

            nose_3d_projection, jac = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rot_vec, trans_vec, cam_matrix, dist_matrix)
            p1 = (int(face_2d[2][0]), int(face_2d[2][1]))
            p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
            
            cv2.line(frame, p1, p2, color_status, 3)

    cv2.rectangle(frame, (0,0), (img_w, 100), (0,0,0), -1) 
    cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_status, 2)
    
    if waktuMulai is not None:
        durasi = hitungDurasiUjian(waktuMulai)
        waktu_text = f"Durasi: {formatWaktu(durasi)}"
        cv2.putText(frame, waktu_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        mencontek_text = f"Mencontek: {jumlahMencontek}x"
        cv2.putText(frame, mencontek_text, (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

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
    print(f"Durasi Total: {formatWaktu(durasi_total)}")
    print(f"Jumlah Mencontek: {jumlahMencontek}x")
    print("="*50)