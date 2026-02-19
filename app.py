from flask import Flask, render_template_string
from datetime import datetime
import platform
import os

app = Flask(__name__)

VERSION = "v1.0.0"
REGISTRY = os.environ.get("ACR_REGISTRY", "miregistroarc2025xk7.azurecr.io")
EMPRESA = os.environ.get("EMPRESA", "Equipo de Infraestructura")
REGION = os.environ.get("REGION", "East US")

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ACR · Estado del Servicio</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:       #050A14;
      --surface:  #0D1623;
      --border:   #1A2D4A;
      --accent:   #00C2FF;
      --accent2:  #00FF94;
      --text:     #E8F4FF;
      --muted:    #4A6A8A;
      --ok:       #00FF94;
      --mono:     'Space Mono', monospace;
      --sans:     'Syne', sans-serif;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      overflow-x: hidden;
    }

    /* Grid background */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(0,194,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,194,255,0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    /* Glow blobs */
    body::after {
      content: '';
      position: fixed;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0,194,255,0.06) 0%, transparent 70%);
      top: -200px;
      right: -200px;
      pointer-events: none;
      z-index: 0;
    }

    .wrapper {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 780px;
    }

    /* Header */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2.5rem;
      animation: fadeDown 0.6s ease both;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .logo-icon {
      width: 40px;
      height: 40px;
      border: 2px solid var(--accent);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      color: var(--accent);
      animation: pulse 3s ease-in-out infinite;
    }

    .logo-text {
      font-size: 0.75rem;
      font-family: var(--mono);
      color: var(--muted);
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }

    .status-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(0,255,148,0.08);
      border: 1px solid rgba(0,255,148,0.25);
      border-radius: 999px;
      padding: 0.35rem 1rem;
      font-family: var(--mono);
      font-size: 0.72rem;
      color: var(--ok);
      letter-spacing: 0.1em;
    }

    .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--ok);
      animation: blink 1.5s ease-in-out infinite;
    }

    /* Hero */
    .hero {
      margin-bottom: 2.5rem;
      animation: fadeDown 0.6s 0.1s ease both;
    }

    .hero h1 {
      font-size: clamp(2rem, 5vw, 3.2rem);
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 0.75rem;
    }

    .hero h1 span {
      color: var(--accent);
    }

    .hero p {
      color: var(--muted);
      font-size: 0.95rem;
      font-family: var(--mono);
    }

    /* Cards grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin-bottom: 1rem;
      animation: fadeUp 0.6s 0.2s ease both;
    }

    .grid-3 {
      grid-template-columns: repeat(3, 1fr);
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      transition: border-color 0.2s, transform 0.2s;
    }

    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
    }

    .card-label {
      font-family: var(--mono);
      font-size: 0.65rem;
      color: var(--muted);
      letter-spacing: 0.15em;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
    }

    .card-value {
      font-size: 1rem;
      font-weight: 600;
      color: var(--text);
      word-break: break-all;
    }

    .card-value.accent { color: var(--accent); }
    .card-value.ok     { color: var(--ok); }
    .card-value.mono   { font-family: var(--mono); font-size: 0.85rem; }

    /* Full width card */
    .card-full {
      grid-column: 1 / -1;
    }

    /* Registry bar */
    .registry-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1rem;
      animation: fadeUp 0.6s 0.3s ease both;
    }

    .registry-bar .card-label { margin-bottom: 0.4rem; }

    .registry-url {
      font-family: var(--mono);
      font-size: 0.9rem;
      color: var(--accent);
      letter-spacing: 0.02em;
    }

    /* Footer */
    footer {
      text-align: center;
      font-family: var(--mono);
      font-size: 0.68rem;
      color: var(--muted);
      margin-top: 2rem;
      letter-spacing: 0.08em;
      animation: fadeUp 0.6s 0.4s ease both;
    }

    /* Animations */
    @keyframes fadeDown {
      from { opacity: 0; transform: translateY(-16px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50%       { opacity: 0.3; }
    }
    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(0,194,255,0.3); }
      50%       { box-shadow: 0 0 0 8px rgba(0,194,255,0); }
    }

    @media (max-width: 540px) {
      .grid, .grid-3 { grid-template-columns: 1fr; }
      .card-full { grid-column: 1; }
    }
  </style>
</head>
<body>
  <div class="wrapper">

    <header>
      <div class="logo">
        <div class="logo-icon">⬡</div>
        <span class="logo-text">Azure Container Registry</span>
      </div>
      <div class="status-pill">
        <div class="dot"></div>
        OPERACIONAL
      </div>
    </header>

    <div class="hero">
      <h1>Servicio <span>activo</span><br>y corriendo.</h1>
      <p>// Imagen desplegada correctamente desde ACR</p>
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-label">Estado</div>
        <div class="card-value ok">✓ OK</div>
      </div>
      <div class="card">
        <div class="card-label">Version</div>
        <div class="card-value accent mono">{{ version }}</div>
      </div>
    </div>

    <div class="grid grid-3">
      <div class="card">
        <div class="card-label">Empresa</div>
        <div class="card-value">{{ empresa }}</div>
      </div>
      <div class="card">
        <div class="card-label">Region</div>
        <div class="card-value mono">{{ region }}</div>
      </div>
      <div class="card">
        <div class="card-label">Runtime</div>
        <div class="card-value mono">{{ runtime }}</div>
      </div>
    </div>

    <div class="grid" style="margin-top: 1rem;">
      <div class="card card-full">
        <div class="card-label">Fecha y hora del servidor</div>
        <div class="card-value mono accent">{{ fecha }}</div>
      </div>
    </div>

    <div class="registry-bar" style="margin-top: 1rem;">
      <div class="card-label">Registry</div>
      <div class="registry-url">{{ registry }}</div>
    </div>

    <footer>
      AZURE CONTAINER REGISTRY &nbsp;·&nbsp; {{ version }} &nbsp;·&nbsp; {{ empresa }}
    </footer>

  </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML,
        version=VERSION,
        registry=REGISTRY,
        empresa=EMPRESA,
        region=REGION,
        runtime=f"Python {platform.python_version()}",
        fecha=datetime.now().strftime("%Y-%m-%d  %H:%M:%S UTC")
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)