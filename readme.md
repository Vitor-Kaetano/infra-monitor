# 🖥️ Infra Monitor

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20(systemd)-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📌 Overview

Infra Monitor is a lightweight and configurable monitoring tool built in Python for Linux environments (Fedora/RHEL-based).

It collects system metrics, validates service states, and checks network availability, generating structured logs for troubleshooting and observability.

---

## 🎯 Motivation

This project was developed to simulate real-world responsibilities of a **Junior Infrastructure Analyst**, focusing on:

- Linux system monitoring
- Service validation using systemd
- Network availability checks
- Automation using Python
- Clean and modular code design

---

## ⚙️ Features

### 📊 Resource Monitoring
- CPU usage
- Memory usage
- Disk usage

### 🔧 Service Validation
- Uses `systemctl` to check real service state
- Handles inactive, failed, and unknown services

### 🌐 Network Checks
- TCP port validation using sockets
- Ensures services are reachable

### 📁 Logging
- Human-readable terminal output
- Structured JSON logs (one entry per line)

### ⚡ Configurable
- No hardcoding
- Uses external JSON config

---

## 📂 Project Structure

```
infra-monitor/
├── monitor.py
├── config.json
├── monitor.json
├── requirements.txt
└── README.md
```

---

## 🧾 Configuration

All parameters are defined in `config.json`.

### Example:

```json
{
  "services": ["sshd", "docker"],
  "ports": [22, 80, 443],
  "thresholds": {
    "cpu": {"warning": 70, "critical": 85},
    "memory": {"warning": 70, "critical": 85},
    "disk": {"warning": 80, "critical": 90}
  }
}
```

---

## ▶️ Usage

### Run with default config:

```bash
python monitor.py
```

### Run with custom config:

```bash
python monitor.py custom_config.json
```

---

## 📤 Example Output

### Terminal

```
2026-04-03T12:50:00 | [OK] CPU: 25%
2026-04-03T12:50:00 | [WARNING] MEMORY: 72%
2026-04-03T12:50:00 | [OK] DISK: 60%
2026-04-03T12:50:00 | [OK] SERVICE sshd: active
2026-04-03T12:50:00 | [CRITICAL] PORT 80: closed
```

---

### JSON Log (`monitor.json`)

```json
{"timestamp": "...", "metric": "cpu", "value": 25, "status": "OK"}
{"timestamp": "...", "metric": "service", "name": "sshd", "value": "active", "status": "OK"}
```

---

## 🧠 Technical Decisions

- **systemctl over process inspection**  
  Provides accurate service state in systemd-based systems.

- **Port validation**  
  Ensures services are not only running but also reachable.

- **External configuration**  
  Separates operational parameters from code.

- **Structured logging**  
  Facilitates troubleshooting and integration with monitoring tools.

---

## ⚠️ Limitations

- Only validates TCP connectivity (no deep application health check)
- No alerting system (email/webhook)
- Designed for systemd-based Linux systems

---

## 🚀 Future Improvements

- HTTP health checks
- Alert system (email/webhook)
- Integration with monitoring tools (Prometheus/Grafana)
- Run as a systemd service
- Config validation with JSON schema

---

## 📦 Requirements

```
psutil
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 💡 What This Project Demonstrates

- Linux system administration fundamentals  
- Monitoring and observability concepts  
- Python automation for infrastructure  
- Structured logging and diagnostics  
- Clean and modular design  

---

## 👨‍💻 Author

Developed as part of preparation for a **Junior Infrastructure Analyst** role.