from datetime import datetime
import mysql.connector
from db import conn, cursor
from models.payment import Payment

def make_payment(booking_id):
    try:
        print("\n===== MAKE PAYMENT =====")
        cursor.execute("""
            SELECT b.booking_id, s.seat_number, s.seat_type, s.seat_price
            FROM bookings b JOIN seats s ON b.seat_id = s.seat_id
            WHERE b.booking_id = %s ORDER BY s.seat_id
        """, (booking_id,))
        booking_records = cursor.fetchall()
        if not booking_records:
            print("\nBooking Not Found.")
            return

        cursor.execute("SELECT payment_id FROM payments WHERE booking_id = %s", (booking_id,))
        existing_payment = cursor.fetchone()
        if existing_payment:
            print(f"\nPayment already exists for this Booking ID.\nPayment ID : {existing_payment[0]}")
            return

        payment_amount = 0.0
        print("\n========== BOOKING DETAILS ==========")
        print(f"Booking ID : {booking_id}\nNumber of Tickets : {len(booking_records)}\n\n---------- SEAT DETAILS ----------")
        for record in booking_records:
            seat_price = float(record[3])
            payment_amount += seat_price
            print(f"Seat : {record[1]} | Type : {record[2]} | Price : ₹{seat_price:.2f}")
        print(f"------------------------------------\nTotal Amount : ₹{payment_amount:.2f}")

        print("\n---------- PAYMENT MODE ----------\n1. UPI\n2. Card\n3. Cash")
        payment_choice = input("Select Payment Mode: ")
        payment_modes = {"1": "UPI", "2": "Card", "3": "Cash"}
        payment_mode = payment_modes.get(payment_choice)

        if not payment_mode:
            print("\nInvalid payment mode.")
            return

        payment_date = datetime.now()
        cursor.execute("INSERT INTO payments (booking_id, payment_mode, payment_amount, payment_date) VALUES (%s, %s, %s, %s)", 
                       (booking_id, payment_mode, payment_amount, payment_date))
        conn.commit()
        
        payment = Payment(payment_id=cursor.lastrowid, booking_id=booking_id, payment_amount=payment_amount, payment_mode=payment_mode, status="Successful", payment_date=payment_date)
        print("\nPayment completed successfully!")
        payment.display_payment()
    except Exception as e:
        conn.rollback()
        print("\nPayment failed!\nError :", e)

def view_payments():
    try:
        print("\n===== VIEW PAYMENT =====")
        booking_id = int(input("Enter Booking ID: "))
        cursor.execute("SELECT payment_id, booking_id, payment_mode, payment_amount, payment_date FROM payments WHERE booking_id = %s", (booking_id,))
        record = cursor.fetchone()
        if not record:
            print("\nPayment Not Found.")
            return
        Payment(payment_id=record[0], booking_id=record[1], payment_mode=record[2], payment_amount=record[3], status="Successful", payment_date=record[4]).display_payment()
    except Exception as e:
        print("\nError :", e)

def generate_receipt():
    try:
        print("\n===== GENERATE RECEIPT =====")
        booking_id = int(input("Enter Booking ID: "))
        cursor.execute("SELECT payment_id, booking_id, payment_mode, payment_amount, payment_date FROM payments WHERE booking_id = %s", (booking_id,))
        record = cursor.fetchone()
        if not record:
            print("\nPayment Not Found.")
            return
        
        payment = Payment(payment_id=record[0], booking_id=record[1], payment_mode=record[2], payment_amount=record[3], status="Successful", payment_date=record[4])
        print("\n" + "=" * 45 + "\n             PAYMENT RECEIPT\n" + "=" * 45)
        print(f"Payment ID     : {payment.payment_id}\nBooking ID     : {payment.booking_id}\nAmount         : ₹{payment.payment_amount:.2f}\nPayment Mode   : {payment.payment_mode}\nStatus         : {payment.status}\nPayment Date   : {payment.payment_date}")
        print("=" * 45 + "\n          Payment Successful!\n" + "=" * 45)
    except Exception as e:
        print("\nError :", e)