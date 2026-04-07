import os
from protocol import parse_request
from streamer import stream_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_FOLDER = os.path.join(BASE_DIR, "..", "music")   

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    try:
        while True:
            request = conn.recv(1024).decode().strip()

            if not request:
                print(f"[CLIENT LEFT] {addr}")
                break

            print(f"[REQUEST] {request}")

            #HANDLE LIST COMMAND
            if request == "LIST":
                try:
                    songs = os.listdir(MUSIC_FOLDER)

                    if not songs:
                        conn.send(b"No songs available\n")
                    else:
                        response = ""
                        for i, song in enumerate(songs):
                            response += f"{i+1}. {song}\n"

                        conn.send(response.encode())

                except Exception as e:
                    conn.send(f"ERROR: {str(e)}".encode())

                continue   

            #HANDLE PLAY REQUEST
            filename = parse_request(request)

            if not filename:
                conn.send(b"ERROR: Invalid Request")
                continue

            file_path = os.path.join(MUSIC_FOLDER, filename)

            if not os.path.exists(file_path):
                conn.send(b"ERROR: File not found")
                continue

            #STREAM FILE
            stream_file(conn, file_path)

    except Exception as e:
        print(f"[CLIENT ERROR] {addr} -> {e}")

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")
