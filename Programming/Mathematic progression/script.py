import requests
from bs4 import BeautifulSoup


CTF_RET = "http://challenge01.root-me.org/programmation/ch1/"
CTF_SUB = "http://challenge01.root-me.org/programmation/ch1/ep1_v.php"


class Seq:
    def __init__(self, arg1, op1, op2, arg2, u0, n ):
        self.arg1 = arg1
        self.arg2 = arg2
        self.op1 = op1
        self.op2 = op2
        self.u0 = u0
        self.n = n

    def val(x):
        if x == "+":
            return 1
        elif x == "-":
            return -1

    def calc_prog(self):
        s = self.u0 
        p = 1

        if self.n < 0:
            p = -1
        
        for i in range(0, self.n, p):
            s = ( self.arg1 + Seq.val(self.op1)*s ) + Seq.val(self.op2)*(i * self.arg2)
        return s


class MathEngine:
    def __init__(self, req):
        self.req = req

    def resolve(self, clean_syntax):
        #print(clean_syntax)
        
        arg1 = int ( clean_syntax[
            clean_syntax.find("[")+1:
            clean_syntax.find("]")-4
        ].strip(" ") )

        op1 = clean_syntax[
            clean_syntax.find("U")-3:
            clean_syntax.find("U")-1
        ].strip(" ")

        clean_syntax = clean_syntax[clean_syntax.find("]")+1:]

        op2 = clean_syntax[
            0: clean_syntax.find("[")-1
        ].strip()

        arg2 = int ( clean_syntax[
            clean_syntax.find("*")+2:
            clean_syntax.find("]")-1 
        ] )

        u0 = int (clean_syntax[
            clean_syntax.find("=")+1:
            clean_syntax.find("U")
        ].strip(" ") )

        n = int ( clean_syntax[
            clean_syntax.find("U")+1:
        ].strip(" ") )

        #print(arg1, op1, op2, arg2, u0, n)
        
        s = Seq(arg1, op1, op2, arg2, u0, n)
        return s.calc_prog()

    def clean(self):
        s = BeautifulSoup(self.req, "html.parser")
        
        subs = s.find_all('sub')
        u0 = s.find_all('br')[0].next_sibling
        payload = ""
        for i in range(len(subs) - 1):
            payload += subs[i].next_sibling
        
        return (payload + u0 + subs[-1].contents[0]).replace("\n", "")
        


class Ctf:
    def __init__(self, ret_url, sub_url):
        self.session = requests.Session()
        self.ret_url = ret_url
        self.sub_url = sub_url

    def retrieve_math(self):
        try:    
            req = self.session.get(self.ret_url).text
            m = MathEngine(req)
            
            return m.resolve(
                m.clean()
            )

        except Exception as E:
            print("Error: ", E)

    def accept_res(self, res: int):
        try:
            return self.session.get(self.sub_url+"?result="+str(res)).text
        except Exception as E:
            print("Error: ", E)
        

def main():
    box = Ctf(CTF_RET, CTF_SUB)
    print( 
        box.accept_res(box.retrieve_math())
    )


if __name__ == "__main__":
    main()
