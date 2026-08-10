import mysql.connector
from db import conn, cursor
from models.user import User

def register_user():
    try:
        print("\n========== USER REGISTRATION ==========")
        full_name = input("Full Name : ")
        email = input("Email : ")
        mobile = input("Mobile : ")
        username = input("Username : ")
        password = input("Password : ")

        cursor.execute("INSERT INTO users (full_name, email, mobile, username, password) VALUES (%s, %s, %s, %s, %s)", 
                       (full_name, email, mobile, username, password))
        conn.commit()
        print("\nRegistration Successful!\nUser ID :", cursor.lastrowid)
    except mysql.connector.IntegrityError:
        conn.rollback()
        print("\nRegistration Failed!\nEmail, Mobile or Username already exists.")
    except Exception as e:
        conn.rollback()
        print("\nError :", e)

def view_profile(user_id):
    try:
        cursor.execute("SELECT user_id, full_name, email, mobile, username FROM users WHERE user_id = %s", (user_id,))
        user_record = cursor.fetchone()
        if not user_record:
            print("\nUser Not Found.")
            return
        User(user_id=user_record[0], full_name=user_record[1], email=user_record[2], mobile=user_record[3], username=user_record[4]).display_user()
    except Exception as e:
        print("\nError :", e)

def update_profile(user_id):
    try:
        print("\n========== UPDATE PROFILE ==========")
        full_name = input("New Full Name : ")
        email = input("New Email : ")
        mobile = input("New Mobile : ")
        username = input("New Username : ")

        cursor.execute("UPDATE users SET full_name = %s, email = %s, mobile = %s, username = %s WHERE user_id = %s", (full_name, email, mobile, username, user_id))
        conn.commit()
        print("\nProfile Updated Successfully!")
    except mysql.connector.IntegrityError:
        conn.rollback()
        print("\nUpdate Failed!\nEmail, Mobile or Username already exists.")
    except Exception as e:
        conn.rollback()
        print("\nError :", e)

def update_user_credentials(email):
    while True:
        try:
            newname=input("Enter full name : ")
            newmobile=input("Enter Mobile number : ")
            newusername=input("Enter new username : ")
            newpass=input("Enter new password : ")
            newemail=input("Enter new email : ")
            reenter_email=input("ReEnter new email : ")
            if newemail == reenter_email:
                cursor.execute("update users set full_name=%s,email=%s, mobile=%s, username=%s, password=%s where email=%s",(newname,newemail,newmobile,newusername,newpass,email))
                conn.commit()
                print("Credentials updated successfully")
                return True
            else:
                print("Enter same email!")
                choice=input("Want to try again (y/n) : ").lower()
                if choice != 'y':
                    return False
        except Exception as e:
            print(e)
            return False