from rich.console import Console
from rich.panel import Panel

from services.theater_services import TheaterService

console = Console()

theater_service = TheaterService()


def theater_menu():

    while True:

        console.print(
            Panel.fit(
                "[bold cyan]THEATER MANAGEMENT[/bold cyan]",
                border_style="blue"
            )
        )

        console.print("[bold yellow]1.[/bold yellow] Add Theater")
        console.print("[bold yellow]2.[/bold yellow] View Theaters")
        console.print("[bold yellow]3.[/bold yellow] Search Theater")
        console.print("[bold yellow]4.[/bold yellow] Update Theater")
        console.print("[bold yellow]5.[/bold yellow] Delete Theater")
        console.print("[bold yellow]6.[/bold yellow] Back")

        choice = console.input("\n[bold green]Enter your choice : [/bold green]")

        if choice == "1":
            theater_service.add_theater()

        elif choice == "2":
            theater_service.view_theaters()

        elif choice == "3":
            theater_service.search_theater()

        elif choice == "4":
            theater_service.update_theater()

        elif choice == "5":
            theater_service.delete_theater()

        elif choice == "6":
            console.print("\n[bold cyan]Returning to Admin Menu...[/bold cyan]\n")
            break

        else:
            console.print("\n[bold red]Invalid Choice! Please Try Again.[/bold red]\n")