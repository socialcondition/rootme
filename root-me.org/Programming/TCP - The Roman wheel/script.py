from re import search
import socket 
import codecs 

def extract_text(text):
    return search(r"'.*'", text).group(0).replace("\'", "")

def conn(HOST, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
    
            response = client_socket.recv(1024)
            print(f"{response.decode('utf-8')}\n")   

            #Retrieve the decoded text and decode it 
            d_text = extract_text(response.decode('utf-8')) # utf-8 Decoded text
            text = codecs.decode(d_text, "rot-13")+"\n" # rot-13 Decoded text

            
            # Send the decoded text         
            client_socket.sendall(text.encode("utf-8"))

            response = client_socket.recv(1024)
            print(f"{response.decode('utf-8')}\n") 

        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?")

HOST = "challenge01.root-me.org"
PORT = 52021

conn(HOST, PORT)