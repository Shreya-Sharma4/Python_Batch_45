import mysql.connector
from rich.console import Console

console = Console()

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ranjeet@8311",
        database="movie_ticket_booking"
    )

    cursor = conn.cursor()

    console.print("[green]Database Connected Successfully[/green]")

except mysql.connector.Error as e:
    console.print(f"[red]Database Connection Error : {e}[/red]")