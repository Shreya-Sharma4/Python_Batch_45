from db import conn
from models.booking import Booking
from rich.console import Console
from rich.table import Table

console = Console()

# GET MOVIES

def get_movies():

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT movie_id, movie_name
            FROM movies
            ORDER BY movie_name
        """)

        movies = cursor.fetchall()

        if not movies:
            console.print("[bold red]No movies available.[/bold red]")
            return []

        table = Table(title="AVAILABLE MOVIES")

        table.add_column("Movie ID", style="cyan")
        table.add_column("Movie Name", style="green")

        for movie in movies:
            table.add_row(
                str(movie[0]),
                movie[1]
            )

        console.print(table)

        return movies

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return []

    finally:
        cursor.close()


# GET THEATERS

def get_theaters(movie_id):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT t.theater_id, t.theater_name, t.location
            FROM theaters t
            JOIN shows s
                ON t.theater_id = s.theater_id
            WHERE s.movie_id = %s
            ORDER BY t.theater_name
        """, (movie_id,))

        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "[bold red]No theaters available for this movie.[/bold red]"
            )
            return []

        table = Table(title="AVAILABLE THEATERS")

        table.add_column("Theater ID", style="cyan")
        table.add_column("Theater Name", style="green")
        table.add_column("Location", style="magenta")

        for theater in theaters:
            table.add_row(
                str(theater[0]),
                theater[1],
                theater[2]
            )

        console.print(table)

        return theaters

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return []

    finally:
        cursor.close()


# GET SHOW DATES

def get_show_dates(movie_id, theater_id):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT show_date
            FROM shows
            WHERE movie_id = %s
            AND theater_id = %s
            ORDER BY show_date
        """, (movie_id, theater_id))

        dates = cursor.fetchall()

        if not dates:
            console.print(
                "[bold red]No shows available.[/bold red]"
            )
            return []

        table = Table(title="AVAILABLE DATES")

        table.add_column("No.", style="cyan")
        table.add_column("Show Date", style="green")

        for index, date in enumerate(dates, start=1):
            table.add_row(
                str(index),
                str(date[0])
            )

        console.print(table)

        return dates

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return []

    finally:
        cursor.close()


# GET SHOW TIMES

def get_show_times(movie_id, theater_id, show_date):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT show_id, show_time
            FROM shows
            WHERE movie_id = %s
            AND theater_id = %s
            AND show_date = %s
            ORDER BY show_time
        """, (movie_id, theater_id, show_date))

        shows = cursor.fetchall()

        if not shows:
            console.print(
                "[bold red]No shows available for this date.[/bold red]"
            )
            return []

        table = Table(title="AVAILABLE SHOW TIMES")

        table.add_column("Show ID", style="cyan")
        table.add_column("Show Time", style="green")

        for show in shows:
            table.add_row(
                str(show[0]),
                str(show[1])
            )

        console.print(table)

        return shows

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return []

    finally:
        cursor.close()


# DISPLAY SEAT LAYOUT

def display_seat_layout(show_id):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                s.seat_id,
                s.seat_number,
                s.seat_type,
                s.seat_price
            FROM seats s
            JOIN shows sh
                ON s.theater_id = sh.theater_id
            WHERE sh.show_id = %s
            ORDER BY s.seat_id
        """, (show_id,))

        seats = cursor.fetchall()

        if not seats:
            console.print(
                "[bold red]No seats available.[/bold red]"
            )
            return []

        table = Table(title="SEAT LAYOUT")

        table.add_column("Seat ID", style="cyan")
        table.add_column("Seat", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Price", style="magenta")
        table.add_column("Status", style="blue")


        for seat in seats:

            # Check whether the seat is booked
            cursor.execute("""
                SELECT booking_id
                FROM bookings
                WHERE show_id = %s
                AND seat_id = %s
            """, (show_id, seat[0]))

            booking = cursor.fetchone()

            if booking:
                status = "Booked"
            else:
                status = "Available"

            table.add_row(
                str(seat[0]),
                seat[1],
                seat[2],
                f"₹{seat[3]}",
                status
            )

        console.print(table)

        return seats

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return []

    finally:
        cursor.close()

# CHECK SEAT AVAILABILITY

def check_seat_availability(show_id, seat_id):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT booking_id
            FROM bookings
            WHERE show_id = %s
            AND seat_id = %s
        """, (show_id, seat_id))

        booking = cursor.fetchone()

        if booking:
            console.print(
                "[bold red]✗ Seat is already booked.[/bold red]"
            )
            return False

        console.print(
            "[bold green]✓ Seat is available.[/bold green]"
        )
        return True

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return False

    finally:
        cursor.close()


# GET SEAT PRICE

def get_seat_price(seat_id):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT seat_price
            FROM seats
            WHERE seat_id = %s
        """, (seat_id,))

        seat = cursor.fetchone()

        if seat:
            return float(seat[0])

        return None

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return None

    finally:
        cursor.close()


# CREATE BOOKING

def create_booking(user_id, show_id, seat_id, total_amount):

    cursor = conn.cursor()

    try:

        booking = Booking(
            user_id=user_id,
            show_id=show_id,
            seat_id=seat_id,
            total_amount=total_amount
        )

        query = """
            INSERT INTO bookings(
                user_id,
                show_id,
                seat_id,
                total_amount
            )
            VALUES(%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                booking.user_id,
                booking.show_id,
                booking.seat_id,
                booking.total_amount
            )
        )

        conn.commit()

        booking_id = cursor.lastrowid

        console.print(
            "\n[bold green]✓ Booking Confirmed Successfully![/bold green]"
        )

        console.print(
            f"[bold cyan]Booking ID : {booking_id}[/bold cyan]\n"
        )

        return booking_id

    except Exception as e:

        conn.rollback()

        console.print(
            f"[bold red]Booking Error:[/bold red] {e}"
        )

        return None

    finally:
        cursor.close()


# VIEW BOOKING


def view_booking(user_id):

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                b.booking_id,
                m.movie_name,
                t.theater_name,
                s.show_date,
                s.show_time,
                se.seat_number,
                se.seat_type,
                b.booking_date,
                b.total_amount
            FROM bookings b

            JOIN shows s
                ON b.show_id = s.show_id

            JOIN movies m
                ON s.movie_id = m.movie_id

            JOIN theaters t
                ON s.theater_id = t.theater_id

            JOIN seats se
                ON b.seat_id = se.seat_id

            WHERE b.user_id = %s

            ORDER BY b.booking_id DESC
        """, (user_id,))

        bookings = cursor.fetchall()

        if not bookings:
            console.print(
                "\n[bold red]No bookings found.[/bold red]\n"
            )
            return

        table = Table(
            title="MY BOOKINGS",
            show_lines=True
        )

        table.add_column("Booking ID", style="cyan")
        table.add_column("Movie", style="green")
        table.add_column("Theater", style="yellow")
        table.add_column("Date", style="magenta")
        table.add_column("Time", style="blue")
        table.add_column("Seat", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Booking Date", style="yellow")
        table.add_column("Amount", style="magenta")

        for booking in bookings:

            table.add_row(
                str(booking[0]),
                booking[1],
                booking[2],
                str(booking[3]),
                str(booking[4]),
                booking[5],
                booking[6],
                str(booking[7]),
                f"₹{booking[8]}"
            )

        console.print(table)

    except Exception as e:
        console.print(
            f"[bold red]Error:[/bold red] {e}"
        )

    finally:
        cursor.close()