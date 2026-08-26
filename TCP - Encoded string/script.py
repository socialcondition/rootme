from re import search
import socket 
import base64 

def extract_text(text):
    return search(r"'.*'", text).group(0).replace("\'", "")

def conn(HOST, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
    
            response = client_socket.recv(1024)
            print(f"{response.decode('utf-8')}\n")   

            d_text = extract_text(response.decode('utf-8'))
            text = base64.b64decode(d_text).decode("utf-8")+"\n"
            
            client_socket.sendall(text.encode("utf-8"))

            response = client_socket.recv(1024)
            print(f"{response.decode('utf-8')}\n") 

        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?")

HOST = "challenge01.root-me.org"
PORT = 52023

conn(HOST, PORT)