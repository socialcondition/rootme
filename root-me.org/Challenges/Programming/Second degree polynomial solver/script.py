import socket
import math

HOST = "challenge01.root-me.org"
PORT = 52018
# "[>] (001/025) Solve this equation please: 714.x² - 477.x¹ + 132 = -454

def d2eq(a, b, c):
    delta = b*b - 4*a*c
    if a != 0:
        if delta == 0:
            root = -b / (2 * a)
            return f"x: {root:.3f}"
        elif delta > 0:
            root1 = (-b + math.sqrt(delta)) / (2 * a)
            root2 = (-b - math.sqrt(delta)) / (2 * a)
            ###
            x1_val = max(root1, root2)
            x2_val = min(root1, root2)
            
            return f"x1: {x1_val:.3f} ; x2: {x2_val:.3f}"
            ###
        else:
            return "Not possible"    
    else:
        return "a = 0"


class Box:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def solve(self, eq):
        try:    
            
            line = eq[
                eq.find("[>]"):eq.find("?")
            ]
            line = line[line.find(":")+1:]
            l = line
            
            a = int(
                line[
                    :line.find(".")
                ]
            )

            line = line[line.find("²")+1:]

            b = int(
                line[
                    :line.find(".")
                ].replace(" ", "")
            )

            line = line[line.find("¹")+1:]
            r = int(
                line[
                    line.find("="):
                ].replace(" ", "").replace("=", "").replace("\n", "")
            )*(-1)

            c = int(
                line[
                    :line.find("=")
                ].replace(" ", "")
            )+r
            
            #print(a, b, c)
            print(d2eq(a, b, c), "\n")
            return d2eq(a, b, c)

        except Exception as E:
            pass
            #print("Error:" ,E)

    def conn(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
        
                response = s.recv(1024)
                print(f"{response.decode('utf-8')}\n")   
                last = response

                while response:
                    s.sendall(
                        (
                            str(
                                self.solve(
                                    response.decode("utf-8")
                                )
                            )+"\n"
                        ).encode("utf-8")
                    )
                    last = response
                    response = s.recv(1024)
                    print(f"{response.decode('utf-8')}\n") 
                
                return last.decode("utf-8")

            except ConnectionRefusedError:
                print("Error: Could not connect to the server. Is it running?")

def main():
    ctf = Box(HOST, PORT)
    print(ctf.conn())

if __name__ == "__main__":
    main()
