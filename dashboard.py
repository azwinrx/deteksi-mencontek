from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)

def getAllSessions():
    """Load semua data session"""
    sessions = []
    if not os.path.exists('data'):
        return sessions
    
    data_files = [f for f in os.listdir('data') if f.endswith('.json')]
    
    for file in sorted(data_files, reverse=True):
        filepath = os.path.join('data', file)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                sessions.append(data)
        except:
            pass
    
    return sessions

def getLatestSession():
    """Load session terakhir"""
    sessions = getAllSessions()
    return sessions[0] if sessions else None

@app.route('/')
def index():
    """Halaman utama dashboard"""
    return render_template('dashboard.html')

@app.route('/api/sessions')
def api_sessions():
    """API untuk list semua session"""
    sessions = getAllSessions()
    return jsonify(sessions)

@app.route('/api/latest')
def api_latest():
    """API untuk session terakhir"""
    session = getLatestSession()
    return jsonify(session if session else {})

@app.route('/api/stats')
def api_stats():
    """API untuk statistik keseluruhan"""
    sessions = getAllSessions()
    
    if not sessions:
        return jsonify({
            'total_sessions': 0,
            'total_violations': 0,
            'avg_violations': 0,
            'total_duration': 0
        })
    
    total_violations = sum(s['jumlah_mencontek'] for s in sessions)
    total_duration = sum(s['durasi_total'] for s in sessions)
    
    stats = {
        'total_sessions': len(sessions),
        'total_violations': total_violations,
        'avg_violations': round(total_violations / len(sessions), 2),
        'total_duration': round(total_duration / 60, 2),  # dalam menit
        'last_session': sessions[0]['timestamp']
    }
    
    return jsonify(stats)

@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    """Serve screenshot files"""
    return send_from_directory('screenshots', filename)

@app.route('/api/screenshots')
def api_screenshots():
    """API untuk list semua screenshot"""
    screenshots = []
    if not os.path.exists('screenshots'):
        return jsonify([])
    
    files = [f for f in os.listdir('screenshots') if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for file in sorted(files, reverse=True):
        # Parse filename untuk extract info
        # Format: 20251204_201615_TENGOK_KANAN_(CURANG!).jpg
        parts = file.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
        if len(parts) >= 3:
            date = parts[0]
            time = parts[1]
            action = '_'.join(parts[2:])
            
            screenshots.append({
                'filename': file,
                'url': f'/screenshots/{file}',
                'date': date,
                'time': time,
                'action': action,
                'timestamp': f"{date}_{time}"
            })
    
    return jsonify(screenshots)

if __name__ == '__main__':
    # Buat template directory
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("="*60)
    print("🌐 CYBER PROCTOR DASHBOARD")
    print("="*60)
    print("📍 Dashboard berjalan di: http://localhost:5000")
    print("💡 Tekan Ctrl+C untuk berhenti")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
