from models.payment import Payment
from db import get_connection


def make_payment(booking_id, amount, payment_method):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO payments
            (booking_id, amount, payment_method, status)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            booking_id,
            amount,
            payment_method,
            "Successful"
        )

        cursor.execute(query, values)
        connection.commit()

        payment_id = cursor.lastrowid

        payment = Payment(
            payment_id=payment_id,
            booking_id=booking_id,
            amount=amount,
            payment_method=payment_method,
            status="Successful"
        )

        print("\nPayment completed successfully!")
        payment.display_payment()

    except Exception as error:
        if connection:
            connection.rollback()

        print(f"\nPayment failed: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def view_payments():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                payment_id,
                booking_id,
                amount,
                payment_method,
                status,
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
                status=record[4],
                payment_date=record[5]
            )

            payment.display_payment()

    except Exception as error:
        print(f"\nUnable to retrieve payments: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()