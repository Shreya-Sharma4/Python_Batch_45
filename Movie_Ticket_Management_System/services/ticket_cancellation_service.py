import mysql.connector
from db import conn, cursor
from models.ticket_c import Ticket
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# --- AUTO-FIX FOR YOUR DATABASE SCHEMA ---
# This automatically adds the missing 'status' column to prevent the 1054 Error
try:
    cursor.execute("SHOW COLUMNS FROM bookings LIKE 'status'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE bookings ADD COLUMN status VARCHAR(20) DEFAULT 'Booked'")
        conn.commit()
except Exception:
    pass
# -----------------------------------------

def view_tickets():
    console.print(Panel("[bold cyan]🎟️ VIEW ACTIVE TICKETS[/bold cyan]", border_style="cyan", box=box.DOUBLE))
    try:
        query = """
        SELECT booking_id, user_id, show_id, seat_id, booking_date, total_amount, status
        FROM bookings
        WHERE status = 'Booked' OR status IS NULL
        ORDER BY booking_id
        """
        cursor.execute(query)
        tickets = cursor.fetchall()
        if not tickets:
            console.print(Panel("[yellow]⚠️ No active tickets found.[/yellow]", border_style="yellow"))
            return

        table = Table(title="🎟️ ACTIVE TICKETS", box=box.ROUNDED, border_style="cyan", show_lines=True)
        table.add_column("Booking ID", justify="center", style="bold yellow")
        table.add_column("User ID", justify="center")
        table.add_column("Show ID", justify="center")
        table.add_column("Seat ID", justify="center")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Status", justify="center", style="bold green")

        for row in tickets:
            table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), f"₹{row[5]}", str(row[6] or 'Booked'))
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def search_ticket():
    try:
        booking_id = int(console.input("[bold green]Enter Booking ID : [/bold green]"))
        cursor.execute("SELECT booking_id, user_id, show_id, seat_id, booking_date, total_amount, status FROM bookings WHERE booking_id = %s", (booking_id,))
        row = cursor.fetchone()
        
        if not row:
            console.print("[bold red]❌ Ticket not found.[/bold red]")
            return

        table = Table(title="🎟️ TICKET DETAILS", box=box.ROUNDED, border_style="green")
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")
        table.add_row("Booking ID", str(row[0]))
        table.add_row("User ID", str(row[1]))
        table.add_row("Show ID", str(row[2]))
        table.add_row("Seat ID", str(row[3]))
        table.add_row("Amount", f"₹{row[5]}")
        table.add_row("Status", str(row[6] or 'Booked'))
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def cancel_ticket():
    try:
        booking_id = int(console.input("[bold green]Enter Booking ID : [/bold green]"))
        cursor.execute("SELECT status FROM bookings WHERE booking_id = %s", (booking_id,))
        row = cursor.fetchone()
        
        if not row:
            console.print("[bold red]❌ Ticket not found.[/bold red]")
            return

        if str(row[0]).lower() == "cancelled":
            console.print("[bold yellow]⚠️ This ticket is already cancelled.[/bold yellow]")
            return

        confirm = console.input("\n[bold red]Are you sure you want to cancel this ticket? (Y/N) : [/bold red]").strip().lower()
        if confirm == "y":
            cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = %s", (booking_id,))
            conn.commit()
            console.print("[bold green]✅ Ticket cancelled successfully.[/bold green]")
        else:
            console.print("[yellow]❌ Cancellation cancelled.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def view_cancelled_tickets():
    try:
        cursor.execute("SELECT booking_id, user_id, show_id, seat_id, total_amount, status FROM bookings WHERE status = 'Cancelled'")
        tickets = cursor.fetchall()
        if not tickets:
            console.print("[yellow]⚠️ No cancelled tickets found.[/yellow]")
            return
            
        table = Table(title="❌ CANCELLED TICKETS", box=box.ROUNDED, border_style="red", show_lines=True)
        table.add_column("Booking ID", justify="center", style="bold yellow")
        table.add_column("Amount", justify="right")
        table.add_column("Status", justify="center", style="bold red")

        for row in tickets:
            table.add_row(str(row[0]), f"₹{row[4]}", str(row[5]))
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")