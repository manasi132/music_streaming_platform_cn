import os
import time
from analysis.metrics import calculate_metrics

CHUNK_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_FOLDER = os.path.join(BASE_DIR, "..", "music")
TXT_FILE = os.path.join(BASE_DIR, "..", "analysis", "metrics.txt")


def stream_file(conn, filename, addr=None):
    filepath = os.path.join(MUSIC_FOLDER, filename)

    if not os.path.exists(filepath):
        conn.send(b"ERROR")
        return

    conn.send(b"OK")

    total_bytes = 0
    start_time = time.time()
    first_packet_time = None

    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)

                if not chunk:
                    break

                conn.sendall(chunk)

                if first_packet_time is None:
                    first_packet_time = time.time()

                total_bytes += len(chunk)

        conn.send(b"END")
        end_time = time.time()

        print(f"[STREAM COMPLETE] {filename}")

        #CALCULATE METRICS
        latency, total_time, throughput = calculate_metrics(
            start_time, first_packet_time, end_time, total_bytes
        )

        print(f"[METRICS] Latency: {latency:.4f}s | Time: {total_time:.4f}s | Throughput: {throughput:.2f} Bps")

        #SAVE METRICS
        save_metrics({
            "client": str(addr),
            "song": filename,
            "bytes_sent": total_bytes,
            "latency_sec": round(latency, 4),
            "total_time_sec": round(total_time, 4),
            "throughput_Bps": round(throughput, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        print("[STREAM ERROR]", e)


def save_metrics(new_data):
    try:
        # Ensure folder exists
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)

        # Save TXT
        with open(TXT_FILE, "a") as f:
            f.write(str(new_data) + "\n")

        print("[METRICS SAVED]")

    except Exception as e:
        print("[METRICS ERROR]", e)

