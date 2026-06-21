# GroundStation — Satellite Telemetry & SDR Ground Station

**Version:** v1.0  
**Status:** Active Development  
**Repository:** https://github.com/OneByJorah/GroundStation

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Service Management](#service-management)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

GroundStation is an end-to-end satellite ground station suite for Software Defined Radio (SDR), radio/rotator control, audio streaming, and satellite image handling. It combines a FastAPI/SocketIO backend with a Vite + React frontend, plus database-backed telemetry and WebRTC video paths.

Designed for ham radio, satellite tracking, and experimental space communications.

---

## Architecture

Client browser → Vite frontend ↔ SocketIO/WebRTC → FastAPI backend (`server/`) → hardware controllers (`controllers/sdr`, `rig`, `rotator`) + audio pipeline (`audio/`) + database (`alembic` migrations).

Configuration and runtime constants are centralized under `backend/common/` and `backend/constants/`.

---

## Technology Stack

| Layer | Stack |
|---|---|
| Runtime | Linux (Ubuntu 22.04+) |
| Backend | Python / FastAPI / Uvicorn / SocketIO |
| Frontend | Vite + React |
| Hardware | SDR (via `controllers/sdr.py`), ham radio (`rig`), rotator (`rotatorhamlib`) |
| Audio | Deepgram / Gemini transcription workers, streaming |
| Database | SQLAlchemy + Alembic |
| CI/CD | Drone (`.drone.yml`) |
| VCS | Git + GitHub (`github.com/OneByJorah/GroundStation`) |

---

## Features

- **SDR control**: live spectrum and sample capture via `controllers/sdr.py`.
- **Radio + rotator**: hamlib integration for rig and rotator control.
- **Audio streaming + transcription**: Deepgram/Gemini workers for voice.
- **Telemetry + WebRTC**: SocketIO event bus and WebRTC video routes.
- **Satellite images**: captured imagery stored under `backend/satimages/`.
- **Database migrations**: `alembic`-managed schema.
- **Docker build**: `Dockerfile` + `.drone.yml` for containerized CI.

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/OneByJorah/GroundStation.git
cd GroundStation

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
pip install -e ".[dev]"
python app.py --host 0.0.0.0 --port 5000

# 3. Frontend (in a second terminal)
cd frontend
npm install
npm run dev
```

> Hardware (SDR, rig, rotator) requires platform-specific drivers and USB access.

---

## Service Management

```bash
# Docker (when available)
docker build -t groundstation .
docker run --rm -it --device /dev/bus/usb groundstation

# Local dev
python backend/app.py --host 0.0.0.0 --port 5000
```

---

## Project Structure

```
GroundStation/
├── backend/
│   ├── app.py
│   ├── alembic/                 # DB migrations
│   ├── audio/                   # Streaming + transcription
│   ├── common/                  # Config, logging, auth
│   ├── constants/               # Framing, modulations
│   ├── controllers/             # SDR, rotator, rig
│   ├── handlers/
│   ├── satimages/               # Captured satellite images
│   └── server/                  # FastAPI + SocketIO + WebRTC
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile / build files
├── Dockerfile
├── .drone.yml
└── README.md
```

---

## Screenshots

_(Screenshots will be added after hardware-backed build/run capture.)_

---

## Contributing

1. Create a feature branch off `main`.
2. Follow the existing code style and pre-commit hooks (`.pre-commit-config.yaml`).
3. Test hardware code paths on real SDR/rig/rotator hardware before submitting.

---

## License

GPL-3.0-only (frontend), MIT (unless otherwise noted in LICENSE)

---

## Author

Built by **Jhonattan L. Jimenez**.
