from db import conn
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def add_theater():
    console.print(Panel.fit("[bold cyan]ADD THEATER[/bold cyan]"))
    theater_name = console.input("[yellow]Enter Theater Name : [/yellow]").strip()
    location = console.input("[yellow]Enter Location : [/yellow]").strip()

    if theater_name == "" or location == "":
        console.print("[bold red]Theater Name and Location cannot be empty![/bold red]")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO theaters(theater_name, location) VALUES(%s, %s)", (theater_name, location))
        conn.commit()
        console.print("\n[bold green]✓ Theater Added Successfully![/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        cursor.close()

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
        for theater in theaters: table.add_row(str(theater[0]), theater[1], theater[2])
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        cursor.close()

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
        for theater in theaters: table.add_row(str(theater[0]), theater[1], theater[2])
        console.print(table)

        console.print("\n[bold cyan]Search Theater By:[/bold cyan]\n1. Theater Name\n2. Location")
        choice = console.input("[yellow]Enter your choice (1/2) : [/yellow]").strip()

        if choice == "1":
            theater_name = console.input("[yellow]Enter Theater Name : [/yellow]").strip()
            cursor.execute("SELECT * FROM theaters WHERE theater_name=%s", (theater_name,))
        elif choice == "2":
            location = console.input("[yellow]Enter Location : [/yellow]").strip()
            cursor.execute("SELECT * FROM theaters WHERE location=%s", (location,))
        else:
            return

        theaters = cursor.fetchall()
        if theaters:
            result = Table(title="SEARCH RESULTS", show_lines=True)
            result.add_column("Theater ID", style="cyan")
            result.add_column("Theater Name", style="green")
            result.add_column("Location", style="magenta")
            for theater in theaters: result.add_row(str(theater[0]), theater[1], theater[2])
            console.print(result)
        else:
            console.print("\n[bold red]Theater Not Found![/bold red]\n")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        cursor.close()

def update_theater():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM theaters")
        theaters = cursor.fetchall()
        if not theaters: return
        theater_id = console.input("\n[yellow]Enter Theater ID to Update : [/yellow]").strip()
        
        cursor.execute("SELECT * FROM theaters WHERE theater_id=%s", (theater_id,))
        if not cursor.fetchone():
            console.print("\n[bold red]Theater Not Found![/bold red]\n")
            return

        new_name = console.input("\n[yellow]Enter New Theater Name : [/yellow]").strip()
        new_location = console.input("[yellow]Enter New Location : [/yellow]").strip()

        cursor.execute("UPDATE theaters SET theater_name=%s, location=%s WHERE theater_id=%s", (new_name, new_location, theater_id))
        conn.commit()
        console.print("\n[bold green]✓ Theater Updated Successfully![/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        cursor.close()

def delete_theater():
    cursor = conn.cursor()
    try:
        theater_id = console.input("\n[yellow]Enter Theater ID to Delete : [/yellow]").strip()
        cursor.execute("SELECT * FROM theaters WHERE theater_id=%s", (theater_id,))
        if not cursor.fetchone():
            console.print("\n[bold red]Theater Not Found![/bold red]\n")
            return

        choice = console.input("[yellow]Delete this theater? (Y/N): [/yellow]").strip().lower()
        if choice == "y":
            cursor.execute("DELETE FROM theaters WHERE theater_id=%s", (theater_id,))
            conn.commit()
            console.print("\n[bold green]✓ Theater Deleted Successfully![/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        cursor.close()