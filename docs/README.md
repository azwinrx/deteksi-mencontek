# 🎓 Cyber Proctor - Sistem Deteksi Kecurangan Ujian

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-red.svg)

**Tugas Pengolahan Citra Digital** - Sistem monitoring ujian otomatis menggunakan Computer Vision & Face Tracking.

## 🚀 Fitur Utama

### ⭐ Core Features

- **Real-time Face Tracking** - Deteksi posisi wajah menggunakan MediaPipe Face Mesh
- **Cheat Detection** - Otomatis mendeteksi tengok kiri/kanan/nunduk
- **Live Counter** - Hitung jumlah pelanggaran secara real-time

### 🔥 Advanced Features (BARU!)

1. **🔊 Alert Sound System** - Bunyi alarm otomatis saat mencontek terdeteksi
2. **📸 Auto Screenshot Capture** - Screenshot otomatis + timestamp saat pelanggaran
3. **👤 Face Recognition** - Verifikasi identitas peserta ujian (anti-joki)
4. **📊 Interactive Timeline Graph** - Visualisasi pola kecurangan dengan matplotlib
5. **🌐 Real-time Dashboard** - Web dashboard dengan Flask untuk monitoring

## 📋 Requirements

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install matplotlib
pip install flask
pip install opencv-contrib-python
```

## 🎯 Cara Penggunaan

### 1️⃣ Setup Face Recognition (Opsional)

Untuk mengaktifkan verifikasi identitas:

```bash
python register_face.py
```

- Masukkan nama Anda
- Ambil 30 foto wajah dari berbagai sudut
- Model akan tersimpan otomatis

### 2️⃣ Jalankan Sistem Deteksi

```bash
python main.py
```

**Kontrol:**

- `Q` - Keluar dari program
- Sistem akan otomatis:
  - ✅ Merekam timeline pelanggaran
  - ✅ Mengambil screenshot
  - ✅ Membunyikan alarm
  - ✅ Verifikasi wajah (jika sudah registrasi)

### 3️⃣ Visualisasi Timeline

Setelah ujian selesai, lihat grafik interaktif:

```bash
python visualize_timeline.py
```

Akan menampilkan:

- Timeline scatter plot pelanggaran
- Bar chart distribusi jenis pelanggaran
- Statistik lengkap sesi ujian

### 4️⃣ Dashboard Web (Real-time Monitoring)

Untuk monitoring multiple sessions:

```bash
python dashboard.py
```

Buka browser: **http://localhost:5000**

**Dashboard Features:**

- 📊 Statistik keseluruhan (total sessions, violations, avg)
- 📝 List semua session ujian
- ⏱️ Timeline latest session
- 🔄 Auto-refresh setiap 10 detik

## 📁 Struktur Project

```
deteksi-mencontek/
├── main.py                    # Program utama
├── register_face.py           # Setup face recognition
├── visualize_timeline.py      # Grafik timeline
├── dashboard.py               # Flask web dashboard
├── templates/
│   └── dashboard.html         # Template dashboard
├── data/                      # Data session (JSON)
├── screenshots/               # Screenshot pelanggaran
├── known_faces/               # Model face recognition
│   ├── face_model.yml
│   └── face_data.pkl
└── README.md
```

## 🎨 Tampilan

### Main Detection Window

- **Header Bar**: Status deteksi + informasi real-time
- **Face Mesh**: Visualisasi 468 landmark points
- **Direction Arrow**: Indikator arah pandangan
- **Counters**: Durasi, jumlah mencontek, screenshots

### Dashboard Web

- **Stats Cards**: Total sessions, violations, averages
- **Timeline Panel**: Kronologis pelanggaran
- **Sessions List**: History semua ujian
- **Responsive Design**: Support mobile & desktop

## 🔧 Konfigurasi

Edit di `main.py`:

```python
# Threshold deteksi
thresh_y = 7   # Sensitivitas kiri/kanan (default: 7)
thresh_x = 3   # Sensitivitas nunduk (default: 3)

# Cooldown deteksi
waktuTerakhirMencontek > 2  # Interval deteksi (detik)

# Index kamera
cap = cv2.VideoCapture(2)  # 0=default, 1,2,3=external
```

## 📊 Output Data

### JSON Session Data (`data/session_TIMESTAMP.json`)

```json
{
  "timestamp": "20251204_143025",
  "durasi_total": 120.5,
  "jumlah_mencontek": 7,
  "user_name": "John Doe",
  "timeline": [
    {
      "waktu": 15.2,
      "jenis": "TENGOK KIRI (CURANG!)",
      "timestamp": "2025-12-04T14:30:40"
    }
  ]
}
```

### Screenshots

Format: `YYYYMMDD_HHMMSS_STATUS.jpg`

- Contoh: `20251204_143045_TENGOK_KANAN.jpg`

## 🛡️ Teknologi

| Komponen         | Teknologi                           |
| ---------------- | ----------------------------------- |
| Face Detection   | MediaPipe Face Mesh (468 landmarks) |
| Face Recognition | OpenCV LBPH Recognizer              |
| Pose Estimation  | solvePnP 3D → 2D projection         |
| Visualization    | Matplotlib + Seaborn                |
| Web Framework    | Flask + HTML/CSS/JS                 |
| Alert System     | Windows winsound                    |

## 🎓 Use Cases

✅ **Ujian Online** - Monitor peserta ujian jarak jauh
✅ **Proctoring System** - Sistem pengawasan otomatis
✅ **Research** - Dataset perilaku ujian
✅ **Demo** - Presentasi computer vision
✅ **Learning** - Belajar face tracking & pose estimation

## 🐛 Troubleshooting

**Kamera tidak terdeteksi:**

```python
cap = cv2.VideoCapture(0)  # Coba index 0, 1, atau 2
```

**Face recognition tidak akurat:**

- Ambil lebih banyak foto saat registrasi (30-50)
- Pastikan pencahayaan cukup
- Coba adjust confidence threshold

**Sound tidak keluar:**

- Windows: Pastikan `winsound` terinstall
- Linux/Mac: Ganti dengan `playsound` atau `pygame`

## 📈 Future Improvements

- [ ] Multi-person detection (detect kolaborasi curang)
- [ ] Eye tracking (deteksi arah pandang mata)
- [ ] Blur detection (deteksi kamera ditutup)
- [ ] WebSocket untuk real-time streaming
- [ ] Export report PDF
- [ ] Integration dengan LMS (Moodle, Canvas)

## 👨‍💻 Author

**Tugas Pengolahan Citra Digital - Semester 7**

## 📄 License

Educational purposes only - Feel free to use for learning!

---

⭐ **Star repo ini jika bermanfaat!** ⭐
