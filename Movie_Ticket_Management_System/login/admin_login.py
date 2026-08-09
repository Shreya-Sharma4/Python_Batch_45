from db import cursor
from services.otp_services import VerifyOtp
from services.admin_services import update_admin_credentials


def admin_login():
    count=0
    while True:
        try:
            username=input("Enter username : ")
            password=input("Enter password : ")
            cursor.execute("select * from admins")
            rows=cursor.fetchone()
            if not rows:
                print("Their is no Admin!")
                return
            if username==rows[1] and password==rows[2]:
                print("Login successful")
                #admin_menu()
                print("Thank you for using our service.")
                return
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
                            limit+=1
                            if email !=rows[3]:
                                print("Email does not match our records.")
                                if limit<3: 
                                    print(f"{3-limit} attempt remaining!")                             
                                    retry=input("Want to Retry again (y/n) : ").lower()
                                    if retry !='y':                              
                                        print("Thank you for using our service.")
                                        return
                                else:
                                    print("Attempts Reached!, Try after some time.")
                                    return
                            else:
                                otp = VerifyOtp()
                                if otp.check_login(email, update_admin_credentials):
                                    print("Please login with your new credentials.")
                                    break
                                else:
                                    return
                        continue
                    else:
                        print("Thank you for using our service.")
                        return
                else:
                    ch=input("Do you want to try again? (y/n) : ").lower()
                    if ch=='y':
                        continue
                    else:
                        print("Thank you for using our service.")
                        return
        except Exception as e:
            print(e)
            return