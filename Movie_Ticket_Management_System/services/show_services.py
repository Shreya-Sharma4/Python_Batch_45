from datetime import datetime, timedelta
import mysql.connector
from db import conn, cursor
from models.show import Show
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def add_show():
    console.print(Panel("[bold cyan]🎭 ADD SHOW[/bold cyan]", border_style="cyan", box=box.DOUBLE))
    try:
        movie_id = int(console.input("[bold green]Movie ID : [/bold green]"))
        theater_id = int(console.input("[bold green]Theater ID : [/bold green]"))
        show_date = console.input("[bold green]Show Date (YYYY-MM-DD) : [/bold green]").strip()
        show_time = console.input("[bold green]Show Time (HH:MM:SS) : [/bold green]").strip()
        new_start = datetime.strptime(show_date + " " + show_time, "%Y-%m-%d %H:%M:%S")

        cursor.execute("SELECT movie_name, duration FROM movies WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()
        if not movie:
            console.print(Panel("[bold red]❌ Movie ID not found.[/bold red]", border_style="red"))
            return

        movie_name = movie[0]
        duration = movie[1]

        cursor.execute("SELECT theater_name FROM theaters WHERE theater_id = %s", (theater_id,))
        theater = cursor.fetchone()
        if not theater:
            console.print(Panel("[bold red]❌ Theater ID not found.[/bold red]", border_style="red"))
            return

        new_end = new_start + timedelta(minutes=duration)

        cursor.execute("""
            SELECT s.show_id, s.show_time, m.movie_name, m.duration
            FROM shows s JOIN movies m ON s.movie_id = m.movie_id
            WHERE s.theater_id = %s AND s.show_date = %s
        """, (theater_id, show_date))

        existing_shows = cursor.fetchall()
        for show in existing_shows:
            existing_time = str(show[1]).split(".")[0]
            existing_start = datetime.strptime(show_date + " " + existing_time, "%Y-%m-%d %H:%M:%S")
            existing_end = existing_start + timedelta(minutes=show[3])
            
            if (new_start < existing_end and new_end > existing_start):
                console.print(Panel(f"[bold red]❌ SHOW TIMING CONFLICT![/bold red]\n\n[yellow]Existing Show ID : {show[0]}[/yellow]\n[yellow]Existing Movie : {show[2]}[/yellow]", border_style="red"))
                return

        cursor.execute("""
            INSERT INTO shows (movie_id, theater_id, show_date, show_time)
            VALUES (%s, %s, %s, %s)
        """, (movie_id, theater_id, show_date, show_time))
        conn.commit()
        console.print(Panel("[bold green]✅ Show added successfully.[/bold green]", border_style="green"))

    except ValueError:
        console.print(Panel("[bold red]❌ Invalid date/time format.[/bold red]", border_style="red"))
    except Exception as e:
        conn.rollback()
        console.print(Panel(f"[bold red]❌ Error[/bold red]\n\n[yellow]{e}[/yellow]", border_style="red"))

def view_shows():
    console.print(Panel("[bold cyan]📋 SHOW LIST[/bold cyan]", border_style="cyan", box=box.DOUBLE))
    try:
        cursor.execute("""
            SELECT s.show_id, m.movie_name, t.theater_name, s.show_date, s.show_time
            FROM shows s
            JOIN movies m ON s.movie_id = m.movie_id
            JOIN theaters t ON s.theater_id = t.theater_id
            ORDER BY s.show_date, s.show_time
        """)
        records = cursor.fetchall()

        if not records:
            console.print(Panel("[yellow]⚠️ No shows found.[/yellow]", border_style="yellow"))
            return

        table = Table(title="🎭 SHOWS", box=box.ROUNDED, border_style="cyan", show_lines=True)
        table.add_column("Show ID", justify="center")
        table.add_column("Movie")
        table.add_column("Theater")
        table.add_column("Date")
        table.add_column("Time")

        for row in records:
            table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
        console.print(table)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error[/bold red]\n\n{e}", border_style="red"))

def search_show():
    try:
        show_id = int(console.input("[bold green]Enter Show ID : [/bold green]"))
        cursor.execute("""
            SELECT s.show_id, m.movie_name, t.theater_name, s.show_date, s.show_time
            FROM shows s JOIN movies m ON s.movie_id = m.movie_id
            JOIN theaters t ON s.theater_id = t.theater_id WHERE s.show_id = %s
        """, (show_id,))
        row = cursor.fetchone()

        if not row:
            console.print(Panel("[bold red]❌ Show not found.[/bold red]", border_style="red"))
            return

        table = Table(title="🎭 SHOW DETAILS", box=box.ROUNDED, border_style="green")
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")
        table.add_row("Show ID", str(row[0]))
        table.add_row("Movie", str(row[1]))
        table.add_row("Theater", str(row[2]))
        table.add_row("Date", str(row[3]))
        table.add_row("Time", str(row[4]))
        console.print(table)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error[/bold red]\n\n{e}", border_style="red"))

def update_show():
    try:
        show_id = int(console.input("[bold green]Show ID : [/bold green]"))
        cursor.execute("SELECT show_id FROM shows WHERE show_id = %s", (show_id,))
        if not cursor.fetchone():
            console.print(Panel("[bold red]❌ Show not found.[/bold red]", border_style="red"))
            return

        movie_id = int(console.input("[bold green]New Movie ID : [/bold green]"))
        theater_id = int(console.input("[bold green]New Theater ID : [/bold green]"))
        show_date = console.input("[bold green]New Date (YYYY-MM-DD) : [/bold green]").strip()
        show_time = console.input("[bold green]New Time (HH:MM:SS) : [/bold green]").strip()

        cursor.execute("UPDATE shows SET movie_id = %s, theater_id = %s, show_date = %s, show_time = %s WHERE show_id = %s", 
                       (movie_id, theater_id, show_date, show_time, show_id))
        conn.commit()
        console.print(Panel("[bold green]✅ Show updated successfully.[/bold green]", border_style="green"))
    except Exception as e:
        conn.rollback()
        console.print(Panel(f"[bold red]❌ Error[/bold red]\n\n{e}", border_style="red"))

def delete_show():
    try:
        show_id = int(console.input("[bold green]Enter Show ID : [/bold green]"))
        cursor.execute("DELETE FROM shows WHERE show_id = %s", (show_id,))
        conn.commit()
        console.print(Panel("[bold green]✅ Show deleted successfully.[/bold green]", border_style="green"))
    except Exception as e:
        conn.rollback()
        console.print(Panel(f"[bold red]❌ Error[/bold red]\n\n{e}", border_style="red"))