from db import cursor
from services.otp_service import VerifyOtp
from services.user_services import update_user_credentials

def user_login():
    count=0
    while True:
        try:
            username=input("Enter username : ")
            password=input("Enter password : ")
            cursor.execute("select * from users where username=%s and password=%s",(username,password))
            row=cursor.fetchone()
            if row is not None:
                print("Login successful")
                return row[0] # Return user_id
            else:
                print("Invalid credentials")
                count+=1
                if count>=3:
                    print("You have exceeded the maximum number of attempts. Please try again later.")
                    choice=input("Do you want to change credentials? (y/n) : ").lower()
                    if choice=='y':
                        limit=0
                        while True:
                            email=input("Enter your registered email: ")
                            cursor.execute("select * from users where email=%s",(email,))
                            email_row=cursor.fetchone()
                            limit+=1
                            if email_row is None:
                                print("Email does not match our records.")
                                if limit<3:    
                                    print(f"{3-limit} attempt remaining!")                          
                                    retry=input("Want to Retry again (y/n) : ").lower()
                                    if retry !='y':                              
                                        print("Thank you for using our service.")
                                        return None  
                                else:
                                    print("Attempts Reached!, Try after some time.")
                                    return None
                            else:
                                otp = VerifyOtp()
                                if otp.check_login(email, update_user_credentials,email):
                                    print("Please login with your new credentials.")
                                    break
                                else:
                                    return None
                        continue
                    else:
                        print("Thank you for using our service.")
                        return None
                else:
                    ch=input("Do you want to try again? (y/n) : ").lower()
                    if ch=='y':
                        continue
                    else:
                        print("Thank you for using our service.")
                        return None
        except Exception as e:
            print(e)
            return None