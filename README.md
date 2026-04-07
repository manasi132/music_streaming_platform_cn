# Secure Audio Streaming System

## Overview
This project implements a secure client-server audio streaming system using Python. The system enables clients to request and receive audio files from a centralized server over a TCP connection secured with SSL/TLS encryption. It demonstrates concepts in network programming, concurrency, and real-time data streaming.

## Features
- Secure communication using SSL/TLS
- Multithreaded server for handling multiple clients
- Chunk-based file streaming
- Client-side buffering for smooth playback
- Performance metrics calculation (latency, throughput, total time)

## Usage
Run the server:
python server.py

Run the client:
python client.py