from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from services.ticket_generation_service import generate_ticket

console = Console()


def ticket_generation_menu():

    while True:

        console.print(
            Panel.fit(
                "[bold cyan] TICKET GENERATION[/bold cyan]",
                border_style="cyan"
            )
        )

        print("1. Generate Ticket")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_ticket_menu()

        elif choice == "2":
            console.print(
                Panel.fit(
                    "[bold green]Thank you for using Ticket Generation. "
                    "Have a great day![/bold green]",
                    border_style="green"
                )
            )
            break

        else:
            console.print(
                "[bold red]Invalid choice. Please select 1 or 2.[/bold red]"
            )


def generate_ticket_menu():

    try:
        booking_id = input("Enter Booking ID: ").strip()

        if not booking_id:
            console.print(
                "[bold red]Booking ID cannot be empty.[/bold red]"
            )
            return

        if not booking_id.isdigit():
            console.print(
                "[bold red]Please enter a valid numeric Booking ID.[/bold red]"
            )
            return

        ticket = generate_ticket(int(booking_id))

        if ticket is None:
            console.print(
                "[bold yellow]No booking found for this Booking ID.[/bold yellow]"
            )
            return

        display_ticket(ticket)

    except Exception as e:
        console.print(
            f"[bold red]Unable to generate ticket: {e}[/bold red]"
        )


def display_ticket(ticket):

    table = Table(
        title="🎬 MOVIE TICKET",
        show_header=False,
        border_style="cyan"
    )

    table.add_row("Booking ID", str(ticket["booking_id"]))
    table.add_row("User ID", str(ticket["user_id"]))
    table.add_row("Movie", ticket["movie_name"])
    table.add_row("Language", ticket["language"])
    table.add_row("Theater", ticket["theater_name"])
    table.add_row("Location", ticket["location"])
    table.add_row("Show Date", str(ticket["show_date"]))
    table.add_row("Show Time", str(ticket["show_time"]))
    table.add_row("Seat", ticket["seat_number"])
    table.add_row("Seat Type", ticket["seat_type"])
    table.add_row("Seat Price", f"₹{ticket['seat_price']}")
    table.add_row("Total Amount", f"₹{ticket['total_amount']}")

    if ticket["payment_mode"]:
        table.add_row("Payment Mode", ticket["payment_mode"])
        table.add_row(
            "Payment Amount",
            f"₹{ticket['payment_amount']}"
        )
        table.add_row(
            "Payment Date",
            str(ticket["payment_date"])
        )
    else:
        table.add_row("Payment Status", "Payment Pending")

    console.print()
    console.print(table)

    console.print(
        "[bold green]Ticket generated successfully![/bold green]"
    )