from db import get_connection
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TheaterService:

    # Add Theater
    def add_theater(self):

        console.print(Panel.fit("[bold cyan]ADD THEATER[/bold cyan]"))

        theater_name = console.input(
            "[yellow]Enter Theater Name : [/yellow]"
        ).strip()

        location = console.input(
            "[yellow]Enter Location : [/yellow]"
        ).strip()

        if theater_name == "" or location == "":
            console.print(
                "[bold red]Theater Name and Location cannot be empty![/bold red]"
            )
            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        query = """
        INSERT INTO theaters(theater_name, location)
        VALUES(%s, %s)
        """

        cursor.execute(query, (theater_name, location))
        conn.commit()

        console.print(
            "\n[bold green]✓ Theater Added Successfully![/bold green]\n"
        )

        cursor.close()
        conn.close()

    # View Theaters
    def view_theaters(self):

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM theaters")

        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theater Found.[/bold red]\n"
            )

        else:

            table = Table(
                title="THEATER DETAILS",
                show_lines=True
            )

            table.add_column(
                "Theater ID",
                style="cyan",
                justify="center"
            )

            table.add_column(
                "Theater Name",
                style="green"
            )

            table.add_column(
                "Location",
                style="magenta"
            )

            for theater in theaters:

                table.add_row(
                    str(theater[0]),
                    theater[1],
                    theater[2]
                )

            console.print(table)

        cursor.close()
        conn.close()

    # Search Theater
    def search_theater(self):

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute(
            "SELECT theater_name, location FROM theaters"
        )

        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theaters Available.[/bold red]\n"
            )
            cursor.close()
            conn.close()
            return

        table = Table(title="AVAILABLE THEATERS")

        table.add_column(
            "Theater Name",
            style="cyan"
        )

        table.add_column(
            "Location",
            style="green"
        )

        for theater in theaters:
            table.add_row(
                theater[0],
                theater[1]
            )

        console.print(table)

        theater_name = console.input(
            "\n[yellow]Enter Theater Name : [/yellow]"
        ).strip()

        location = console.input(
            "[yellow]Enter City/Location : [/yellow]"
        ).strip()

        cursor.execute(
            """
            SELECT *
            FROM theaters
            WHERE theater_name=%s
            AND location=%s
            """,
            (theater_name, location)
        )

        theater = cursor.fetchone()

        if theater:

            result = Table(title="THEATER FOUND")

            result.add_column(
                "Field",
                style="cyan"
            )

            result.add_column(
                "Value",
                style="green"
            )

            result.add_row(
                "Theater ID",
                str(theater[0])
            )

            result.add_row(
                "Theater Name",
                theater[1]
            )

            result.add_row(
                "Location",
                theater[2]
            )

            console.print(result)

        else:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )

        cursor.close()
        conn.close()

    # Update Theater
    def update_theater(self):

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute(
            "SELECT theater_name, location FROM theaters"
        )

        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theaters Available.[/bold red]\n"
            )
            return

        table = Table(title="AVAILABLE THEATERS")

        table.add_column("Theater Name", style="cyan")
        table.add_column("Location", style="green")

        for theater in theaters:
            table.add_row(
                theater[0],
                theater[1]
            )

        console.print(table)

        theater_name = console.input(
            "\n[yellow]Enter Theater Name to Update : [/yellow]"
        ).strip()

        location = console.input(
            "[yellow]Enter City/Location : [/yellow]"
        ).strip()

        cursor.execute(
            """
            SELECT *
            FROM theaters
            WHERE theater_name=%s
            AND location=%s
            """,
            (theater_name, location)
        )

        theater = cursor.fetchone()

        if theater is None:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )
            return

        new_name = console.input(
            "[yellow]Enter New Theater Name : [/yellow]"
        ).strip()

        new_location = console.input(
            "[yellow]Enter New Location : [/yellow]"
        ).strip()

        cursor.execute(
            """
            UPDATE theaters
            SET theater_name=%s,
                location=%s
            WHERE theater_name=%s
            AND location=%s
            """,
            (
                new_name,
                new_location,
                theater_name,
                location
            )
        )

        conn.commit()

        console.print(
            "\n[bold green]✓ Theater Updated Successfully![/bold green]\n"
        )

        cursor.close()
        conn.close()

    # Delete Theater
    def delete_theater(self):

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute(
            "SELECT theater_name, location FROM theaters"
        )

        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theaters Available.[/bold red]\n"
            )
            return

        table = Table(title="AVAILABLE THEATERS")

        table.add_column("Theater Name", style="cyan")
        table.add_column("Location", style="green")

        for theater in theaters:
            table.add_row(
                theater[0],
                theater[1]
            )

        console.print(table)

        theater_name = console.input(
            "\n[yellow]Enter Theater Name to Delete : [/yellow]"
        ).strip()

        location = console.input(
            "[yellow]Enter City/Location : [/yellow]"
        ).strip()

        cursor.execute(
            """
            SELECT *
            FROM theaters
            WHERE theater_name=%s
            AND location=%s
            """,
            (theater_name, location)
        )

        theater = cursor.fetchone()

        if theater is None:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )
            return

        choice = console.input(
            "[yellow]Delete this theater? (Y/N): [/yellow]"
        )

        if choice.lower() == "y":

            cursor.execute(
                """
                DELETE FROM theaters
                WHERE theater_name=%s
                AND location=%s
                """,
                (theater_name, location)
            )

            conn.commit()

            console.print(
                "\n[bold green]✓ Theater Deleted Successfully![/bold green]\n"
            )

        else:
            console.print(
                "\n[bold cyan]Delete Cancelled.[/bold cyan]\n"
            )

        cursor.close()
        conn.close()