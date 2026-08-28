import math
from re import findall
import socket 

def calc(text):
    text = text.replace("You should tell me the answer of this math operation in less than 2 seconds !", "")
    nums = findall(r" [0-9]* ", text)
    print(nums)
    return round( math.sqrt( int(nums[0]) ) * int(nums[1]), 2 )
   
def conn(HOST, PORT):

    # Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
    
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode('utf-8')}")
            

            message = str(calc(response.decode("utf-8")))+"\n"
            print(message)
            client_socket.sendall(message.encode("utf-8"))
            
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode('utf-8')}")
            

        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?")

HOST = "challenge01.root-me.org"
PORT = 52002

conn(HOST, PORT)