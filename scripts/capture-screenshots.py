from playwright.sync_api import sync_playwright
import time
import os

SCREENSHOT_DIR = "/home/j1coder/github-repos/GroundStation/docs/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Tracker mockup - satellite tracking map view
TRACKER_HTML = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroundStation - Satellite Tracker</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #030712; color: #e5e7eb; height: 100vh; display: flex; }
        .sidebar { width: 260px; background: #111827; padding: 20px; border-right: 1px solid #1f2937; }
        .logo { font-size: 18px; font-weight: 700; color: #22d3ee; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
        .logo-icon { font-size: 24px; }
        .logo-sub { font-size: 11px; color: #6b7280; font-weight: 400; margin-bottom: 32px; }
        .nav-section { font-size: 11px; text-transform: uppercase; color: #6b7280; letter-spacing: 1px; margin: 20px 0 8px 0; }
        .nav-item { padding: 10px 14px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 2px; font-size: 14px; color: #9ca3af; }
        .nav-item:hover { background: #1f2937; color: #e5e7eb; }
        .nav-item.active { background: rgba(34, 211, 238, 0.15); color: #22d3ee; }
        .main { flex: 1; display: flex; flex-direction: column; }
        .topbar { padding: 16px 24px; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; }
        .topbar h1 { font-size: 20px; font-weight: 600; }
        .topbar-actions { display: flex; gap: 12px; align-items: center; }
        .badge { background: rgba(34, 197, 94, 0.15); color: #22c55e; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500; display: flex; align-items: center; gap: 6px; }
        .badge .dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .content { flex: 1; display: flex; gap: 0; }
        .map-area { flex: 1; background: #0c1220; position: relative; overflow: hidden; }
        .map-grid { position: absolute; inset: 0; background-image: 
            linear-gradient(rgba(34, 211, 238, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(34, 211, 238, 0.03) 1px, transparent 1px);
            background-size: 50px 50px; }
        .map-continents { position: absolute; inset: 0; }
        .continent { position: absolute; background: rgba(34, 211, 238, 0.08); border: 1px solid rgba(34, 211, 238, 0.15); border-radius: 20px; }
        .continent.na { top: 20%; left: 8%; width: 18%; height: 25%; }
        .continent.sa { top: 50%; left: 15%; width: 10%; height: 30%; }
        .continent.eu { top: 15%; left: 42%; width: 12%; height: 15%; }
        .continent.af { top: 30%; left: 42%; width: 14%; height: 30%; }
        .continent.as { top: 15%; left: 55%; width: 22%; height: 30%; }
        .continent.au { top: 55%; left: 75%; width: 12%; height: 15%; }
        .satellite { position: absolute; width: 10px; height: 10px; }
        .satellite::before { content: ''; position: absolute; inset: 0; background: #22d3ee; border-radius: 50%; box-shadow: 0 0 15px rgba(34, 211, 238, 0.6); }
        .satellite::after { content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 24px; height: 24px; border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 50%; }
        .sat1 { top: 30%; left: 25%; animation: orbit1 8s linear infinite; }
        .sat2 { top: 45%; left: 60%; animation: orbit2 12s linear infinite; }
        .sat3 { top: 60%; left: 35%; animation: orbit3 10s linear infinite; }
        .sat4 { top: 20%; left: 75%; animation: orbit1 15s linear infinite; }
        @keyframes orbit1 { 0% { transform: translate(0, 0); } 50% { transform: translate(30px, -20px); } 100% { transform: translate(0, 0); } }
        @keyframes orbit2 { 0% { transform: translate(0, 0); } 50% { transform: translate(-25px, 15px); } 100% { transform: translate(0, 0); } }
        @keyframes orbit3 { 0% { transform: translate(0, 0); } 50% { transform: translate(20px, 25px); } 100% { transform: translate(0, 0); } }
        .ground-station { position: absolute; width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; }
        .ground-station::after { content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20px; height: 20px; border: 1px dashed rgba(245, 158, 11, 0.4); border-radius: 50%; }
        .gs1 { top: 35%; left: 18%; }
        .gs2 { top: 25%; left: 48%; }
        .gs3 { top: 55%; left: 70%; }
        .info-panel { width: 380px; background: #111827; border-left: 1px solid #1f2937; padding: 24px; overflow-y: auto; }
        .panel-title { font-size: 14px; font-weight: 600; color: #22d3ee; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
        .sat-card { background: #1f2937; border: 1px solid #374151; border-radius: 10px; padding: 16px; margin-bottom: 12px; }
        .sat-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .sat-name { font-weight: 600; font-size: 15px; }
        .sat-status { font-size: 11px; padding: 4px 10px; border-radius: 12px; font-weight: 500; }
        .sat-status.tracking { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
        .sat-status.passing { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
        .sat-status.predicted { background: rgba(34, 211, 238, 0.15); color: #22d3ee; }
        .sat-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; }
        .sat-meta-item { }
        .sat-meta-label { color: #6b7280; }
        .sat-meta-value { color: #e5e7eb; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo"><span class="logo-icon">📡</span> GroundStation</div>
        <div class="logo-sub">Satellite Tracking Platform</div>
        <div class="nav-section">Tracking</div>
        <div class="nav-item active">🗺️ Live Map</div>
        <div class="nav-item">🛰️ Satellites</div>
        <div class="nav-item">🔄 Passes</div>
        <div class="nav-section">Data</div>
        <div class="nav-item">📊 Telemetry</div>
        <div class="nav-item">📈 Analytics</div>
        <div class="nav-item">💾 Recordings</div>
        <div class="nav-section">System</div>
        <div class="nav-item">⚙️ Ground Stations</div>
        <div class="nav-item">🔧 Configuration</div>
    </div>
    <div class="main">
        <div class="topbar">
            <h1>🗺️ Live Satellite Tracker</h1>
            <div class="topbar-actions">
                <div class="badge"><span class="dot"></span> 4 Satellites Tracked</div>
                <div style="background:#1f2937;padding:8px 16px;border-radius:8px;font-size:13px;font-family:'JetBrains Mono',monospace;">UTC 2026-07-18 14:32:07</div>
            </div>
        </div>
        <div class="content">
            <div class="map-area">
                <div class="map-grid"></div>
                <div class="map-continents">
                    <div class="continent na"></div>
                    <div class="continent sa"></div>
                    <div class="continent eu"></div>
                    <div class="continent af"></div>
                    <div class="continent as"></div>
                    <div class="continent au"></div>
                </div>
                <div class="satellite sat1"></div>
                <div class="satellite sat2"></div>
                <div class="satellite sat3"></div>
                <div class="satellite sat4"></div>
                <div class="ground-station gs1"></div>
                <div class="ground-station gs2"></div>
                <div class="ground-station gs3"></div>
            </div>
            <div class="info-panel">
                <div class="panel-title">🛰️ Tracked Satellites</div>
                <div class="sat-card">
                    <div class="sat-header">
                        <span class="sat-name">NOAA-19</span>
                        <span class="sat-status tracking">● Tracking</span>
                    </div>
                    <div class="sat-meta">
                        <div class="sat-meta-item"><span class="sat-meta-label">NORAD ID</span><br><span class="sat-meta-value">33591</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Altitude</span><br><span class="sat-meta-value">854 km</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Velocity</span><br><span class="sat-meta-value">7.45 km/s</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Inclination</span><br><span class="sat-meta-value">98.74°</span></div>
                    </div>
                </div>
                <div class="sat-card">
                    <div class="sat-header">
                        <span class="sat-name">ISS (ZARYA)</span>
                        <span class="sat-status passing">● AOS in 12m</span>
                    </div>
                    <div class="sat-meta">
                        <div class="sat-meta-item"><span class="sat-meta-label">NORAD ID</span><br><span class="sat-meta-value">25544</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Altitude</span><br><span class="sat-meta-value">421 km</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Velocity</span><br><span class="sat-meta-value">7.66 km/s</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Inclination</span><br><span class="sat-meta-value">51.64°</span></div>
                    </div>
                </div>
                <div class="sat-card">
                    <div class="sat-header">
                        <span class="sat-name">STARLINK-4201</span>
                        <span class="sat-status tracking">● Tracking</span>
                    </div>
                    <div class="sat-meta">
                        <div class="sat-meta-item"><span class="sat-meta-label">NORAD ID</span><br><span class="sat-meta-value">48274</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Altitude</span><br><span class="sat-meta-value">550 km</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Velocity</span><br><span class="sat-meta-value">7.59 km/s</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Inclination</span><br><span class="sat-meta-value">53.05°</span></div>
                    </div>
                </div>
                <div class="sat-card">
                    <div class="sat-header">
                        <span class="sat-name">TIANGONG</span>
                        <span class="sat-status predicted">● Predicted</span>
                    </div>
                    <div class="sat-meta">
                        <div class="sat-meta-item"><span class="sat-meta-label">NORAD ID</span><br><span class="sat-meta-value">48274</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Altitude</span><br><span class="sat-meta-value">389 km</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Velocity</span><br><span class="sat-meta-value">7.68 km/s</span></div>
                        <div class="sat-meta-item"><span class="sat-meta-label">Inclination</span><br><span class="sat-meta-value">41.47°</span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Telemetry mockup
TELEMETRY_HTML = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroundStation - Telemetry Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #030712; color: #e5e7eb; height: 100vh; display: flex; }
        .sidebar { width: 260px; background: #111827; padding: 20px; border-right: 1px solid #1f2937; }
        .logo { font-size: 18px; font-weight: 700; color: #22d3ee; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
        .logo-icon { font-size: 24px; }
        .logo-sub { font-size: 11px; color: #6b7280; font-weight: 400; margin-bottom: 32px; }
        .nav-section { font-size: 11px; text-transform: uppercase; color: #6b7280; letter-spacing: 1px; margin: 20px 0 8px 0; }
        .nav-item { padding: 10px 14px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 2px; font-size: 14px; color: #9ca3af; }
        .nav-item:hover { background: #1f2937; color: #e5e7eb; }
        .nav-item.active { background: rgba(34, 211, 238, 0.15); color: #22d3ee; }
        .main { flex: 1; padding: 24px; overflow-y: auto; }
        .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .topbar h1 { font-size: 20px; font-weight: 600; }
        .select-box { background: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 10px 16px; color: #e5e7eb; font-size: 13px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .metric-card { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; }
        .metric-label { font-size: 12px; color: #6b7280; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { font-size: 28px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
        .metric-value.cyan { color: #22d3ee; }
        .metric-value.green { color: #22c55e; }
        .metric-value.yellow { color: #fbbf24; }
        .metric-value.purple { color: #a78bfa; }
        .metric-unit { font-size: 14px; color: #6b7280; font-weight: 400; }
        .metric-change { font-size: 12px; margin-top: 4px; color: #6b7280; }
        .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
        .chart-card { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; }
        .chart-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
        .chart-title span { font-size: 12px; color: #22d3ee; font-family: 'JetBrains Mono', monospace; }
        .wave-chart { height: 120px; display: flex; align-items: flex-end; gap: 2px; }
        .wave-bar { flex: 1; background: linear-gradient(to top, rgba(34, 211, 238, 0.2), rgba(34, 211, 238, 0.6)); border-radius: 2px 2px 0 0; min-width: 3px; }
        .gauge-container { display: flex; justify-content: space-around; padding: 20px 0; }
        .gauge { text-align: center; }
        .gauge-ring { width: 80px; height: 80px; border-radius: 50%; border: 6px solid #1f2937; position: relative; margin: 0 auto 10px; }
        .gauge-ring::after { content: attr(data-value); position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
        .gauge-ring.temp { border-color: #22c55e; color: #22c55e; border-top-color: #22c55e; border-right-color: #22c55e; }
        .gauge-ring.batt { border-color: #fbbf24; color: #fbbf24; border-top-color: #fbbf24; }
        .gauge-ring.signal { border-color: #22d3ee; color: #22d3ee; border-top-color: #22d3ee; border-right-color: #22d3ee; border-bottom-color: #22d3ee; }
        .gauge-label { font-size: 11px; color: #6b7280; }
        .data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
        .data-table th { text-align: left; padding: 10px 12px; color: #6b7280; font-weight: 500; border-bottom: 1px solid #1f2937; }
        .data-table td { padding: 10px 12px; border-bottom: 1px solid #1f2937; font-family: 'JetBrains Mono', monospace; }
        .signal-bar { display: flex; gap: 2px; align-items: flex-end; height: 16px; }
        .signal-segment { width: 4px; background: #22d3ee; border-radius: 1px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo"><span class="logo-icon">📡</span> GroundStation</div>
        <div class="logo-sub">Satellite Tracking Platform</div>
        <div class="nav-section">Tracking</div>
        <div class="nav-item">🗺️ Live Map</div>
        <div class="nav-item">🛰️ Satellites</div>
        <div class="nav-item">🔄 Passes</div>
        <div class="nav-section">Data</div>
        <div class="nav-item active">📊 Telemetry</div>
        <div class="nav-item">📈 Analytics</div>
        <div class="nav-item">💾 Recordings</div>
        <div class="nav-section">System</div>
        <div class="nav-item">⚙️ Ground Stations</div>
        <div class="nav-item">🔧 Configuration</div>
    </div>
    <div class="main">
        <div class="topbar">
            <h1>📊 Telemetry Dashboard</h1>
            <div style="display:flex;gap:12px;align-items:center;">
                <select class="select-box">
                    <option>🛰️ NOAA-19 (33591)</option>
                    <option>🛰️ ISS (25544)</option>
                    <option>🛰️ STARLINK-4201</option>
                </select>
                <div style="background:rgba(34, 197, 94, 0.15);color:#22c55e;padding:8px 16px;border-radius:8px;font-size:12px;">● Live Stream</div>
            </div>
        </div>
        <div class="grid">
            <div class="metric-card">
                <div class="metric-label">Signal Strength</div>
                <div class="metric-value cyan">-72.4 <span class="metric-unit">dBm</span></div>
                <div class="metric-change">↑ 2.1 dB from last pass</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Bit Error Rate</div>
                <div class="metric-value green">0.002<span class="metric-unit">%</span></div>
                <div class="metric-change">Within acceptable range</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Data Rate</div>
                <div class="metric-value yellow">1.7<span class="metric-unit"> Mbps</span></div>
                <div class="metric-change">APT 137.1 MHz NOAA</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Frames Decoded</div>
                <div class="metric-value purple">12,847</div>
                <div class="metric-change">+284 this session</div>
            </div>
        </div>
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">Signal Strength (Last 5 min) <span>-72.4 dBm</span></div>
                <div class="wave-chart" id="signal-chart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Doppler Shift <span>±4.2 kHz</span></div>
                <div class="wave-chart" id="doppler-chart"></div>
            </div>
        </div>
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">System Gauges</div>
                <div class="gauge-container">
                    <div class="gauge">
                        <div class="gauge-ring temp" data-value="42°C"></div>
                        <div class="gauge-label">LNA Temp</div>
                    </div>
                    <div class="gauge">
                        <div class="gauge-ring batt" data-value="87%"></div>
                        <div class="gauge-label">Battery</div>
                    </div>
                    <div class="gauge">
                        <div class="gauge-ring signal" data-value="94%"></div>
                        <div class="gauge-label">Signal Qual.</div>
                    </div>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Recent Telemetry Packets</div>
                <table class="data-table">
                    <thead>
                        <tr><th>Time (UTC)</th><th>Type</th><th>Value</th><th>Signal</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>14:32:07</td><td style="color:#22d3ee;">TEMP</td><td>42.3°C</td><td><div class="signal-bar"><div class="signal-segment" style="height:8px"></div><div class="signal-segment" style="height:12px"></div><div class="signal-segment" style="height:16px"></div><div class="signal-segment" style="height:14px"></div><div class="signal-segment" style="height:10px"></div></div></td></tr>
                        <tr><td>14:32:06</td><td style="color:#22c55e;">BATT</td><td>87.2%</td><td><div class="signal-bar"><div class="signal-segment" style="height:6px"></div><div class="signal-segment" style="height:10px"></div><div class="signal-segment" style="height:14px"></div><div class="signal-segment" style="height:12px"></div><div class="signal-segment" style="height:8px"></div></div></td></tr>
                        <tr><td>14:32:05</td><td style="color:#fbbf24;">PWR</td><td>14.2 W</td><td><div class="signal-bar"><div class="signal-segment" style="height:10px"></div><div class="signal-segment" style="height:14px"></div><div class="signal-segment" style="height:16px"></div><div class="signal-segment" style="height:16px"></div><div class="signal-segment" style="height:12px"></div></div></td></tr>
                        <tr><td>14:32:04</td><td style="color:#a78bfa;">SIG</td><td>-72.4 dBm</td><td><div class="signal-bar"><div class="signal-segment" style="height:8px"></div><div class="signal-segment" style="height:12px"></div><div class="signal-segment" style="height:16px"></div><div class="signal-segment" style="height:14px"></div><div class="signal-segment" style="height:10px"></div></div></td></tr>
                        <tr><td>14:32:03</td><td style="color:#22d3ee;">TEMP</td><td>42.1°C</td><td><div class="signal-bar"><div class="signal-segment" style="height:7px"></div><div class="signal-segment" style="height:11px"></div><div class="signal-segment" style="height:15px"></div><div class="signal-segment" style="height:13px"></div><div class="signal-segment" style="height:9px"></div></div></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <script>
        // Generate wave chart bars
        function generateWaveChart(id, variance) {
            const container = document.getElementById(id);
            for (let i = 0; i < 60; i++) {
                const bar = document.createElement('div');
                bar.className = 'wave-bar';
                const height = 30 + Math.sin(i * 0.3) * 20 + (Math.random() * variance);
                bar.style.height = Math.max(10, Math.min(100, height)) + '%';
                container.appendChild(bar);
            }
        }
        generateWaveChart('signal-chart', 15);
        generateWaveChart('doppler-chart', 25);
    </script>
</body>
</html>
"""

# Passes mockup
PASSES_HTML = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroundStation - Satellite Passes</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #030712; color: #e5e7eb; height: 100vh; display: flex; }
        .sidebar { width: 260px; background: #111827; padding: 20px; border-right: 1px solid #1f2937; }
        .logo { font-size: 18px; font-weight: 700; color: #22d3ee; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
        .logo-icon { font-size: 24px; }
        .logo-sub { font-size: 11px; color: #6b7280; font-weight: 400; margin-bottom: 32px; }
        .nav-section { font-size: 11px; text-transform: uppercase; color: #6b7280; letter-spacing: 1px; margin: 20px 0 8px 0; }
        .nav-item { padding: 10px 14px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 2px; font-size: 14px; color: #9ca3af; }
        .nav-item:hover { background: #1f2937; color: #e5e7eb; }
        .nav-item.active { background: rgba(34, 211, 238, 0.15); color: #22d3ee; }
        .main { flex: 1; padding: 24px; overflow-y: auto; }
        .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .topbar h1 { font-size: 20px; font-weight: 600; }
        .tabs { display: flex; gap: 4px; background: #111827; padding: 4px; border-radius: 10px; }
        .tab { padding: 8px 16px; border-radius: 8px; font-size: 13px; cursor: pointer; color: #6b7280; }
        .tab.active { background: #1f2937; color: #22d3ee; }
        .pass-list { display: flex; flex-direction: column; gap: 12px; }
        .pass-card { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; display: flex; gap: 20px; align-items: center; }
        .pass-card.next { border-color: rgba(34, 211, 238, 0.3); background: rgba(34, 211, 238, 0.05); }
        .pass-time { min-width: 100px; text-align: center; }
        .pass-time-label { font-size: 11px; color: #6b7280; margin-bottom: 4px; }
        .pass-time-value { font-size: 18px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
        .pass-time-countdown { font-size: 12px; color: #22d3ee; margin-top: 4px; }
        .pass-info { flex: 1; }
        .pass-satellite { font-size: 16px; font-weight: 600; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
        .pass-details { display: flex; gap: 24px; font-size: 13px; color: #9ca3af; }
        .pass-detail { display: flex; align-items: center; gap: 6px; }
        .pass-duration { min-width: 120px; }
        .duration-bar-bg { height: 8px; background: #1f2937; border-radius: 4px; overflow: hidden; margin-top: 6px; }
        .duration-bar { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #22d3ee, #06b6d4); }
        .pass-actions { display: flex; gap: 8px; }
        .btn { padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; border: none; }
        .btn-primary { background: #22d3ee; color: #030712; }
        .btn-secondary { background: #1f2937; color: #e5e7eb; border: 1px solid #374151; }
        .elevation-chart { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; margin-top: 16px; }
        .chart-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; }
        .elevation-visual { height: 100px; position: relative; border-bottom: 1px solid #1f2937; }
        .horizon-line { position: absolute; bottom: 0; left: 0; right: 0; border-top: 1px dashed #374151; }
        .elevation-label { position: absolute; left: 8px; font-size: 10px; color: #6b7280; }
        .elevation-curve { position: absolute; bottom: 0; left: 0; right: 0; height: 100%; }
        .legend { display: flex; gap: 20px; margin-top: 12px; font-size: 12px; color: #6b7280; }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .legend-dot { width: 8px; height: 8px; border-radius: 50%; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo"><span class="logo-icon">📡</span> GroundStation</div>
        <div class="logo-sub">Satellite Tracking Platform</div>
        <div class="nav-section">Tracking</div>
        <div class="nav-item">🗺️ Live Map</div>
        <div class="nav-item">🛰️ Satellites</div>
        <div class="nav-item active">🔄 Passes</div>
        <div class="nav-section">Data</div>
        <div class="nav-item">📊 Telemetry</div>
        <div class="nav-item">📈 Analytics</div>
        <div class="nav-item">💾 Recordings</div>
        <div class="nav-section">System</div>
        <div class="nav-item">⚙️ Ground Stations</div>
        <div class="nav-item">🔧 Configuration</div>
    </div>
    <div class="main">
        <div class="topbar">
            <h1>🔄 Satellite Passes</h1>
            <div class="tabs">
                <div class="tab active">Upcoming</div>
                <div class="tab">Today</div>
                <div class="tab">7 Days</div>
                <div class="tab">Calendar</div>
            </div>
        </div>
        <div class="pass-list">
            <div class="pass-card next">
                <div class="pass-time">
                    <div class="pass-time-label">AOS</div>
                    <div class="pass-time-value" style="color:#22d3ee;">14:44</div>
                    <div class="pass-time-countdown">in 12m 07s</div>
                </div>
                <div class="pass-info">
                    <div class="pass-satellite">🛰️ ISS (ZARYA) <span style="background:rgba(34, 197, 94, 0.15);color:#22c55e;padding:3px 10px;border-radius:12px;font-size:11px;">● Next</span></div>
                    <div class="pass-details">
                        <div class="pass-detail">📍 Max El: <strong style="color:#e5e7eb;">72°</strong></div>
                        <div class="pass-detail">🧭 Direction: <strong style="color:#e5e7eb;">NW → SE</strong></div>
                        <div class="pass-detail">📡 Frequency: <strong style="color:#e5e7eb;">145.825 MHz</strong></div>
                    </div>
                </div>
                <div class="pass-duration">
                    <div style="font-size:12px;color:#6b7280;">Duration</div>
                    <div style="font-size:16px;font-weight:600;font-family:'JetBrains Mono',monospace;">6m 42s</div>
                    <div class="duration-bar-bg"><div class="duration-bar" style="width:85%;"></div></div>
                </div>
                <div class="pass-actions">
                    <button class="btn btn-primary">📡 Track</button>
                    <button class="btn btn-secondary">🔔 Alert</button>
                </div>
            </div>
            <div class="pass-card">
                <div class="pass-time">
                    <div class="pass-time-label">AOS</div>
                    <div class="pass-time-value">15:23</div>
                    <div class="pass-time-countdown" style="color:#6b7280;">in 51m 07s</div>
                </div>
                <div class="pass-info">
                    <div class="pass-satellite">🛰️ NOAA-19</div>
                    <div class="pass-details">
                        <div class="pass-detail">📍 Max El: <strong style="color:#e5e7eb;">48°</strong></div>
                        <div class="pass-detail">🧭 Direction: <strong style="color:#e5e7eb;">W → E</strong></div>
                        <div class="pass-detail">📡 Frequency: <strong style="color:#e5e7eb;">137.100 MHz</strong></div>
                    </div>
                </div>
                <div class="pass-duration">
                    <div style="font-size:12px;color:#6b7280;">Duration</div>
                    <div style="font-size:16px;font-weight:600;font-family:'JetBrains Mono',monospace;">14m 18s</div>
                    <div class="duration-bar-bg"><div class="duration-bar" style="width:100%;"></div></div>
                </div>
                <div class="pass-actions">
                    <button class="btn btn-secondary">📡 Track</button>
                    <button class="btn btn-secondary">🔔 Alert</button>
                </div>
            </div>
            <div class="pass-card">
                <div class="pass-time">
                    <div class="pass-time-label">AOS</div>
                    <div class="pass-time-value">16:08</div>
                    <div class="pass-time-countdown" style="color:#6b7280;">in 1h 36m</div>
                </div>
                <div class="pass-info">
                    <div class="pass-satellite">🛰️ STARLINK-4201</div>
                    <div class="pass-details">
                        <div class="pass-detail">📍 Max El: <strong style="color:#e5e7eb;">31°</strong></div>
                        <div class="pass-detail">🧭 Direction: <strong style="color:#e5e7eb;">SW → NE</strong></div>
                        <div class="pass-detail">📡 Frequency: <strong style="color:#e5e7eb;">137.500 MHz</strong></div>
                    </div>
                </div>
                <div class="pass-duration">
                    <div style="font-size:12px;color:#6b7280;">Duration</div>
                    <div style="font-size:16px;font-weight:600;font-family:'JetBrains Mono',monospace;">4m 52s</div>
                    <div class="duration-bar-bg"><div class="duration-bar" style="width:58%;"></div></div>
                </div>
                <div class="pass-actions">
                    <button class="btn btn-secondary">📡 Track</button>
                    <button class="btn btn-secondary">🔔 Alert</button>
                </div>
            </div>
            <div class="pass-card">
                <div class="pass-time">
                    <div class="pass-time-label">AOS</div>
                    <div class="pass-time-value">17:45</div>
                    <div class="pass-time-countdown" style="color:#6b7280;">in 3h 13m</div>
                </div>
                <div class="pass-info">
                    <div class="pass-satellite">🛰️ TIANGONG</div>
                    <div class="pass-details">
                        <div class="pass-detail">📍 Max El: <strong style="color:#e5e7eb;">56°</strong></div>
                        <div class="pass-detail">🧭 Direction: <strong style="color:#e5e7eb;">S → N</strong></div>
                        <div class="pass-detail">📡 Frequency: <strong style="color:#e5e7eb;">145.800 MHz</strong></div>
                    </div>
                </div>
                <div class="pass-duration">
                    <div style="font-size:12px;color:#6b7280;">Duration</div>
                    <div style="font-size:16px;font-weight:600;font-family:'JetBrains Mono',monospace;">8m 14s</div>
                    <div class="duration-bar-bg"><div class="duration-bar" style="width:72%;"></div></div>
                </div>
                <div class="pass-actions">
                    <button class="btn btn-secondary">📡 Track</button>
                    <button class="btn btn-secondary">🔔 Alert</button>
                </div>
            </div>
        </div>
        <div class="elevation-chart">
            <div class="chart-title">ISS Pass Elevation Profile — 14:44 to 14:51 UTC</div>
            <div class="elevation-visual">
                <div class="elevation-label" style="bottom:80%;">90°</div>
                <div class="elevation-label" style="bottom:60%;">60°</div>
                <div class="elevation-label" style="bottom:40%;">42°</div>
                <div class="elevation-label" style="bottom:20%;">30°</div>
                <div class="elevation-label" style="bottom:0;">0°</div>
                <svg viewBox="0 0 400 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%;">
                    <defs>
                        <linearGradient id="elevGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="rgba(34, 211, 238, 0.3)"/>
                            <stop offset="100%" stop-color="rgba(34, 211, 238, 0)"/>
                        </linearGradient>
                    </defs>
                    <path d="M0,100 L20,95 L40,85 L60,70 L80,50 L100,30 L120,18 L140,10 L160,8 L180,12 L200,22 L220,38 L240,55 L260,70 L280,82 L300,90 L320,95 L340,98 L400,100" fill="url(#elevGrad)" stroke="#22d3ee" stroke-width="2"/>
                    <circle cx="160" cy="8" r="4" fill="#22d3ee"/>
                    <text x="165" y="8" fill="#22d3ee" font-size="10" font-family="JetBrains Mono">72°</text>
                </svg>
            </div>
            <div class="legend">
                <div class="legend-item"><div class="legend-dot" style="background:#22d3ee;"></div> ISS (ZARYA)</div>
                <div class="legend-item">📍 AOS: 14:44:12 UTC</div>
                <div class="legend-item">📍 TCA: 14:47:48 UTC (Max El: 72°)</div>
                <div class="legend-item">📍 LOS: 14:50:54 UTC</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def capture_screenshots():
    """Capture GroundStation screenshots using HTML mockups.
    
    Note: These are representative mockups, not screenshots from the running application.
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # 1. Capture tracker
        print("Capturing tracker...")
        page.set_content(TRACKER_HTML)
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.screenshot(path=f"{SCREENSHOT_DIR}/tracker.png", full_page=False)
        size = os.path.getsize(f"{SCREENSHOT_DIR}/tracker.png")
        print(f"  Saved: tracker.png ({size:,} bytes)")
        
        # 2. Capture telemetry
        print("Capturing telemetry...")
        page.set_content(TELEMETRY_HTML)
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.screenshot(path=f"{SCREENSHOT_DIR}/telemetry.png", full_page=False)
        size = os.path.getsize(f"{SCREENSHOT_DIR}/telemetry.png")
        print(f"  Saved: telemetry.png ({size:,} bytes)")
        
        # 3. Capture passes
        print("Capturing passes...")
        page.set_content(PASSES_HTML)
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.screenshot(path=f"{SCREENSHOT_DIR}/passes.png", full_page=False)
        size = os.path.getsize(f"{SCREENSHOT_DIR}/passes.png")
        print(f"  Saved: passes.png ({size:,} bytes)")
        
        browser.close()
    
    print(f"\nScreenshots saved to {SCREENSHOT_DIR}/")

if __name__ == "__main__":
    capture_screenshots()
