# 🚀 QUICK START GUIDE

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Pilih Mode Penggunaan

### Mode A: Tanpa Face Recognition (Langsung Pakai)

```bash
python main.py
```

- Tekan `Q` untuk keluar
- Screenshot & data akan tersimpan otomatis

### Mode B: Dengan Face Recognition (Recommended)

**1. Registrasi wajah terlebih dahulu:**

```bash
python register_face.py
```

- Masukkan nama Anda
- Ambil 30 foto (tekan SPACE)
- Model akan tersimpan

**2. Jalankan deteksi:**

```bash
python main.py
```

- Sistem akan verifikasi wajah Anda
- Warning jika wajah tidak dikenali

## Step 3: Lihat Hasil

### Timeline Graph

```bash
python visualize_timeline.py
```

### Web Dashboard

```bash
python dashboard.py
```

Buka: http://localhost:5000

## ⚡ Tips & Tricks

### Sesuaikan Sensitivitas

Edit `main.py`:

```python
thresh_y = 7   # Kiri/kanan (makin kecil = makin sensitif)
thresh_x = 3   # Nunduk (makin kecil = makin sensitif)
```

### Ganti Kamera

```python
cap = cv2.VideoCapture(0)  # Coba 0, 1, 2, atau 3
```

### Interval Screenshot

```python
if curangSekarang and (waktuSekarang - waktuTerakhirMencontek) > 2:
# Ubah angka 2 (detik) sesuai kebutuhan
```

## 📊 Output Locations

| Output         | Location                     |
| -------------- | ---------------------------- |
| Screenshots    | `screenshots/`               |
| Session Data   | `data/session_*.json`        |
| Timeline Plots | `data/timeline_plot_*.png`   |
| Face Model     | `known_faces/face_model.yml` |

## 🎯 Demo Workflow

1. `python register_face.py` → Daftar wajah
2. `python main.py` → Jalankan deteksi (pura-pura mencontek)
3. `python visualize_timeline.py` → Lihat grafik
4. `python dashboard.py` → Buka dashboard

## 🐛 Common Issues

**Error: "No module named 'cv2'"**

```bash
pip install opencv-python opencv-contrib-python
```

**Error: "No module named 'flask'"**

```bash
pip install flask
```

**Kamera tidak muncul:**

- Coba index kamera berbeda (0, 1, 2)
- Cek permission kamera di Windows Settings

**Sound tidak keluar:**

- Normal, hanya berfungsi di Windows
- Untuk Linux/Mac: install `pygame`

## 🎓 For Presentation

1. Demo deteksi real-time
2. Screenshot bukti pelanggaran
3. Tampilkan grafik timeline
4. Buka dashboard untuk impress dosen! 😎

---

**Need help?** Read full README.md
