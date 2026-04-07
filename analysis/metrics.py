import time

def calculate_metrics(start_time, first_packet_time, end_time, total_bytes):
    print("\n[CALCULATING METRICS]")

    # Latency = time until first packet sent
    if first_packet_time:
        latency = first_packet_time - start_time
    else:
        latency = 0

    total_time = end_time - start_time

    if total_time > 0:
        throughput = total_bytes / total_time
    else:
        throughput = 0

    return latency, total_time, throughput

