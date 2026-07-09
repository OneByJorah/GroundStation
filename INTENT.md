# INTENT.md — J1-PIPELINE Phase -1 (ORACLE)

**Repository:** `OneByJorah/GroundStation`
**Analysis Date:** 2026-07-05
**Analyst:** J1-PIPELINE ORACLE (read-only)
**Status:** Intent Reconstructed

---

## What This System Does

GroundStation is an end-to-end satellite ground station suite for Software Defined Radio (SDR), ham radio/rotator control, audio streaming, satellite image handling, and telemetry decoding. It combines a **FastAPI/SocketIO Python backend** with a **Vite + React frontend**, plus database-backed telemetry, WebRTC video paths, and AI-powered audio transcription.

### Service Table

| Layer | Technology | Role |
|---|---|---|
| **Backend** | Python 3.12 / FastAPI / Uvicorn / SocketIO | API server, real-time event bus, hardware control |
| **Frontend** | Vite + React 19 / MUI / Redux / Leaflet | Web UI: waterfall, maps, scheduler, telemetry viewer |
| **Database** | SQLAlchemy + Alembic (SQLite) | Persistent storage: satellites, TLEs, observations, config |
| **SDR Control** | SoapySDR, UHD, RTL-SDR, Airspy, HackRF, LimeSDR, SDRplay, HydraSDR | Multi-vendor SDR hardware abstraction |
| **DSP** | GNU Radio 3.10, gr-satellites, gr-lora_sdr, SatDump | Signal demodulation and decoding |
| **Audio** | Deepgram / Gemini transcription workers | AI-powered voice-to-text from radio audio |
| **Rig/Rotator** | Hamlib integration | Physical radio and antenna rotator control |
| **CI/CD** | Drone CI + GitHub Actions | Multi-arch Docker builds (amd64 + arm64) |
| **Container** | Docker (multi-stage, multi-arch) | Production deployment on x86 and ARM (RPi5, Jetson) |

### Operational Role

The system is deployed as a Docker container running on dedicated ground station hardware (AMD64 server and/or ARM64 Raspberry Pi 5 / Jetson Orin). It provides a web-accessible control panel for:

- **Live SDR operation**: Waterfall display, VFO control, demodulation, recording
- **Satellite tracking**: Automated antenna rotator pointing with doppler correction
- **Scheduled observations**: Auto-generate observation windows from TLE data, resolve conflicts, execute passes
- **Signal decoding**: LoRa, AFSK, BPSK, GMSK, FSK, SSTV, Morse, AM, FM, SSB
- **Telemetry analysis**: Hex/ASCII/float32/integer viewers for decoded satellite telemetry
- **Audio streaming + transcription**: Real-time AI transcription via Deepgram/Gemini
- **File browser**: Browse/manage IQ recordings (SigMF), snapshots, decoded data
- **Multi-language UI**: English, German, Greek, Spanish, French, Italian, Dutch

---

## Why This Was Built

### Real Problem

Operating a satellite ground station requires orchestrating a complex stack of hardware and software: SDR receivers, antenna rotators, ham radio transceivers, demodulators, decoders, TLE-based pass prediction, doppler correction, and data recording. Before GroundStation, an operator had to cobble together multiple standalone tools — GQRX for SDR visualization, SatDump for decoding, GPredict for tracking, custom scripts for scheduling, and separate tools for telemetry analysis — none of which talked to each other or provided a unified web interface.

The core pain points were:

1. **No unified scheduling**: Existing tools couldn't automatically generate observation windows from TLE data, resolve hardware conflicts (same SDR/rotator needed for overlapping passes), and execute them unattended.
2. **No multi-session tracking**: You couldn't track multiple satellites simultaneously on different VFOs of the same SDR stream.
3. **No web-based remote operation**: Most ground station software was desktop-only (GQRX, SDR#, SatDump GUI), making remote/headless operation difficult.
4. **No integrated AI transcription**: Audio from radio passes had to be recorded and processed separately.
5. **No unified telemetry viewer**: Decoded telemetry was scattered across files and formats.
6. **No containerized deployment**: Setting up the full SDR/DSP stack (UHD, SoapySDR, GNU Radio, SatDump, Hamlib) was a multi-hour manual process per machine.

### Why Existing Tools Were Insufficient

| Tool | Gap |
|---|---|
| **GQRX** | Desktop-only, no tracking, no scheduling, no decoding pipeline |
| **SatDump (standalone)** | CLI/GUI only, no web UI, no integrated scheduler, no multi-session |
| **GPredict** | Tracking only — no SDR control, no recording, no decoding |
| **GNU Radio flowgraphs** | Custom per-use-case, no persistent UI, no scheduling |
| **SDR# / SDR Console** | Windows-only, no headless operation, no API |
| **OpenWebRX** | Web-based SDR but limited to single-user RX, no rotator control, no scheduling |
| **Wireshark / custom decoders** | Post-processing only, no real-time integration |

### What Triggered Development

The initial commit message is simply "first commit" — no explicit trigger documented. However, the repo's evolution (3,262 commits, 40+ tagged releases from v0.1.0 through v0.7.10) and the breadth of integrated technologies suggest it was built to serve as the primary ground station software for a **dedicated satellite ground station installation** — likely the author's (Efstratios Goudelis / sgoudelis) personal station, later adopted into the OneByJorah ecosystem.

The Drone CI pipeline reveals two physical deployment targets:
- **AMD64 host** at `192.168.60.98` (primary server)
- **ARM64 host** (RPi5) at `192.168.60.52` (secondary/edge node)

This confirms the system is actively deployed on real hardware, not just a development project.

### Ecosystem Fit

```
JorahOne Ecosystem
├── GroundStation          ← THIS REPO — Satellite ground station suite
├── EdgeRouter             (related network/infrastructure)
├── ADSentinel             (related security/monitoring)
└── [other OneByJorah repos]
```

GroundStation is the **satellite communications and RF observation** pillar of the JorahOne ecosystem. It fills the gap between infrastructure (EdgeRouter), security (ADSentinel), and the physical RF layer — providing the hardware control, signal processing, and data collection pipeline for space-based communications.

---

## Operational Classification

**Classification: BETA → PRODUCTION** (actively deployed on production hardware)

**Evidence:**
- **Versioned releases**: 40+ tagged releases (v0.1.0 through v0.7.10), semantic versioning
- **Active CI/CD**: Drone CI pipeline building and deploying to two physical hosts (AMD64 + ARM64) on push and tag events
- **GitHub Actions**: Tests (backend pytest + frontend vitest + Playwright E2E), CodeQL security scanning, Docker release workflow
- **Dependabot**: Weekly dependency updates for pip, npm, docker, and GitHub Actions
- **Pre-commit hooks**: Black, isort, flake8, mypy, ESLint — enforced code quality
- **Security policy**: SECURITY.md with 48-hour response SLA, 90-day disclosure timeline
- **Security audit history**: Commits for email sanitization and path traversal prevention
- **Docker multi-arch**: Production images published to GHCR for both amd64 and arm64
- **Health checks**: Container startup verification in CI pipeline
- **Persistent data volume**: Docker volume mount for database, recordings, snapshots
- **Production deployment**: Two physical hosts running the container with `--restart=unless-stopped`
- **i18n**: 6 languages supported (en, de, el, es, fr, it, nl)
- **E2E tests**: Playwright-based end-to-end tests against a real backend container
- **Coverage tracking**: Codecov integration for both backend and frontend

**Classification caveat**: The pyproject.toml declares `Development Status :: 4 - Beta`, and the README says "Active Development." The system is deployed in production but still under active development — typical for a ground station that evolves with new satellites and modulation types.

---

## Key Architectural Decisions

1. **SDR center frequency is static during tracking** — Users set the SDR center frequency once; doppler correction is applied via VFO software windows, not hardware retuning. This enables multi-session tracking (multiple satellites on the same SDR stream).

2. **Dual VOLK library strategy** — Two versions of VOLK coexist in the Docker image: system libvolk (for SatDump) and VOLK 3.2 compiled to `/opt/volk` (for GNU Radio). This avoids symbol conflicts between SatDump's Planck constant macros and VOLK 3.2's `c1/c2` variables.

3. **All SDR drivers compiled from source in Docker** — UHD, SoapySDR, SoapySDR modules (RTLSDR, Airspy, HackRF, UHD, SDRplay, HydraSDR), GNU Radio, gr-satellites, gr-lora_sdr, SatDump, LimeSuite — all built in the Dockerfile. This ensures reproducible builds across architectures.

4. **Host networking for mDNS discovery** — The container uses `--network host` to enable Avahi mDNS discovery of SoapySDR remote servers on the LAN.

5. **SQLite with Alembic migrations** — Single-file database with versioned schema migrations, auto-applied on container startup.

6. **SocketIO real-time event bus** — All hardware state, tracking data, FFT data, and audio streams flow through SocketIO events, enabling the React frontend to update in real time.

7. **Auth removed** — User authentication was explicitly removed from the system (auth.py states "User authentication has been removed from the system"). The system is designed for trusted-network operation.

8. **GNU Radio mmap-based buffers** — Configured to use `vmcirc_mmap_tmpfile` instead of SysV shared memory to prevent `shmget` exhaustion in Docker.

9. **Multi-arch CI/CD** — Drone CI builds and deploys to both amd64 and arm64 targets simultaneously, with separate Docker registries and tags.

10. **SatDump commit pinning** — SatDump is pinned to a specific commit (`7aef0fe8441bc3eb440b1b6ba053556da5e40991`) to prevent upstream CLI/behavior changes from breaking decoding.

---

## Repository Structure

```
GroundStation/
├── backend/
│   ├── app.py                          # Entry point — FastAPI + SocketIO server
│   ├── alembic/                        # Database migrations (20+ migration files)
│   ├── audio/                          # Audio streaming + AI transcription workers
│   ├── common/                         # Config, logging, auth, constants, SDR config
│   ├── constants/                      # Framing, modulation type definitions
│   ├── controllers/                    # SDR, rig (hamlib), rotator (hamlib) control
│   ├── crud/                           # Database CRUD operations
│   ├── data/                           # Persistent data mount point (README placeholder)
│   ├── db/                             # SQLAlchemy models + migration runner
│   ├── demodulators/                   # 15+ demodulator/decoder implementations
│   ├── docs/                           # External protocol documentation (PDF)
│   ├── fft/                            # FFT processing, averaging, waterfall generation
│   ├── handlers/                       # SocketIO event handlers + routing
│   ├── hardware/                       # SDR hardware enumeration/probing
│   ├── monitoring/                     # Performance monitoring
│   ├── observations/                   # Observation scheduling, execution, conflict resolution
│   ├── pipeline/                       # Signal processing pipeline (managers, orchestration, registries, streaming)
│   ├── satconfig/                      # Satellite configuration
│   ├── satimages/                      # Captured satellite images (NORAD ID PNGs)
│   ├── pyproject.toml                  # Python project config
│   ├── requirements.txt                # Production dependencies
│   ├── requirements-dev.txt            # Dev/testing dependencies
│   ├── startup.sh                      # Container startup script
│   └── satellite-norad-lookup.json    # NORAD ID → satellite name mapping
├── frontend/
│   ├── src/
│   │   ├── components/                 # React components (waterfall, scheduler, target, etc.)
│   │   ├── i18n/                       # Internationalization (6 languages)
│   │   ├── hooks/                      # Custom React hooks
│   │   ├── services/                   # Data sync services
│   │   ├── utils/                      # Doppler calculator, date-time, etc.
│   │   └── themes/                     # Theme configurations
│   ├── package.json
│   ├── vite.config.js
│   └── vitest.config.js
├── Dockerfile                          # Multi-stage Docker build (497 lines)
├── .drone.yml                          # Drone CI pipeline (305 lines)
├── .github/
│   ├── workflows/                      # GitHub Actions (tests, CodeQL, release)
│   ├── dependabot.yml
│   └── ISSUE_TEMPLATE/                 # Bug report + feature request templates
├── .pre-commit-config.yaml
├── SECURITY.md
├── LICENSE                             # GPL-3.0
└── README.md
```

---

## Notes

- **Author discrepancy**: The README credits "Jhonattan L. Jimenez" as the author, but all code copyright headers and the pyproject.toml author field credit "Efstratios Goudelis" (sgoudelis). The Drone CI pipeline also references `sgoudelis` as the Docker Hub/GHCR user. This suggests the repo was forked or transferred into the OneByJorah organization from the original author's personal account.
- **Auth removed**: User authentication was explicitly stripped from the system. The system operates without authentication, intended for trusted-network environments.
- **No docker-compose.yml**: Despite being Docker-deployed, there is no docker-compose file. Deployment is managed via raw `docker run` commands in CI/CD.
- **No docs/ directory at repo root**: Documentation is limited to the README, inline code comments, and the Alembic migration guide. No formal architecture docs exist outside the codebase.
- **Hamlib compilation commented out**: The Dockerfile has Hamlib compilation commented out, suggesting it's installed via the system package manager or not currently needed.
- **csdr/pycsdr compilation commented out**: Similarly commented out in the Dockerfile — these may have been replaced by GNU Radio or SatDump.
- **Dependabot ecosystem alignment**: Dependabot is configured for pip, npm, docker, and GitHub Actions — all of which have corresponding files in the repo. No ecosystem mismatch.
- **Security audit commits**: Two security-related commits found — email sanitization and path traversal prevention — indicating proactive security maintenance.
- **3,262 commits** across the full history, with 40+ tagged releases — a mature, actively maintained project.
