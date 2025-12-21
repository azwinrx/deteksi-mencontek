# 🎓 Cyber Proctor - Sistem Deteksi Kecurangan Ujian

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)

**Tugas Pengolahan Citra Digital** - Sistem monitoring ujian otomatis menggunakan Computer Vision & Face Tracking dengan integrasi web quiz.

## 🚀 Fitur Utama

### ⭐ Core Features

- **Real-time Face Tracking** - Deteksi posisi wajah menggunakan MediaPipe Face Mesh
- **Cheat Detection** - Otomatis mendeteksi tengok kiri/kanan/nunduk dengan threshold yang dapat dikustomisasi
- **Live Counter** - Hitung jumlah pelanggaran secara real-time

### 🔥 Advanced Features

1. **🔊 Alert Sound System** - Bunyi alarm otomatis saat mencontek terdeteksi
2. **📸 Auto Screenshot Capture** - Screenshot otomatis + timestamp saat pelanggaran
3. **🌐 Browser Tab Integration** - Integrasi dengan web quiz untuk auto-submit
4. **📏 Always On Top Window** - Window monitoring tetap di atas untuk mencegah disembunyikan
5. **⏱️ Smart Cooldown System** - Delay 5 detik antar deteksi untuk menghindari false positive

## 📋 Requirements

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pyautogui
```

## 🎯 Cara Penggunaan

### 1️⃣ Setup URL Web Quiz

Edit `main.py` pada line ~62:

```python
url_target = 'http://localhost:5173/'  # Ganti dengan URL quiz kamu
```

### 2️⃣ Jalankan Sistem Deteksi

```bash
python main.py
```

**Kontrol:**

- `Q` - Keluar dari program
- Window size: 640x360 (dapat diubah di line ~100)
- Always on top: Aktif secara default

**Sistem akan otomatis:**

- ✅ Mendeteksi tengok kiri/kanan (threshold: 15°)
- ✅ Mendeteksi nunduk (threshold: 8°)
- ✅ Mengambil screenshot ke folder `screenshots/`
- ✅ Membunyikan alarm beep
- ✅ Membuka-tutup tab browser untuk trigger auto-submit
- ✅ Cooldown 5 detik antar deteksi

### 3️⃣ Setelah Ujian

Program akan menampilkan ringkasan:

```
==================================================
RINGKASAN UJIAN
==================================================
User: Peserta
Durasi Total: 15:30
Jumlah Mencontek: 3x
Screenshots Diambil: 3
==================================================
```

## ⚙️ Kustomisasi

### Ubah Threshold Deteksi

Di `main.py` line ~180:

```python
thresh_y = 15  # Tengok kiri/kanan (default: 15°)
thresh_x = 8   # Nunduk (default: 8°)
```

### Ubah Cooldown Timer

Di `main.py` line ~194:

```python
if curangSekarang and (waktuSekarang - waktuTerakhirMencontek) > 5:  # 5 detik
```

### Ubah Ukuran Window

Di `main.py` line ~100:

```python
cv2.resizeWindow(window_name, 640, 360)  # (width, height)
```

## 📁 Struktur Project

```
deteksi-mencontek/
├── main.py                    # Program utama
├── screenshots/               # Screenshot pelanggaran
├── docs/                      # Dokumentasi
│   └── README.md
└── .gitignore
```

## 🎨 Tampilan

### Main Detection Window

- **Header Bar**: Status deteksi + informasi real-time
- **Face Mesh**: Visualisasi 468 landmark points
- **Direction Arrow**: Indikator arah pandangan
- **Counters**: Durasi, jumlah mencontek, screenshots
- **Always On Top**: Window pinned di atas untuk monitoring ketat

## 🔧 Cara Kerja Integrasi Web Quiz

1. **Deteksi Kecurangan** → Sistem mendeteksi tengok/nunduk
2. **Trigger Action** → Buka-tutup 1 tab browser ke URL quiz
3. **Focus Change Event** → Web quiz detect tab switch
4. **Auto Submit** → Setelah 5x focus change, quiz otomatis submit

### Setup di Web Quiz

Web quiz harus implement detection focus change:

```javascript
let focusChangeCount = 0;

window.addEventListener("blur", function () {
  focusChangeCount++;
  if (focusChangeCount >= 5) {
    submitQuiz(); // Auto submit
  }
});
```

## 📊 Output Data

### Screenshots

Format: `YYYYMMDD_HHMMSS_STATUS.jpg`

- Contoh: `20251204_143045_TENGOK_KANAN.jpg`
- Lokasi: `screenshots/` folder

### Console Output

```
[INFO] Cyber Proctor siap. Tekan 'Q' untuk keluar.
[INFO] Ujian dimulai!
[WARNING] Terdeteksi mencontek! Total: 1x
[SCREENSHOT] Disimpan: screenshots/20251221_143045_TENGOK_KANAN.jpg
[ACTION] Buka-tutup 1 tab browser untuk trigger auto-submit!
```

## 🛡️ Teknologi

| Komponen        | Teknologi                           |
| --------------- | ----------------------------------- |
| Face Detection  | MediaPipe Face Mesh (468 landmarks) |
| Pose Estimation | solvePnP 3D → 2D projection         |
| Alert System    | Windows winsound beep               |
| Browser Control | webbrowser + pyautogui              |
| Screenshot      | OpenCV imwrite                      |

## 🎓 Use Cases

✅ **Ujian Online** - Monitor peserta ujian jarak jauh dengan auto-submit
✅ **Proctoring System** - Sistem pengawasan otomatis terintegrasi
✅ **Research** - Dataset perilaku ujian dan deteksi kecurangan
✅ **Demo** - Presentasi computer vision dan automation
✅ **Learning** - Belajar face tracking & browser automation

## 🐛 Troubleshooting

**Kamera tidak terdeteksi:**

```python
cap = cv2.VideoCapture(0)  # Coba index 0, 1, atau 2
```

**Browser tidak terbuka:**

- Pastikan ada default browser di sistem
- Cek apakah URL quiz sudah benar
- Test manual: `python -c "import webbrowser; webbrowser.open('http://localhost:5173/')"`

**Tab tidak tertutup otomatis:**

- Pastikan `pyautogui` terinstall
- Browser harus dalam focus saat `Ctrl+W` ditekan
- Delay 0.3 detik mungkin perlu diubah jika koneksi lambat

**Sound tidak keluar:**

- Windows: Pastikan volume tidak mute
- Check: `python -c "import winsound; winsound.Beep(1000, 300)"`

**Terlalu sensitif:**

- Naikin threshold: `thresh_y = 20` dan `thresh_x = 10`
- Naikin cooldown: `> 10` (10 detik)

## 📈 Future Improvements

- [ ] Multi-person detection untuk detect kolaborasi
- [ ] Eye tracking untuk deteksi arah pandang mata
- [ ] Configurable settings via JSON/YAML
- [ ] Log file untuk audit trail
- [ ] Email notification saat pelanggaran
- [ ] Integration dengan LMS (Moodle, Canvas)

## 👨‍💻 Author

**Tugas Pengolahan Citra Digital - Semester 7**

## 📄 License

Educational purposes only - Feel free to use for learning!

---

⭐ **Star repo ini jika bermanfaat!** ⭐
