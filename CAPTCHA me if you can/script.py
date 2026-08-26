import requests 
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import cv2
import base64
import re

HOST_URL = "http://challenge01.root-me.org/programmation/ch8/" 
IMG_PATH = "img.png"

COOKIE = {
    "PHPSESSID": "<retrieve this cookie from browser -> dev tools -> network. Or using a proxy>",
}

session = requests.Session()
session.cookies.update(COOKIE)

def send_captcha(url, captcha):
    print(captcha)

    payload = {
        "cametu":captcha
    }

    try:
        response = session.post(
            url,
            data=payload
        ).text

        s = BeautifulSoup(response, 'html.parser')
        return (s.p)
    except Exception as E:
        print("Error: ", E)

def clean_img(path):
    # 1. Load the original color image
    img = cv2.imread(path)
    
    # 2. Apply a 3x3 Median Filter.
    cleaned_img = cv2.medianBlur(img, 3)
    cv2.imwrite('cleaned_img.png', cleaned_img)    



def resolve_captcha(captcha_url):
    download_img(captcha_url)
    clean_img(IMG_PATH)
    # load the image
    img = Image.open('cleaned_img.png')

    # extract text from image
    custom_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return pytesseract.image_to_string(img, config=custom_config).replace("\n", "")


def download_img(img_url):
    try:
        match = re.match(r"data:image/([^;]+);base64,(.*)", img_url, re.DOTALL)

        if not match:
            raise ValueError("Not a valid base64 image data URI")

        extension = match.group(1)
        base64_data = match.group(2)
        img_data = base64.b64decode(base64_data)
        
        filename = f"img.{extension}"

        with open(filename, "wb") as f:
            f.write(img_data)

    except Exception as e:
        print("Error downloading image:", e)


def get_captcha_url(url):
    try:
        source_code = session.get(url).text
        soup = BeautifulSoup(source_code, 'html.parser')

        return soup.img["src"]
    except Exception as E:
        print("Error: ", E)

def main():
    flag = send_captcha(
        HOST_URL,
        resolve_captcha(
            get_captcha_url(HOST_URL)
        )
    )
    print(flag)

if __name__ == "__main__":
    for i in range(10):
        main()
