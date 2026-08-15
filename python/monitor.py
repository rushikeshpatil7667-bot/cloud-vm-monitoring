import time
import platform
import psutil

from prometheus_client import start_http_server, Gauge


# ============================================================
# Cloud VM Monitoring System - Python Metrics Exporter
# ============================================================

EXPORTER_PORT = 8000
COLLECTION_INTERVAL = 5


# -----------------------------
# System Information
# -----------------------------

system_info = Gauge(
    "system_info",
    "System information",
    ["hostname", "platform", "python_version"]
)


# -----------------------------
# CPU Metrics
# -----------------------------

cpu_usage = Gauge(
    "system_cpu_usage_percent",
    "Current CPU utilization percentage"
)

cpu_count = Gauge(
    "system_cpu_count",
    "Number of logical CPU cores"
)


# -----------------------------
# Memory Metrics
# -----------------------------

memory_usage = Gauge(
    "system_memory_usage_percent",
    "Current memory utilization percentage"
)

memory_total = Gauge(
    "system_memory_total_bytes",
    "Total system memory in bytes"
)

memory_available = Gauge(
    "system_memory_available_bytes",
    "Available system memory in bytes"
)


# -----------------------------
# Disk Metrics
# -----------------------------

disk_usage = Gauge(
    "system_disk_usage_percent",
    "Current disk utilization percentage"
)

disk_total = Gauge(
    "system_disk_total_bytes",
    "Total disk capacity in bytes"
)

disk_free = Gauge(
    "system_disk_free_bytes",
    "Available disk space in bytes"
)


# -----------------------------
# Network Metrics
# -----------------------------

network_bytes_sent = Gauge(
    "system_network_bytes_sent_total",
    "Total bytes sent over the network"
)

network_bytes_received = Gauge(
    "system_network_bytes_received_total",
    "Total bytes received over the network"
)

network_packets_sent = Gauge(
    "system_network_packets_sent_total",
    "Total packets sent over the network"
)

network_packets_received = Gauge(
    "system_network_packets_received_total",
    "Total packets received over the network"
)


# -----------------------------
# System Health Metrics
# -----------------------------

system_uptime = Gauge(
    "system_uptime_seconds",
    "System uptime in seconds"
)

load_average = Gauge(
    "system_load_average",
    "System one-minute load average"
)


# ============================================================
# Metric Collection
# ============================================================

def collect_metrics():

    # System information
    system_info.labels(
        hostname=platform.node(),
        platform=platform.platform(),
        python_version=platform.python_version()
    ).set(1)

    # CPU
    cpu_usage.set(psutil.cpu_percent(interval=1))
    cpu_count.set(psutil.cpu_count(logical=True))

    # Memory
    memory = psutil.virtual_memory()

    memory_usage.set(memory.percent)
    memory_total.set(memory.total)
    memory_available.set(memory.available)

    # Disk
    disk = psutil.disk_usage("/")

    disk_usage.set(disk.percent)
    disk_total.set(disk.total)
    disk_free.set(disk.free)

    # Network
    network = psutil.net_io_counters()

    network_bytes_sent.set(network.bytes_sent)
    network_bytes_received.set(network.bytes_recv)
    network_packets_sent.set(network.packets_sent)
    network_packets_received.set(network.packets_recv)

    # Uptime
    uptime = time.time() - psutil.boot_time()
    system_uptime.set(uptime)

    # Load average
    try:
        load_average.set(psutil.getloadavg()[0])
    except (AttributeError, OSError):
        load_average.set(0)


# ============================================================
# Application Entry Point
# ============================================================

def main():

    print("=" * 60)
    print(" Cloud VM Monitoring - Python Metrics Exporter")
    print("=" * 60)
    print(f" Metrics endpoint : http://localhost:{EXPORTER_PORT}/metrics")
    print(f" Collection interval : {COLLECTION_INTERVAL} seconds")
    print("=" * 60)

    # Start Prometheus HTTP endpoint
    start_http_server(EXPORTER_PORT)

    # Continuously collect metrics
    while True:

        try:
            collect_metrics()

        except Exception as error:
            print(f"[ERROR] Metric collection failed: {error}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
