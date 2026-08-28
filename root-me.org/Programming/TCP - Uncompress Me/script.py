from re import search
import socket 
import base64 
import zlib

def extract_text(text):
    return search(r"'.*'", text).group(0).replace("\'", "")

def dec_text(text):
    return zlib.decompress(
            base64.b64decode(text)
            ).decode("utf-8") 


def conn(HOST, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
    
            try:
                response = client_socket.recv(1024)
                while response:
                    print(f"{response.decode('utf-8')}\n")   
                
                    client_socket.sendall(
                            (
                                dec_text(
                                    extract_text(
                                        response.decode("utf-8")
                                    )
                                )+"\n"
                            ).encode("utf-8")
                    )

                    response = client_socket.recv(1024)
                    print(f"{response.decode('utf-8')}\n") 
            except Exception: 
                pass
        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?")

HOST = "challenge01.root-me.org"
PORT = 52022

conn(HOST, PORT)