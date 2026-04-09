#  Online Music Streaming Server

##  Overview

This project implements a **secure client-server audio streaming system** using Python. The system allows multiple clients to request and stream audio files from a centralized server over a **TCP connection secured with SSL/TLS**.

It demonstrates key concepts in:

* Computer Networks
* Socket Programming
* Secure Communication (SSL/TLS)
* Buffer Management
* Performance Evaluation

---

##  Problem Statement

Traditional file transfer systems lack efficient real-time streaming, buffering, and secure transmission mechanisms.

This project aims to:

* Enable **real-time audio streaming**
* Support **multiple concurrent clients**
* Ensure **secure communication using SSL/TLS**
* Implement **buffering for smooth playback**
* Measure **network performance metrics**

---

##  System Architecture

```
Client  <==== SSL/TCP ====>  Server
   |                             |
   |---- Request (GET/LIST) ---->|
   |<--- Audio Stream (chunks) --|
   |                             |
Buffering → Playback → Metrics Logging
```

---

## Working of the System


* Client connects to the server using SSL/TCP.
* Secure handshake is established using certificates.
* Client sends command:
  * LIST → server returns available songs
  * GET <file> → server starts streaming
* Server reads audio file in chunks.
* Chunks are sent over encrypted connection.
* Client buffers received data.
* Buffered data is written to file / played.
* Metrics are recorded during transfer.

---

##  Project Structure
```
music_streaming_platform_cn/
│
├── server/
│   ├── server.py
│   ├── client_handler.py
│   ├── streamer.py
│   └── protocol.py
│
├── client/
│   ├── client.py
│   ├── buffer.py
│   └── player.py
│
├── analysis/
│   ├── metrics.py
│   ├── metrics.txt
│   └── performance_log.txt
│
├── music/
│   └── (audio files)
│
├── .gitignore
└── README.md
```

---

##  Features

###  Secure Communication

* SSL/TLS encryption over TCP
* Prevents unauthorized access and data interception

###  Audio Streaming

* Streams audio in chunks (buffer-based)
* Supports multiple songs
  

###  Song Listing

* Clients can request available songs using `LIST`  
  
  **Note:** Sample audio files are used for demonstration purposes only.

###  Buffer Management

* Client buffers data before playback
* Ensures smooth streaming without interruptions

###  Playback System

* Audio plays via system’s default media player

###  Performance Metrics

Measured metrics include:

* Latency
* Total Transmission Time
* Throughput
* Data Size

Logs stored in:

```
analysis/metrics.txt
analysis/performance_log.txt
```

---

##  Prerequisites

Make sure the following are installed:

* Python 3.x
* OpenSSL (for SSL certificates)
* VLC Media Player / Default system media player


Python libraries used:

* socket
* ssl
* threading
* os
* time


##  How to Run

###  Step 1: Navigate to project root

```
cd music_streaming_platform_cn
```

###  Step 2: Start Server

```
python -m server.server
```

###  Step 3: Start Client (new terminal)

```
python -m client.client
```

---

##  Commands

| Command          | Description          |
| ---------------- | -------------------- |
| `LIST`           | Show available songs |
| `GET <filename>` | Stream a song        |
| `exit`           | Close client         |

---


##  Performance Evaluation

Metrics measured:

* Latency (time to receive first chunk)
* Throughput (bytes per second)
* Total transmission time
* File size

Test scenarios:

* Single client streaming
* Multiple concurrent clients
* Large vs small audio files


---

## Metrics Logging Design

The system maintains two separate log files to capture performance metrics at different stages of the streaming process.

### metrics.txt (Server-side Logging)

* Stores metrics calculated at the server
* Includes:

  * Data transmission time
  * Throughput (based on bytes sent)
  * Server-side latency estimation
* Represents how efficiently the server streams data

### performance_log.txt (Client-side Logging)

* Stores metrics calculated at the client
* Includes:

  * Actual latency experienced (time to first packet)
  * Total download time
  * Throughput (based on bytes received)
* Represents real-world user experience

Client-side metrics may differ from server-side metrics due to network latency, buffering delays, and playback overhead.

---
##  Technologies Used

* Python
* Socket Programming
* SSL/TLS (Secure Sockets Layer)
* Multithreading
* File I/O

---

##  Security Implementation

* SSL wrapping of sockets
* Certificate-based encryption
* Private key excluded using `.gitignore`

---

##  Contributors

* Nishkaa V
* Atharva D Kulkarni
* B R Manasi

---

##  Conclusion

This project successfully demonstrates a **secure, efficient, and scalable audio streaming system**, integrating networking, security, and performance evaluation concepts.

---

