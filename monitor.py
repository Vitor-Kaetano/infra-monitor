import psutil
import subprocess
from datetime import datetime
import json
import socket
import sys

# argumento de configuração
config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"


# =========================
# CONFIG
# =========================

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_config(config):
    required_keys = ["services", "ports", "thresholds"]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")


# =========================
# CLASSIFICAÇÃO
# =========================

def classify_resource(metric, value, thresholds):
    if value >= thresholds[metric]["critical"]:
        return "CRITICAL"
    elif value >= thresholds[metric]["warning"]:
        return "WARNING"
    return "OK"


def classify_service(status):
    if status == "active":
        return "OK"
    elif status in ["inactive", "failed"]:
        return "CRITICAL"
    elif status == "unknown" or "error" in status:
        return "WARNING"
    return "WARNING"


def classify_port(status):
    return "OK" if status == "open" else "CRITICAL"


# =========================
# CHECKS (COLETA)
# =========================

def check_cpu():
    return psutil.cpu_percent(interval=1)


def check_memory():
    return psutil.virtual_memory().percent


def check_disk():
    return psutil.disk_usage("/").percent


def check_service(service):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip()
    except Exception as e:
        return f"error: {str(e)}"


def check_port(port, host="localhost"):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((host, port))
        return "open"
    except Exception:
        return "closed"


# =========================
# BUILD ENTRIES
# =========================

def build_resource_entry(metric, value, thresholds, timestamp):
    return {
        "timestamp": timestamp,
        "metric": metric,
        "value": value,
        "status": classify_resource(metric, value, thresholds)
    }


def build_service_entry(service, timestamp):
    raw_status = check_service(service)

    return {
        "timestamp": timestamp,
        "metric": "service",
        "name": service,
        "value": raw_status,
        "status": classify_service(raw_status)
    }


def build_port_entry(port, timestamp):
    status = check_port(port)

    return {
        "timestamp": timestamp,
        "metric": "port",
        "name": port,
        "value": status,
        "status": classify_port(status)
    }


# =========================
# OUTPUT
# =========================

def format_log(entry):
    if entry["metric"] == "service":
        return f"{entry['timestamp']} | [{entry['status']}] SERVICE {entry['name']}: {entry['value']}"

    elif entry["metric"] == "port":
        return f"{entry['timestamp']} | [{entry['status']}] PORT {entry['name']}: {entry['value']}"

    else:
        return f"{entry['timestamp']} | [{entry['status']}] {entry['metric'].upper()}: {entry['value']}%"


def write_json(entries, path="monitor.json"):
    with open(path, "a") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


# =========================
# MAIN
# =========================

def main():
    config = load_config(config_path)
    validate_config(config)

    thresholds = config["thresholds"]
    services = config["services"]
    ports = config["ports"]

    entries = []
    timestamp = datetime.now().isoformat()

    # recursos
    entries.append(build_resource_entry("cpu", check_cpu(), thresholds, timestamp))
    entries.append(build_resource_entry("memory", check_memory(), thresholds, timestamp))
    entries.append(build_resource_entry("disk", check_disk(), thresholds, timestamp))

    # serviços
    for service in services:
        entries.append(build_service_entry(service, timestamp))

    # portas
    for port in ports:
        entries.append(build_port_entry(port, timestamp))

    # saída
    write_json(entries)

    for entry in entries:
        print(format_log(entry))


if __name__ == "__main__":
    main()