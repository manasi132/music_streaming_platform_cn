import socket
import ssl
import threading
from .client_handler import handle_client

HOST = "0.0.0.0"
PORT = 8080

def main():
    # SSL setup
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    # Socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[SERVER STARTED] Listening on port {PORT}")

    while True:
        client_socket, addr = server_socket.accept()

        try:
            secure_conn = context.wrap_socket(client_socket, server_side=True)

            thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
            thread.start()

        except Exception as e:
            print("[SSL ERROR]", e)
            client_socket.close()

if __name__ == "__main__":
    main()
