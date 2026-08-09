from db import conn,cursor

def update_admin_credentials():
    while True:
        try:
            cursor.execute("select * from admins")
            rows=cursor.fetchone()
            newusername=input("Enter new username : ")
            newpass=input("Enter new password : ")
            newemail=input("Enter new email : ")
            reenter_email=input("ReEnter new email : ")
            if newemail == reenter_email:
                cursor.execute("update admins set admin_username=%s,admin_password=%s, admin_email=%s where admin_id=%s",(newusername,newpass,newemail,rows[0]))
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