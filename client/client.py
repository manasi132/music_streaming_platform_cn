import socket
import ssl
import time
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.metrics import calculate_metrics
from buffer import Buffer
from player import AudioPlayer

HOST = "127.0.0.1"   # 🔥 change to server IP for multi-device
PORT = 8080


def main():
    print("[CONNECTING TO SERVER]")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SSL setup
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
    secure_socket.connect((HOST, PORT))

    print("[CONNECTED]")

    # 🔥 GET SONG LIST
    secure_socket.sendall(b"LIST")
    song_data = secure_socket.recv(4096).decode()

    print("\n🎵 AVAILABLE SONGS:")
    print(song_data)

    while True:
        filename = input("\nEnter song name (or 'exit'): ")

        if filename.lower() == "exit":
            break

        secure_socket.sendall(f"GET {filename}".encode())

        response = secure_socket.recv(1024)

        if response.startswith(b"ERROR"):
            print("❌ File not found")
            continue

        print("[STREAMING STARTED]")

        save_path = f"received_{filename}"
        buffer = Buffer(save_path)
        player = AudioPlayer(save_path)

        start_time = time.time()
        first_packet_time = None

        started = False
        BUFFER_THRESHOLD = 200000

        chunk_count = 0
        total_received = 0

        while True:
            data = secure_socket.recv(4096)

            if data == b"END":
                print("[END OF STREAM]")
                break

            if not data:
                break

            if first_packet_time is None:
                first_packet_time = time.time()

            buffer.add_chunk(data)

            # 🔥 chunk logging
            chunk_count += 1
            total_received += len(data)
            print(f"📦 Chunk {chunk_count} received ({len(data)} bytes) | Total: {total_received} bytes")

            # 🎧 start playback
            if not started and buffer.get_total_bytes() > BUFFER_THRESHOLD:
                player.play()
                started = True

        end_time = time.time()
        buffer.close()

        print("[DOWNLOAD COMPLETE]")

        # 📊 metrics
        latency, total_time, throughput = calculate_metrics(
            start_time,
            first_packet_time,
            end_time,
            buffer.get_total_bytes()
        )

        print("\n📊 PERFORMANCE METRICS")
        print(f"Latency     : {latency:.4f} sec")
        print(f"Total Time  : {total_time:.4f} sec")
        print(f"Throughput  : {throughput:.2f} bytes/sec")
        print(f"Data Size   : {buffer.get_total_bytes()} bytes")

        # 🔥 SAVE METRICS
        log_path = os.path.join("analysis", "performance_log.txt")

        with open(log_path, "a") as f:
            f.write("\n===== STREAM SESSION =====\n")
            f.write(f"File        : {filename}\n")
            f.write(f"Latency     : {latency:.4f} sec\n")
            f.write(f"Total Time  : {total_time:.4f} sec\n")
            f.write(f"Throughput  : {throughput:.2f} bytes/sec\n")
            f.write(f"Data Size   : {buffer.get_total_bytes()} bytes\n")
            f.write("===========================\n")

        print(f"📁 Metrics saved to {log_path}")

    secure_socket.close()


if __name__ == "__main__":
    main()