import socket, re
from hashlib import sha1
from base64 import b64encode

from websocket.utils import get_host_addr, decode_frame, encode_frame

from time import sleep

class WebSocket():
    id = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, host: str = "localhost", port: int = 9001) -> None:
        self._host = get_host_addr(host)
        self._port = port
        self._sock = self._create_socket()
        self._is_running = True      

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def serve(self):
        self._sock.bind((self._host, self._port))
        self._sock.listen(3)

        while self._is_running:
            print("[+] WebSocket is listenning...")

            conn, addr = self._sock.accept()

            if conn:
                # Do Handshake, after handshake is done , create session
                print(f"[!] Do Handshake with {addr[0]}.")

                # make handshake
                data = conn.recv(5000).decode()
                wkey = re.search(r'Sec-WebSocket-Key:(.*)', data).group(1)
                wkey = wkey.strip()
                
                tmp = sha1((wkey + self.id).encode()).digest()
                client_key = b64encode(tmp).decode()
                
                response = "HTTP/1.1 101 Switching Protocols\r\n"
                response += "Upgrade: websocket\r\n"
                response += "Connection: Upgrade\r\n"
                response += f"Sec-WebSocket-Accept: {client_key}\r\n"
                response += f"Sec-WebSocket-Version: 13\r\n"
                response += "Sec-WebSocket-Protocol: chat\r\n"
                response += "\r\n"
                response = response.encode()
                conn.send(response)                        

                print("[!] handshake done !!")

                ws_client = WebSocketClient(conn)
        
        self._sock.close()


class WebSocketClient():
    def __init__(self, client: socket.socket) -> None:
        self._client = client
        self.is_running = True
        
        self.send("Connection successfully connected !!")

        while self.is_running:
            resp = self.recv()
           
            if resp == "/exit":
                self._client.close()
                self.is_running = False
            
            elif resp == "/changeme":
                sleep(3)
                self.send("Has been changed !!")


    def send(self, msg):
        frame = encode_frame(msg.encode())
        self._client.send(frame)
    
    def recv(self, buffersize: int = 1024):
        data = None

        while True:
            data = self._client.recv(buffersize)

            if len(data) < buffersize:
                break
        
        if data is not None:
            data = decode_frame(data)

        return data