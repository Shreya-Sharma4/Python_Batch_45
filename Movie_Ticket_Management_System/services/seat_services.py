import mysql.connector
from db import conn, cursor
from rich.console import Console
from rich.table import Table

console = Console()

def add_seat():
    try:
        console.print("\n[bold cyan]===== Add Seat =====[/bold cyan]")
        theater_id = int(input("Enter Theater ID : ").strip())
        
        cursor.execute("SELECT theater_id, theater_name, location FROM theaters WHERE theater_id = %s", (theater_id,))
        theater = cursor.fetchone()

        if not theater:
            console.print("[red]Theater not found![/red]")
            return

        console.print(f"\n[green]Theater : {theater[1]}[/green]")
        console.print(f"[green]Location: {theater[2]}[/green]")

        seat_number = input("Seat Number : ").strip().upper()
        if not seat_number or len(seat_number) > 5:
            console.print("[red]Invalid seat number![/red]")
            return

        seat_type = input("Seat Type (Premium/Gold/Silver) : ").strip().title()
        if not seat_type or len(seat_type) > 20:
            console.print("[red]Invalid seat type![/red]")
            return

        seat_price = float(input("Seat Price : ").strip())
        if seat_price < 0:
            console.print("[red]Seat price cannot be negative![/red]")
            return

        cursor.execute("SELECT seat_id FROM seats WHERE theater_id = %s AND seat_number = %s", (theater_id, seat_number))
        if cursor.fetchone():
            console.print("[red]This seat already exists in this theater![/red]")
            return

        cursor.execute("""
            INSERT INTO seats (theater_id, seat_number, seat_type, seat_price)
            VALUES (%s, %s, %s, %s)
        """, (theater_id, seat_number, seat_type, seat_price))
        conn.commit()
        console.print("\n[green]Seat Added Successfully![/green]")
    except ValueError:
        console.print("[red]Please enter valid numeric values.[/red]")
    except mysql.connector.Error as e:
        console.print(f"[red]Database Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def view_seats():
    try:
        console.print("\n[bold cyan]===== View Seat Layout =====[/bold cyan]")
        show_id = int(input("Enter Show ID : ").strip())
        theater_id = int(input("Enter Theater ID : ").strip())

        cursor.execute("SELECT theater_id, theater_name, location FROM theaters WHERE theater_id = %s", (theater_id,))
        theater = cursor.fetchone()
        if not theater:
            console.print("[red]Theater not found![/red]")
            return

        console.print(f"\n[bold yellow]{theater[1]}[/bold yellow] - [dim]{theater[2]}[/dim]")
        
        cursor.execute("""
            SELECT s.seat_id, s.seat_number, s.seat_type, s.seat_price,
                   CASE WHEN b.seat_id IS NULL THEN 'Available' ELSE 'Booked' END AS status
            FROM seats s
            LEFT JOIN bookings b ON s.seat_id = b.seat_id AND b.show_id = %s
            WHERE s.theater_id = %s ORDER BY s.seat_id
        """, (show_id, theater_id))
        
        seats = cursor.fetchall()
        if not seats:
            console.print("\n[yellow]No seats found for this theater.[/yellow]")
            return

        console.print("\n[bold white]                 SCREEN[/bold white]")
        console.print("[dim]------------------------------------------------[/dim]")
        
        for i in range(0, len(seats), 5):
            row = seats[i:i + 5]
            for seat in row:
                if seat[4] == "Available":
                    console.print(f"[black on green]  {seat[1]:^5}  [/black on green]", end=" ")
                else:
                    console.print(f"[white on red]  {seat[1]:^5}  [/white on red]", end=" ")
            console.print()

        console.print("\n[green]■ Available[/green]    [red]■ Booked[/red]")

        table = Table(title="Seat Details")
        table.add_column("Seat ID", justify="center")
        table.add_column("Seat", justify="center")
        table.add_column("Type", justify="center")
        table.add_column("Price", justify="center")
        table.add_column("Status", justify="center")

        for seat in seats:
            status_text = "[green]Available[/green]" if seat[4] == "Available" else "[red]Booked[/red]"
            table.add_row(str(seat[0]), seat[1], seat[2], f"₹{seat[3]:.2f}", status_text)
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def check_seat_availability():
    try:
        show_id = int(input("Enter Show ID : ").strip())
        theater_id = int(input("Enter Theater ID : ").strip())
        seat_number = input("Enter Seat Number : ").strip().upper()

        cursor.execute("""
            SELECT s.seat_id, s.seat_number, s.seat_type, s.seat_price,
                   CASE WHEN b.seat_id IS NULL THEN 'Available' ELSE 'Booked' END AS status
            FROM seats s
            LEFT JOIN bookings b ON s.seat_id = b.seat_id AND b.show_id = %s
            WHERE s.theater_id = %s AND s.seat_number = %s
        """, (show_id, theater_id, seat_number))
        
        seat = cursor.fetchone()
        if not seat:
            console.print("\n[red]Seat Not Found![/red]")
            return

        console.print(f"Seat: {seat[1]} | Type: {seat[2]} | Price: ₹{seat[3]:.2f}")
        console.print("Status: [green]AVAILABLE[/green]" if seat[4] == "Available" else "Status: [red]BOOKED[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def update_seat():
    try:
        seat_id = int(input("Seat ID : ").strip())
        cursor.execute("SELECT seat_id FROM seats WHERE seat_id = %s", (seat_id,))
        if not cursor.fetchone():
            console.print("[red]Seat Not Found![/red]")
            return

        new_seat_type = input("\nNew Seat Type : ").strip().title()
        if not new_seat_type: return

        cursor.execute("UPDATE seats SET seat_type = %s WHERE seat_id = %s", (new_seat_type, seat_id))
        conn.commit()
        console.print("\n[green]Seat Type Updated Successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def delete_seat():
    try:
        seat_id = int(input("Seat ID : ").strip())
        cursor.execute("DELETE FROM seats WHERE seat_id = %s", (seat_id,))
        conn.commit()
        console.print("\n[green]Seat Deleted Successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")