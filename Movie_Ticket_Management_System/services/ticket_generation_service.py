from db import conn


def generate_ticket(booking_id):

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            b.booking_id,
            b.user_id,
            b.booking_date,
            b.total_amount,

            m.movie_name,
            m.language,

            t.theater_name,
            t.location,

            s.show_date,
            s.show_time,

            se.seat_number,
            se.seat_type,
            se.seat_price,

            p.payment_mode,
            p.payment_amount,
            p.payment_date

        FROM bookings b

        JOIN shows s
            ON b.show_id = s.show_id

        JOIN movies m
            ON s.movie_id = m.movie_id

        JOIN theaters t
            ON s.theater_id = t.theater_id

        JOIN seats se
            ON b.seat_id = se.seat_id

        LEFT JOIN payments p
            ON b.booking_id = p.booking_id

        WHERE b.booking_id = %s
    """

    cursor.execute(query, (booking_id,))
    ticket = cursor.fetchone()

    cursor.close()

    return ticket