import mysql.connector

from db import conn, cursor
from models.ticket import Ticket

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


# ==========================================================
# VIEW ACTIVE TICKETS
# ==========================================================

def view_tickets():

    console.print(
        Panel(
            "[bold cyan]🎟️ VIEW ACTIVE TICKETS[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        query = """
        SELECT
            booking_id,
            user_id,
            show_id,
            seat_id,
            booking_date,
            total_amount,
            status
        FROM tickets
        WHERE status = 'Booked'
        ORDER BY booking_id
        """

        cursor.execute(query)

        tickets = cursor.fetchall()

        if not tickets:

            console.print(
                Panel(
                    "[yellow]⚠️ No active tickets found.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        table = Table(
            title="🎟️ ACTIVE TICKETS",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True
        )

        table.add_column(
            "Booking ID",
            justify="center",
            style="bold yellow"
        )

        table.add_column(
            "User ID",
            justify="center"
        )

        table.add_column(
            "Show ID",
            justify="center"
        )

        table.add_column(
            "Seat ID",
            justify="center"
        )

        table.add_column(
            "Booking Date",
            justify="center",
            style="cyan"
        )

        table.add_column(
            "Amount",
            justify="right",
            style="green"
        )

        table.add_column(
            "Status",
            justify="center",
            style="bold green"
        )

        for row in tickets:

            ticket = Ticket(
                booking_id=row[0],
                user_id=row[1],
                show_id=row[2],
                seat_id=row[3],
                booking_date=row[4],
                total_amount=row[5],
                status=row[6]
            )

            table.add_row(
                str(ticket.booking_id),
                str(ticket.user_id),
                str(ticket.show_id),
                str(ticket.seat_id),
                str(ticket.booking_date),
                f"₹{ticket.total_amount}",
                str(ticket.status)
            )

        console.print(table)

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]⚠️ View tickets cancelled.[/yellow]"
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# SEARCH TICKET
# ==========================================================

def search_ticket():

    console.print(
        Panel(
            "[bold cyan]🔍 SEARCH TICKET[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        booking_id = int(
            console.input(
                "[bold green]Enter Booking ID : [/bold green]"
            )
        )

        query = """
        SELECT
            booking_id,
            user_id,
            show_id,
            seat_id,
            booking_date,
            total_amount,
            status
        FROM tickets
        WHERE booking_id = %s
        """

        cursor.execute(
            query,
            (booking_id,)
        )

        row = cursor.fetchone()

        if not row:

            console.print(
                Panel(
                    "[bold red]❌ Ticket not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        ticket = Ticket(
            booking_id=row[0],
            user_id=row[1],
            show_id=row[2],
            seat_id=row[3],
            booking_date=row[4],
            total_amount=row[5],
            status=row[6]
        )

        table = Table(
            title="🎟️ TICKET DETAILS",
            box=box.ROUNDED,
            border_style="green"
        )

        table.add_column(
            "Field",
            style="bold cyan"
        )

        table.add_column(
            "Value",
            style="bold white"
        )

        table.add_row(
            "Booking ID",
            str(ticket.booking_id)
        )

        table.add_row(
            "User ID",
            str(ticket.user_id)
        )

        table.add_row(
            "Show ID",
            str(ticket.show_id)
        )

        table.add_row(
            "Seat ID",
            str(ticket.seat_id)
        )

        table.add_row(
            "Booking Date",
            str(ticket.booking_date)
        )

        table.add_row(
            "Total Amount",
            f"₹{ticket.total_amount}"
        )

        table.add_row(
            "Status",
            str(ticket.status)
        )

        console.print(table)

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Invalid Booking ID[/bold red]\n\n"
                "[yellow]Booking ID must be a number.[/yellow]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]⚠️ Search cancelled.[/yellow]"
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# CANCEL TICKET
# ==========================================================

def cancel_ticket():

    console.print(
        Panel(
            "[bold cyan]❌ CANCEL TICKET[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        booking_id = int(
            console.input(
                "[bold green]Enter Booking ID : [/bold green]"
            )
        )

        # --------------------------------------------------
        # GET TICKET
        # --------------------------------------------------

        query = """
        SELECT
            booking_id,
            user_id,
            show_id,
            seat_id,
            booking_date,
            total_amount,
            status
        FROM tickets
        WHERE booking_id = %s
        """

        cursor.execute(
            query,
            (booking_id,)
        )

        row = cursor.fetchone()

        if not row:

            console.print(
                Panel(
                    "[bold red]❌ Ticket not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        # --------------------------------------------------
        # CHECK STATUS
        # --------------------------------------------------

        if str(row[6]).lower() == "cancelled":

            console.print(
                Panel(
                    "[bold yellow]⚠️ This ticket is already "
                    "cancelled.[/bold yellow]",
                    border_style="yellow"
                )
            )

            return

        # --------------------------------------------------
        # CREATE TICKET OBJECT
        # --------------------------------------------------

        ticket = Ticket(
            booking_id=row[0],
            user_id=row[1],
            show_id=row[2],
            seat_id=row[3],
            booking_date=row[4],
            total_amount=row[5],
            status=row[6]
        )

        # --------------------------------------------------
        # DISPLAY TICKET
        # --------------------------------------------------

        table = Table(
            title="🎟️ TICKET DETAILS",
            box=box.ROUNDED,
            border_style="yellow"
        )

        table.add_column(
            "Field",
            style="bold cyan"
        )

        table.add_column(
            "Value",
            style="bold white"
        )

        table.add_row(
            "Booking ID",
            str(ticket.booking_id)
        )

        table.add_row(
            "User ID",
            str(ticket.user_id)
        )

        table.add_row(
            "Show ID",
            str(ticket.show_id)
        )

        table.add_row(
            "Seat ID",
            str(ticket.seat_id)
        )

        table.add_row(
            "Booking Date",
            str(ticket.booking_date)
        )

        table.add_row(
            "Total Amount",
            f"₹{ticket.total_amount}"
        )

        table.add_row(
            "Status",
            str(ticket.status)
        )

        console.print(table)

        # --------------------------------------------------
        # CONFIRM
        # --------------------------------------------------

        confirm = console.input(
            "\n[bold red]Are you sure you want to "
            "cancel this ticket? (Y/N) : [/bold red]"
        ).strip().lower()

        if confirm != "y":

            console.print(
                Panel(
                    "[yellow]❌ Cancellation cancelled.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        # --------------------------------------------------
        # CANCEL
        # --------------------------------------------------

        update_query = """
        UPDATE tickets
        SET status = 'Cancelled'
        WHERE booking_id = %s
        """

        cursor.execute(
            update_query,
            (booking_id,)
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Ticket cancelled successfully.[/bold green]",
                border_style="green"
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Invalid Booking ID[/bold red]\n\n"
                "[yellow]Booking ID must be a number.[/yellow]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        conn.rollback()

        console.print(
            "\n[yellow]⚠️ Ticket cancellation interrupted.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# VIEW CANCELLED TICKETS
# ==========================================================

def view_cancelled_tickets():

    console.print(
        Panel(
            "[bold cyan]📋 CANCELLED TICKETS[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        query = """
        SELECT
            booking_id,
            user_id,
            show_id,
            seat_id,
            booking_date,
            total_amount,
            status
        FROM tickets
        WHERE status = 'Cancelled'
        ORDER BY booking_id
        """

        cursor.execute(query)

        tickets = cursor.fetchall()

        if not tickets:

            console.print(
                Panel(
                    "[yellow]⚠️ No cancelled tickets found.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        table = Table(
            title="❌ CANCELLED TICKETS",
            box=box.ROUNDED,
            border_style="red",
            show_lines=True
        )

        table.add_column(
            "Booking ID",
            justify="center",
            style="bold yellow"
        )

        table.add_column(
            "User ID",
            justify="center"
        )

        table.add_column(
            "Show ID",
            justify="center"
        )

        table.add_column(
            "Seat ID",
            justify="center"
        )

        table.add_column(
            "Booking Date",
            justify="center"
        )

        table.add_column(
            "Amount",
            justify="right"
        )

        table.add_column(
            "Status",
            justify="center",
            style="bold red"
        )

        for row in tickets:

            ticket = Ticket(
                booking_id=row[0],
                user_id=row[1],
                show_id=row[2],
                seat_id=row[3],
                booking_date=row[4],
                total_amount=row[5],
                status=row[6]
            )

            table.add_row(
                str(ticket.booking_id),
                str(ticket.user_id),
                str(ticket.show_id),
                str(ticket.seat_id),
                str(ticket.booking_date),
                f"₹{ticket.total_amount}",
                str(ticket.status)
            )

        console.print(table)

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]⚠️ View cancelled tickets interrupted.[/yellow]"
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# TICKET MANAGEMENT MENU
# ==========================================================

def ticket_management():

    while True:

        try:

            console.clear()

            console.print(
                Panel(
                    "[bold cyan]🎟️ TICKET MANAGEMENT[/bold cyan]",
                    border_style="cyan",
                    box=box.DOUBLE
                )
            )

            table = Table(
                title="TICKET MENU",
                box=box.ROUNDED,
                border_style="cyan"
            )

            table.add_column(
                "Option",
                justify="center",
                style="bold yellow"
            )

            table.add_column(
                "Operation",
                style="bold white"
            )

            table.add_row(
                "1",
                "📋 View Active Tickets"
            )

            table.add_row(
                "2",
                "🔍 Search Ticket"
            )

            table.add_row(
                "3",
                "❌ Cancel Ticket"
            )

            table.add_row(
                "4",
                "📂 View Cancelled Tickets"
            )

            table.add_row(
                "5",
                "⬅️ Back"
            )

            console.print(table)

            choice = console.input(
                "\n[bold green]Enter Choice : [/bold green]"
            ).strip()

            if choice == "1":

                view_tickets()

            elif choice == "2":

                search_ticket()

            elif choice == "3":

                cancel_ticket()

            elif choice == "4":

                view_cancelled_tickets()

            elif choice == "5":

                break

            else:

                console.print(
                    Panel(
                        "[bold red]❌ Invalid Choice![/bold red]\n\n"
                        "[yellow]Please enter a number from 1 to 5.[/yellow]",
                        border_style="red"
                    )
                )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

        except KeyboardInterrupt:

            console.print(
                "\n[yellow]⚠️ Returning to previous menu...[/yellow]"
            )

            break

        except Exception as e:

            console.print(
                Panel(
                    f"[bold red]❌ Unexpected Error[/bold red]\n\n"
                    f"[yellow]{e}[/yellow]",
                    border_style="red"
                )
            )

            console.input(
                "\n[cyan]Press Enter to continue...[/cyan]"
            )