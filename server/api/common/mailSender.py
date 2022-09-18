
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template
from pathlib import Path

from string import Template


class mail_sender():
    def __init__(self):
        self.content = MIMEMultipart() 
        self.content["from"] = "oceanremotelab@gmail.com"  #寄件者        
    def send_resetPassword_mail(self,recipient,token):
        self.content["to"] = recipient+"@mail.ntou.edu.tw" #收件者                
        self.content["subject"] = "reset your password"  #郵件標題
        ##self.template = Template(Path("/resetPasswordMail.html"))
        ##print(str(self.template))
        body = render_template("resetPasswordMail.html",token=token)
        self.content.attach(MIMEText(body, "html")) 
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("oceanremotelab@gmail.com", "ckystilkvgqxnodh")  # 登入寄件者gmail
                smtp.send_message(self.content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)