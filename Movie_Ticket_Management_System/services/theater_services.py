from db import conn
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ADD THEATER

def add_theater():

    console.print(Panel.fit("[bold cyan]ADD THEATER[/bold cyan]"))

    theater_name = console.input("[yellow]Enter Theater Name : [/yellow]").strip()
    location = console.input("[yellow]Enter Location : [/yellow]").strip()

    if theater_name == "" or location == "":
        console.print("[bold red]Theater Name and Location cannot be empty![/bold red]")
        return

    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO theaters(theater_name, location)
        VALUES(%s, %s)
        """
        cursor.execute(query, (theater_name, location))
        conn.commit()

        console.print("\n[bold green]✓ Theater Added Successfully![/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

    finally:
        cursor.close()


# VIEW THEATERS

def view_theaters():

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM theaters")
        theaters = cursor.fetchall()

        if not theaters:
            console.print("\n[bold red]No Theater Found.[/bold red]\n")
            return

        table = Table(title="THEATER DETAILS", show_lines=True)

        table.add_column("Theater ID", style="cyan", justify="center")
        table.add_column("Theater Name", style="green")
        table.add_column("Location", style="magenta")

        for theater in theaters:
            table.add_row(str(theater[0]), theater[1], theater[2])

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

    finally:
        cursor.close()


# SEARCH THEATER

def search_theater():

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM theaters")
        theaters = cursor.fetchall()

        if not theaters:
            console.print("\n[bold red]No Theaters Available.[/bold red]\n")
            return

        table = Table(title="AVAILABLE THEATERS")
        table.add_column("Theater ID", style="cyan")
        table.add_column("Theater Name", style="green")
        table.add_column("Location", style="magenta")

        for theater in theaters:
            table.add_row(
                str(theater[0]),
                theater[1],
                theater[2]
            )

        console.print(table)

        console.print("\n[bold cyan]Search Theater By:[/bold cyan]")
        console.print("1. Theater Name")
        console.print("2. Location")

        choice = console.input(
            "[yellow]Enter your choice (1/2) : [/yellow]"
        ).strip()

        if choice == "1":

            theater_name = console.input(
                "[yellow]Enter Theater Name : [/yellow]"
            ).strip()

            if theater_name == "":
                console.print(
                    "[bold red]Theater Name cannot be empty![/bold red]"
                )
                return

            cursor.execute("""
                SELECT * FROM theaters
                WHERE theater_name=%s
            """, (theater_name,))

        elif choice == "2":

            location = console.input(
                "[yellow]Enter Location : [/yellow]"
            ).strip()

            if location == "":
                console.print(
                    "[bold red]Location cannot be empty![/bold red]"
                )
                return

            cursor.execute("""
                SELECT * FROM theaters
                WHERE location=%s
            """, (location,))

        else:
            console.print(
                "[bold red]Invalid Choice! Enter 1 or 2 only.[/bold red]"
            )
            return

        theaters = cursor.fetchall()

        if theaters:

            result = Table(title="SEARCH RESULTS", show_lines=True)

            result.add_column("Theater ID", style="cyan")
            result.add_column("Theater Name", style="green")
            result.add_column("Location", style="magenta")

            for theater in theaters:
                result.add_row(
                    str(theater[0]),
                    theater[1],
                    theater[2]
                )

            console.print(result)

        else:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

    finally:
        cursor.close()


# UPDATE THEATER

def update_theater():

    cursor = conn.cursor()

    try:
        # Display all theaters with ID
        cursor.execute("SELECT * FROM theaters")
        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theaters Available.[/bold red]\n"
            )
            return

        table = Table(
            title="AVAILABLE THEATERS",
            show_lines=True
        )

        table.add_column("Theater ID", style="cyan")
        table.add_column("Theater Name", style="green")
        table.add_column("Location", style="magenta")

        for theater in theaters:
            table.add_row(
                str(theater[0]),
                theater[1],
                theater[2]
            )

        console.print(table)

        # Ask for Theater ID
        theater_id = console.input(
            "\n[yellow]Enter Theater ID to Update : [/yellow]"
        ).strip()

        if theater_id == "":
            console.print(
                "[bold red]Theater ID cannot be empty![/bold red]"
            )
            return

        # Find theater using ID
        cursor.execute("""
            SELECT * FROM theaters
            WHERE theater_id=%s
        """, (theater_id,))

        theater = cursor.fetchone()

        if theater is None:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )
            return

        # Show current details
        current = Table(
            title="CURRENT THEATER DETAILS",
            show_lines=True
        )

        current.add_column("Field", style="cyan")
        current.add_column("Value", style="green")

        current.add_row("Theater ID", str(theater[0]))
        current.add_row("Theater Name", theater[1])
        current.add_row("Location", theater[2])

        console.print(current)

        # Ask for new details
        new_name = console.input(
            "\n[yellow]Enter New Theater Name : [/yellow]"
        ).strip()

        new_location = console.input(
            "[yellow]Enter New Location : [/yellow]"
        ).strip()

        if new_name == "" or new_location == "":
            console.print(
                "[bold red]Theater Name and Location cannot be empty![/bold red]"
            )
            return

        # Update using Theater ID
        cursor.execute("""
            UPDATE theaters
            SET theater_name=%s, location=%s
            WHERE theater_id=%s
        """, (new_name, new_location, theater_id))

        conn.commit()

        console.print(
            "\n[bold green]✓ Theater Updated Successfully![/bold green]\n"
        )

    except Exception as e:
        console.print(
            f"[bold red]Error:[/bold red] {e}"
        )

    finally:
        cursor.close()


# DELETE THEATER

def delete_theater():

    cursor = conn.cursor()

    try:
        # Display all theaters with ID
        cursor.execute("SELECT * FROM theaters")
        theaters = cursor.fetchall()

        if not theaters:
            console.print(
                "\n[bold red]No Theaters Available.[/bold red]\n"
            )
            return

        table = Table(
            title="AVAILABLE THEATERS",
            show_lines=True
        )

        table.add_column("Theater ID", style="cyan")
        table.add_column("Theater Name", style="green")
        table.add_column("Location", style="magenta")

        for theater in theaters:
            table.add_row(
                str(theater[0]),
                theater[1],
                theater[2]
            )

        console.print(table)

        # Ask for Theater ID
        theater_id = console.input(
            "\n[yellow]Enter Theater ID to Delete : [/yellow]"
        ).strip()

        if theater_id == "":
            console.print(
                "[bold red]Theater ID cannot be empty![/bold red]"
            )
            return

        # Find theater using ID
        cursor.execute("""
            SELECT * FROM theaters
            WHERE theater_id=%s
        """, (theater_id,))

        theater = cursor.fetchone()

        if theater is None:
            console.print(
                "\n[bold red]Theater Not Found![/bold red]\n"
            )
            return

        # Show theater before deletion
        selected = Table(
            title="THEATER TO DELETE",
            show_lines=True
        )

        selected.add_column("Field", style="cyan")
        selected.add_column("Value", style="green")

        selected.add_row("Theater ID", str(theater[0]))
        selected.add_row("Theater Name", theater[1])
        selected.add_row("Location", theater[2])

        console.print(selected)

        choice = console.input(
            "[yellow]Delete this theater? (Y/N): [/yellow]"
        ).strip().lower()

        if choice not in ["y", "n"]:
            console.print(
                "[bold red]Invalid Choice! Enter Y or N only.[/bold red]"
            )
            return

        if choice == "y":

            cursor.execute("""
                DELETE FROM theaters
                WHERE theater_id=%s
            """, (theater_id,))

            conn.commit()

            console.print(
                "\n[bold green]✓ Theater Deleted Successfully![/bold green]\n"
            )

        else:
            console.print(
                "\n[bold cyan]Delete Cancelled.[/bold cyan]\n"
            )

    except Exception as e:
        console.print(
            f"[bold red]Error:[/bold red] {e}"
        )

    finally:
        cursor.close()
