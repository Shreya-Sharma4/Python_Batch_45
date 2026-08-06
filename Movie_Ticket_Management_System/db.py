import mysql.connector
from rich.console import Console


console = Console()


def get_connection():

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="movie_ticket_booking"
        )

        return connection

    except mysql.connector.Error as err:
        console.print(f"[bold red]Database Connection Error:[/bold red] {err}")
        return None