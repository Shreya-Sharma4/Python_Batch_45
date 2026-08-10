from db import cursor
from services.otp_service import VerifyOtp
from services.admin_service import update_admin_credentials

def admin_login():
    count=0
    while True:
        try:
            username = input("Enter username : ")
            password = input("Enter password : ")
            
            # FIXED: Actually filter by username
            cursor.execute("SELECT * FROM admins WHERE admin_username=%s AND admin_password=%s", (username, password))
            row = cursor.fetchone()
            
            if row:
                print("\n✅ Login successful!")
                return True # Proceed to admin menu
            else:
                print("\n❌ Invalid credentials")
                count+=1
                
                if count>=3:
                    print("You have exceeded the maximum number of attempts.")
                    choice=input("Do you want to change credentials using OTP? (y/n) : ").lower()
                    if choice=='y':
                        email=input("Enter your registered email: ")
                        cursor.execute("SELECT * FROM admins WHERE admin_email=%s", (email,))
                        email_row = cursor.fetchone()
                        
                        if email_row:
                            otp = VerifyOtp()
                            if otp.check_login(email, update_admin_credentials):
                                print("Please login with your new credentials.")
                                count = 0 # reset count
                                continue
                            else:
                                return False
                        else:
                            print("Email does not match our records.")
                            return False
                    else:
                        print("Thank you for using our service.")
                        return False
                else:
                    ch=input("Do you want to try again? (y/n) : ").lower()
                    if ch=='y':
                        continue
                    else:
                        print("Thank you for using our service.")
                        return
        except Exception as e:
            print(e)
            return False