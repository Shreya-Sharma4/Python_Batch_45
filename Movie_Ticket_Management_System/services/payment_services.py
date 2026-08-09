from datetime import datetime
import mysql.connector

from db import conn, cursor
from models.payment import Payment


# ---------------- MAKE PAYMENT ----------------

def make_payment(booking_id):

    try:

        print("\n===== MAKE PAYMENT =====")

        # Get all seats belonging to the booking ID
        query = """
        SELECT
            b.booking_id,
            s.seat_number,
            s.seat_type,
            s.seat_price
        FROM bookings b
        JOIN seats s
            ON b.seat_id = s.seat_id
        WHERE b.booking_id = %s
        ORDER BY s.seat_id
        """

        cursor.execute(query, (booking_id,))

        booking_records = cursor.fetchall()

        # Check whether booking exists
        if not booking_records:

            print("\nBooking Not Found.")
            return

        # Check whether payment already exists
        query = """
        SELECT payment_id
        FROM payments
        WHERE booking_id = %s
        """

        cursor.execute(query, (booking_id,))

        existing_payment = cursor.fetchone()

        if existing_payment:

            print("\nPayment already exists for this Booking ID.")
            print(f"Payment ID : {existing_payment[0]}")
            return

        # ---------------- BOOKING DETAILS ----------------

        payment_amount = 0.0

        print("\n========== BOOKING DETAILS ==========")
        print(f"Booking ID : {booking_id}")
        print(f"Number of Tickets : {len(booking_records)}")

        print("\n---------- SEAT DETAILS ----------")

        for record in booking_records:

            seat_number = record[1]
            seat_type = record[2]
            seat_price = float(record[3])

            payment_amount += seat_price

            print(
                f"Seat : {seat_number} | "
                f"Type : {seat_type} | "
                f"Price : ₹{seat_price:.2f}"
            )

        print("------------------------------------")
        print(f"Total Amount : ₹{payment_amount:.2f}")

        # ---------------- PAYMENT MODE ----------------

        print("\n---------- PAYMENT MODE ----------")
        print("1. UPI")
        print("2. Card")
        print("3. Cash")

        payment_choice = input(
            "Select Payment Mode: "
        )

        payment_modes = {
            "1": "UPI",
            "2": "Card",
            "3": "Cash"
        }

        payment_mode = payment_modes.get(payment_choice)

        if payment_mode is None:

            print("\nInvalid payment mode.")
            return

        # ---------------- PAYMENT DATE ----------------

        payment_date = datetime.now()

        # ---------------- INSERT PAYMENT ----------------

        query = """
        INSERT INTO payments
        (
            booking_id,
            payment_mode,
            payment_amount,
            payment_date
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            booking_id,
            payment_mode,
            payment_amount,
            payment_date
        )

        cursor.execute(query, values)

        conn.commit()

        payment_id = cursor.lastrowid

        # Status is handled by Python.
        # It is NOT stored in the database.

        status = "Successful"

        payment = Payment(
            payment_id=payment_id,
            booking_id=booking_id,
            payment_amount=payment_amount,
            payment_mode=payment_mode,
            status=status,
            payment_date=payment_date
        )

        print("\nPayment completed successfully!")

        payment.display_payment()

    except mysql.connector.Error as e:

        conn.rollback()

        print("\nPayment failed!")
        print("Status : Failed")
        print("Database Error :", e)

    except Exception as e:

        conn.rollback()

        print("\nPayment failed!")
        print("Status : Failed")
        print("Error :", e)


# ---------------- VIEW PAYMENT ----------------

def view_payments():

    try:

        print("\n===== VIEW PAYMENT =====")

        booking_id = int(
            input("Enter Booking ID: ")
        )

        query = """
        SELECT
            payment_id,
            booking_id,
            payment_mode,
            payment_amount,
            payment_date
        FROM payments
        WHERE booking_id = %s
        """

        cursor.execute(query, (booking_id,))

        payment_record = cursor.fetchone()

        if not payment_record:

            print("\nPayment Not Found.")
            return

        payment = Payment(
            payment_id=payment_record[0],
            booking_id=payment_record[1],
            payment_mode=payment_record[2],
            payment_amount=payment_record[3],
            status="Successful",
            payment_date=payment_record[4]
        )

        payment.display_payment()

    except ValueError:

        print("\nPlease enter a valid Booking ID.")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

    except Exception as e:

        print("\nError :", e)


# ---------------- GENERATE RECEIPT ----------------

def generate_receipt():

    try:

        print("\n===== GENERATE RECEIPT =====")

        booking_id = int(
            input("Enter Booking ID: ")
        )

        query = """
        SELECT
            payment_id,
            booking_id,
            payment_mode,
            payment_amount,
            payment_date
        FROM payments
        WHERE booking_id = %s
        """

        cursor.execute(query, (booking_id,))

        payment_record = cursor.fetchone()

        if not payment_record:

            print("\nPayment Not Found.")
            return

        payment = Payment(
            payment_id=payment_record[0],
            booking_id=payment_record[1],
            payment_mode=payment_record[2],
            payment_amount=payment_record[3],
            status="Successful",
            payment_date=payment_record[4]
        )

        print("\n")
        print("=" * 45)
        print("             PAYMENT RECEIPT")
        print("=" * 45)

        print(f"Payment ID     : {payment.payment_id}")
        print(f"Booking ID     : {payment.booking_id}")
        print(f"Amount         : ₹{payment.payment_amount:.2f}")
        print(f"Payment Mode   : {payment.payment_mode}")
        print(f"Status         : {payment.status}")
        print(f"Payment Date   : {payment.payment_date}")

        print("=" * 45)
        print("          Payment Successful!")
        print("=" * 45)

    except ValueError:

        print("\nPlease enter a valid Booking ID.")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

    except Exception as e:

        print("\nError :", e)