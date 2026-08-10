import os
from dotenv import load_dotenv
import time
import random as r
import smtplib
from email.message import EmailMessage

load_dotenv()
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

class VerifyOtp:
    def __init__(self):
        self.__otp=None
        self.__attempts=0
    
    def check_attempts(self,receiver,update_function,*args):
        if self.__attempts<3:
            return self.check_login(receiver,update_function,*args)

    def check_login(self,receiver,update_function,*args):
        self.__otp=r.randint(1000,9999)
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = receiver
        msg["Subject"] = "Update your credentials"
        msg.set_content(f"Your OTP is : {self.__otp} ")
        server=None
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            self.sendtime=time.time()
        except Exception as e:
            print(e)
            return
        finally:
            if server is not None:
                server.quit()
        try:    
            print("your otp is send on your mail")
            userotp=int(input("reenter your otp to validate : "))
            self.currenttime=time.time()
            if self.currenttime-self.sendtime>300:
                print("otp expired")
                choice=input("resend otp (y/n) : ").lower()
                if choice=='y':
                    return self.check_login(receiver,update_function,*args)
                else:
                    print("Thank you for using our service")
                    return False
            if self.__otp==userotp:
                print("otp matched")
                return update_function(*args)
            else:
                print("otp not matched")
                self.__attempts+=1
                print(3-self.__attempts,"left !")
                if self.__attempts==3:
                    print("attempts reached! try after some time")
                    return False
                resend=input("Resend OTP (y/n) : ").lower()
                if resend !='y':
                    print("Thank you for using our service")
                    return False
                return self.check_attempts(receiver, update_function,*args)
        except Exception as e:
            print(e)
            return False