from rich.console import Console
from rich.panel import Panel

from services.ticket_booking_services import (
    get_movies,
    get_available_shows,
    display_seat_layout,
    check_seat_availability,
    get_seat_price,
    create_multiple_bookings,
    view_booking
)

console = Console()


# -------------------------------------------------
# BOOK TICKET
# -------------------------------------------------

def book_ticket(user_id):

    try:
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

        if not movie_id.isdigit():
            console.print(
                "[bold red]Movie ID must be a number.[/bold red]"
            )
            return

        movie_id = int(movie_id)

        # STEP 2 - THEATER + DATE + SHOW + TIME
        shows = get_available_shows(movie_id)

        if not shows:
            return

        show_id = console.input(
            "[yellow]Enter Show ID : [/yellow]"
        ).strip()

        if not show_id.isdigit():
            console.print(
                "[bold red]Show ID must be a number.[/bold red]"
            )
            return

        show_id = int(show_id)

        # Check whether selected show exists
        selected_show = None

        for show in shows:
            if show[0] == show_id:
                selected_show = show
                break

        if selected_show is None:
            console.print(
                "[bold red]Invalid Show ID.[/bold red]"
            )
            return

        # STEP 3 - SEAT LAYOUT
        seats = display_seat_layout(show_id)

        if not seats:
            return

        # STEP 4 - MULTIPLE SEATS
        seat_input = console.input(
            "\n[yellow]Enter Seat IDs (example: 1,2,3): [/yellow]"
        ).strip()

        if not seat_input:
            console.print(
                "[bold red]Please enter at least one Seat ID.[/bold red]"
            )
            return

        try:
            seat_ids = [
                int(seat.strip())
                for seat in seat_input.split(",")
            ]
        except ValueError:
            console.print(
                "[bold red]Enter valid numeric Seat IDs.[/bold red]"
            )
            return

        # Remove duplicate seat IDs
        seat_ids = list(dict.fromkeys(seat_ids))

        # STEP 5 - CHECK ALL SEATS
        selected_seats = []
        total_amount = 0

        for seat_id in seat_ids:

            available = check_seat_availability(
                show_id,
                seat_id
            )

            if not available:
                console.print(
                    f"[bold red]Seat ID {seat_id} cannot be booked.[/bold red]"
                )
                return

            price = get_seat_price(seat_id)

            if price is None:
                console.print(
                    f"[bold red]Invalid Seat ID: {seat_id}[/bold red]"
                )
                return

            selected_seats.append(
                (seat_id, price)
            )

            total_amount += price

        # STEP 6 - TOTAL
        console.print(
            f"\n[bold cyan]Number of Seats : "
            f"{len(selected_seats)}[/bold cyan]"
        )

        console.print(
            f"[bold cyan]Total Amount : "
            f"₹{total_amount:.2f}[/bold cyan]"
        )

        # STEP 7 - CONFIRM
        choice = console.input(
            "\n[yellow]Confirm Booking? (Y/N): [/yellow]"
        ).strip().lower()

        if choice != "y":
            console.print(
                "\n[bold cyan]Booking Cancelled.[/bold cyan]\n"
            )
            return

        # STEP 8 - SAVE ALL BOOKINGS
        booking_ids = create_multiple_bookings(
            user_id,
            show_id,
            selected_seats
        )

        if booking_ids:
            console.print(
                "\n[bold green]"
                "✓ All selected seats booked successfully!"
                "[/bold green]"
            )

            console.print(
                f"[bold cyan]Booking IDs : "
                f"{', '.join(map(str, booking_ids))}[/bold cyan]\n"
            )

    except Exception as e:
        console.print(
            f"[bold red]Booking Error: {e}[/bold red]"
        )


# -------------------------------------------------
# CHECK SEAT AVAILABILITY
# -------------------------------------------------

def seat_availability():

    # This functionality will be added by the collaborator.
    pass


# -------------------------------------------------
# VIEW BOOKING
# -------------------------------------------------

def booking_details(user_id):

    try:
        console.print(
            Panel.fit(
                "[bold cyan]MY BOOKINGS[/bold cyan]"
            )
        )

        # Only this user's bookings are displayed
        view_booking(user_id)

    except Exception as e:
        console.print(
            f"[bold red]Unable to view bookings: {e}[/bold red]"
        )


# -------------------------------------------------
# TICKET BOOKING MENU
# -------------------------------------------------

def ticket_booking_menu(user_id):

    while True:

        try:
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
                    "[bold red]Invalid Choice! "
                    "Please select 1-4.[/bold red]"
                )

        except KeyboardInterrupt:
            console.print(
                "\n[bold yellow]Operation cancelled.[/bold yellow]"
            )
            break

        except Exception as e:
            console.print(
                f"[bold red]Menu Error: {e}[/bold red]"
            )
