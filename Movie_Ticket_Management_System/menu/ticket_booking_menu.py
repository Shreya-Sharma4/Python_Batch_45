from rich.console import Console
from rich.panel import Panel

from services.ticket_booking_services import (
    get_movies,
    get_theaters,
    get_show_dates,
    get_show_times,
    display_seat_layout,
    check_seat_availability,
    get_seat_price,
    create_booking,
    view_booking
)

console = Console()


# -------------------------------------------------
# BOOK TICKET
# -------------------------------------------------

def book_ticket(user_id):

    console.print(
        Panel.fit(
            "[bold cyan]BOOK TICKET[/bold cyan]"
        )
    )

    # STEP 1 - MOVIE

    movies = get_movies()

    if not movies:
        return

    movie_id = console.input(
        "[yellow]Enter Movie ID : [/yellow]"
    ).strip()

    # STEP 2 - THEATER

    theaters = get_theaters(movie_id)

    if not theaters:
        return

    theater_id = console.input(
        "[yellow]Enter Theater ID : [/yellow]"
    ).strip()

    # STEP 3 - DATE

    dates = get_show_dates(
        movie_id,
        theater_id
    )

    if not dates:
        return

    date_choice = console.input(
        "[yellow]Select Date No. : [/yellow]"
    ).strip()

    try:
        date_index = int(date_choice) - 1

        if date_index < 0 or date_index >= len(dates):
            console.print(
                "[bold red]Invalid Date Selection![/bold red]"
            )
            return

        show_date = dates[date_index][0]

    except ValueError:
        console.print(
            "[bold red]Enter a valid number.[/bold red]"
        )
        return

    # STEP 4 - SHOW TIME

    shows = get_show_times(
        movie_id,
        theater_id,
        show_date
    )

    if not shows:
        return

    show_id = console.input(
        "[yellow]Enter Show ID : [/yellow]"
    ).strip()

    # STEP 5 - SEAT LAYOUT

    seats = display_seat_layout(show_id)

    if not seats:
        return

    # STEP 6 - SELECT SEAT

    seat_id = console.input(
        "[yellow]Enter Seat ID : [/yellow]"
    ).strip()

    # STEP 7 - CHECK AVAILABILITY

    if not check_seat_availability(
        show_id,
        seat_id
    ):
        return

    # STEP 8 - GET PRICE

    price = get_seat_price(seat_id)

    if price is None:
        console.print(
            "[bold red]Invalid Seat ID![/bold red]"
        )
        return

    total_amount = price

    console.print(
        f"\n[bold cyan]Total Amount : ₹{total_amount:.2f}[/bold cyan]"
    )

    # STEP 9 - CONFIRM

    choice = console.input(
        "\n[yellow]Confirm Booking? (Y/N): [/yellow]"
    ).strip().lower()

    if choice != "y":
        console.print(
            "\n[bold cyan]Booking Cancelled.[/bold cyan]\n"
        )
        return

    # STEP 10 - SAVE BOOKING

    create_booking(
        user_id,
        show_id,
        seat_id,
        total_amount
    )


# CHECK SEAT AVAILABILITY

def seat_availability():

    console.print(
        Panel.fit(
            "[bold cyan]CHECK SEAT AVAILABILITY[/bold cyan]"
        )
    )

    show_id = console.input(
        "[yellow]Enter Show ID : [/yellow]"
    ).strip()

    display_seat_layout(show_id)


# VIEW BOOKING

def booking_details(user_id):

    console.print(
        Panel.fit(
            "[bold cyan]VIEW BOOKING[/bold cyan]"
        )
    )

    view_booking(user_id)



# TICKET BOOKING MENU

def ticket_booking_menu(user_id):

    while True:

        console.print(
            Panel.fit(
                "[bold cyan]TICKET BOOKING MENU[/bold cyan]"
            )
        )

        console.print("1. Book Ticket")
        console.print("2. Check Seat Availability")
        console.print("3. View Booking")
        console.print("4. Back")

        choice = console.input(
            "\n[yellow]Enter your choice : [/yellow]"
        ).strip()

        if choice == "1":

            book_ticket(user_id)

        elif choice == "2":

            seat_availability()

        elif choice == "3":

            booking_details(user_id)

        elif choice == "4":

            break

        else:

            console.print(
                "[bold red]Invalid Choice![/bold red]"
            )