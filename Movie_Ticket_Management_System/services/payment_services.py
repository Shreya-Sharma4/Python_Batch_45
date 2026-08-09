import mysql.connector

from db import conn, cursor
from models.payment import Payment


# ---------------- MAKE PAYMENT ----------------

def make_payment(booking_id):

    try:

        print("\n===== MAKE PAYMENT =====")

        # Get ALL seats belonging to the booking ID
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

        # ---------------- BOOKING DETAILS ----------------

        total_amount = 0.0

        print("\n========== BOOKING DETAILS ==========")
        print(f"Booking ID : {booking_id}")
        print(f"Number of Tickets : {len(booking_records)}")

        print("\n---------- SEAT DETAILS ----------")

        for record in booking_records:

            seat_number = record[1]
            seat_type = record[2]
            seat_price = float(record[3])

            total_amount += seat_price

            print(
                f"Seat : {seat_number} | "
                f"Type : {seat_type} | "
                f"Price : ₹{seat_price:.2f}"
            )

        print("------------------------------------")
        print(f"Total Amount : ₹{total_amount:.2f}")

        # ---------------- PAYMENT METHOD ----------------

        print("\n---------- PAYMENT METHODS ----------")
        print("1. UPI")
        print("2. Card")
        print("3. Cash")

        payment_choice = input(
            "Select Payment Method: "
        )

        payment_methods = {
            "1": "UPI",
            "2": "Card",
            "3": "Cash"
        }

        payment_method = payment_methods.get(payment_choice)

        if payment_method is None:

            print("\nInvalid payment method.")
            return

        # ---------------- INSERT PAYMENT ----------------

        query = """
        INSERT INTO payments
        (booking_id, amount, payment_method)
        VALUES (%s, %s, %s)
        """

        values = (
            booking_id,
            total_amount,
            payment_method
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
            amount=total_amount,
            payment_method=payment_method,
            status=status
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


# ---------------- VIEW PAYMENTS ----------------

def view_payments():

    try:

        query = """
        SELECT
            payment_id,
            booking_id,
            amount,
            payment_method,
            payment_date
        FROM payments
        ORDER BY payment_id
        """

        cursor.execute(query)

        payment_records = cursor.fetchall()

        if not payment_records:

            print("\nNo payment records found.")
            return

        print("\n========== ALL PAYMENT RECORDS ==========")

        for record in payment_records:

            payment = Payment(
                payment_id=record[0],
                booking_id=record[1],
                amount=record[2],
                payment_method=record[3],
                status="Successful",
                payment_date=record[4]
            )

            payment.display_payment()

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

    except Exception as e:

        print("\nError :", e)