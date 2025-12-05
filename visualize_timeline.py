import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

def loadLatestSession():
    """Load data session terakhir"""
    data_files = [f for f in os.listdir('data') if f.endswith('.json')]
    if not data_files:
        print("[ERROR] Tidak ada data session yang tersimpan!")
        return None
    
    latest_file = sorted(data_files)[-1]
    filepath = os.path.join('data', latest_file)
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"[INFO] Memuat data dari: {latest_file}")
    return data

def plotTimeline(data):
    """Buat grafik timeline interaktif"""
    if not data or not data['timeline']:
        print("[ERROR] Data timeline kosong!")
        return
    
    timeline = data['timeline']
    
    # Extract data
    waktu_list = [t['waktu'] for t in timeline]
    jenis_list = [t['jenis'] for t in timeline]
    
    # Buat figure dengan 2 subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'📊 Analisis Ujian - {data["user_name"]}', fontsize=16, fontweight='bold')
    
    # Subplot 1: Timeline scatter plot
    colors = []
    for jenis in jenis_list:
        if 'KIRI' in jenis:
            colors.append('red')
        elif 'KANAN' in jenis:
            colors.append('orange')
        elif 'NUNDUK' in jenis:
            colors.append('purple')
        else:
            colors.append('blue')
    
    ax1.scatter(waktu_list, range(len(waktu_list)), c=colors, s=100, alpha=0.6, edgecolors='black')
    ax1.set_xlabel('Waktu (detik)', fontsize=12)
    ax1.set_ylabel('Kejadian ke-', fontsize=12)
    ax1.set_title('Timeline Pelanggaran', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Tengok Kiri'),
        Patch(facecolor='orange', label='Tengok Kanan'),
        Patch(facecolor='purple', label='Nunduk')
    ]
    ax1.legend(handles=legend_elements, loc='upper left')
    
    # Subplot 2: Bar chart by type
    jenis_count = {}
    for jenis in jenis_list:
        jenis_count[jenis] = jenis_count.get(jenis, 0) + 1
    
    types = list(jenis_count.keys())
    counts = list(jenis_count.values())
    bar_colors = ['red' if 'KIRI' in t else 'orange' if 'KANAN' in t else 'purple' for t in types]
    
    ax2.bar(range(len(types)), counts, color=bar_colors, alpha=0.7, edgecolor='black')
    ax2.set_xticks(range(len(types)))
    ax2.set_xticklabels(types, rotation=15, ha='right')
    ax2.set_xlabel('Jenis Pelanggaran', fontsize=12)
    ax2.set_ylabel('Jumlah', fontsize=12)
    ax2.set_title('Distribusi Jenis Pelanggaran', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add count labels on bars
    for i, count in enumerate(counts):
        ax2.text(i, count + 0.1, str(count), ha='center', fontweight='bold')
    
    # Add info text
    info_text = f"""
    📝 Ringkasan:
    • Durasi: {int(data['durasi_total']//60)}m {int(data['durasi_total']%60)}s
    • Total Pelanggaran: {data['jumlah_mencontek']}x
    • Session: {data['timestamp']}
    """
    fig.text(0.02, 0.02, info_text, fontsize=10, verticalalignment='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Simpan grafik
    output_file = f"data/timeline_plot_{data['timestamp']}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"[SAVED] Grafik disimpan: {output_file}")
    
    plt.show()

if __name__ == "__main__":
    print("="*60)
    print("📈 VISUALISASI TIMELINE UJIAN")
    print("="*60)
    
    data = loadLatestSession()
    if data:
        plotTimeline(data)
    else:
        print("\n[INFO] Jalankan main.py terlebih dahulu untuk mengumpulkan data!")
