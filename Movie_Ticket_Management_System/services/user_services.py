import mysql.connector

from db import conn, cursor
from models.user import User


# =========================================================
# REGISTER
# =========================================================

def register_user():

    try:

        print("\n========== USER REGISTRATION ==========")

        full_name = input("Full Name : ")
        email = input("Email : ")
        mobile = input("Mobile : ")
        username = input("Username : ")
        password = input("Password : ")

        user = User(
            full_name=full_name,
            email=email,
            mobile=mobile,
            username=username,
            password=password
        )

        query = """
        INSERT INTO users
        (
            full_name,
            email,
            mobile,
            username,
            password
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            user.full_name,
            user.email,
            user.mobile,
            user.username,
            user.password
        )

        cursor.execute(query, values)

        conn.commit()

        print("\nRegistration Successful!")
        print("User ID :", cursor.lastrowid)

    except mysql.connector.IntegrityError:

        conn.rollback()

        print("\nRegistration Failed!")
        print("Email, Mobile or Username already exists.")

    except mysql.connector.Error as e:

        conn.rollback()

        print("\nDatabase Error :", e)

    except Exception as e:

        conn.rollback()

        print("\nError :", e)


# =========================================================
# LOGIN
# =========================================================

def login_user():

    try:

        print("\n========== USER LOGIN ==========")

        username = input("Username : ")
        password = input("Password : ")

        query = """
        SELECT
            user_id,
            full_name,
            email,
            mobile,
            username
        FROM users
        WHERE username = %s
        AND password = %s
        """

        values = (
            username,
            password
        )

        cursor.execute(query, values)

        user_record = cursor.fetchone()

        if user_record:

            print("\nLogin Successful!")
            print("Welcome,", user_record[1])

            return user_record[0]

        print("\nInvalid Username or Password.")

        return None

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

        return None

    except Exception as e:

        print("\nError :", e)

        return None


# =========================================================
# VIEW PROFILE
# =========================================================

def view_profile(user_id):

    try:

        query = """
        SELECT
            user_id,
            full_name,
            email,
            mobile,
            username
        FROM users
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        user_record = cursor.fetchone()

        if not user_record:

            print("\nUser Not Found.")

            return

        user = User(
            user_id=user_record[0],
            full_name=user_record[1],
            email=user_record[2],
            mobile=user_record[3],
            username=user_record[4]
        )

        user.display_user()

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

    except Exception as e:

        print("\nError :", e)


# =========================================================
# UPDATE PROFILE
# =========================================================

def update_profile(user_id):

    try:

        query = """
        SELECT
            user_id,
            full_name,
            email,
            mobile,
            username
        FROM users
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        user_record = cursor.fetchone()

        if not user_record:

            print("\nUser Not Found.")

            return

        print("\n========== UPDATE PROFILE ==========")

        full_name = input("New Full Name : ")
        email = input("New Email : ")
        mobile = input("New Mobile : ")
        username = input("New Username : ")

        query = """
        UPDATE users
        SET
            full_name = %s,
            email = %s,
            mobile = %s,
            username = %s
        WHERE user_id = %s
        """

        values = (
            full_name,
            email,
            mobile,
            username,
            user_id
        )

        cursor.execute(query, values)

        conn.commit()

        print("\nProfile Updated Successfully!")

    except mysql.connector.IntegrityError:

        conn.rollback()

        print("\nUpdate Failed!")
        print("Email, Mobile or Username already exists.")

    except mysql.connector.Error as e:

        conn.rollback()

        print("\nDatabase Error :", e)

    except Exception as e:

        conn.rollback()

        print("\nError :", e)


# =========================================================
# CHANGE PASSWORD
# =========================================================

def change_password(user_id):

    try:

        print("\n========== CHANGE PASSWORD ==========")

        current_password = input("Current Password : ")
        new_password = input("New Password : ")
        confirm_password = input("Confirm New Password : ")

        query = """
        SELECT password
        FROM users
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        user_record = cursor.fetchone()

        if not user_record:

            print("\nUser Not Found.")

            return

        if user_record[0] != current_password:

            print("\nCurrent Password is incorrect.")

            return

        if new_password != confirm_password:

            print("\nNew Password and Confirm Password do not match.")

            return

        query = """
        UPDATE users
        SET password = %s
        WHERE user_id = %s
        """

        values = (
            new_password,
            user_id
        )

        cursor.execute(query, values)

        conn.commit()

        print("\nPassword Changed Successfully!")

    except mysql.connector.Error as e:

        conn.rollback()

        print("\nDatabase Error :", e)

    except Exception as e:

        conn.rollback()

        print("\nError :", e)
