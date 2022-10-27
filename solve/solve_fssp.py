import requests
import base64
from PIL import Image
import io
import time
import os


session = requests.Session()


##Get captcha and save

headers = {'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5','Connection':'keep-alive','Referer':'https://fssp.gov.ru/','Sec-Fetch-Dest':'script','Sec-Fetch-Mode':'no-cors','Sec-Fetch-Site':'same-site','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36','sec-ch-ua':'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"'}

img_bytes = session.get('https://is.fssp.gov.ru/refresh_visual_captcha/',headers=headers)

#print(img_bytes.text)
image_base64=str(img_bytes.text.split(',')[1].split('"')[0])


image = base64.b64decode(str(img_bytes.text.split(',')[1].split('"')[0]))       


if img_bytes.status_code == 200:
    with open("fssp_captcha.jpg", 'wb') as f:
        f.write(image)
        print("Download and save captcha from is.fssp.gov.ru")

        #solve captcha
        
        json = {"clientKey":"DEMO","task": {
		"type": "ImageToTextTask",
        "subType":"fssp",
		"body": image_base64
	    }}
        #print(json)
        url_solve_captcha="http://iamnotbot.com:5000/createTask";         
        r = requests.post(url_solve_captcha, json=json)
        print("Captcha = "+r.text)

else:
    print("Cannot download and save captcha from is.fssp.gov.ru")
   