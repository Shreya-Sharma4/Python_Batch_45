from rich.console import Console
from rich.panel import Panel

from menu.theater_menu import theater_menu

console = Console()


def main():

    while True:

        console.print(
            Panel.fit(
                "[bold blue]MOVIE TICKET BOOKING SYSTEM[/bold blue]\n"
                "[bold cyan]THEATER MANAGEMENT MODULE[/bold cyan]",
                border_style="green"
            )
        )

        console.print("[bold yellow]1.[/bold yellow] Theater Management")
        console.print("[bold yellow]2.[/bold yellow] Exit")

        # ✅ FIXED INPUT + INDENTATION
        try:
            choice = int(console.input("\n[bold green]Enter your choice : [/bold green]"))
        except ValueError:
            console.print("[bold red]Invalid input! Please enter a number[/bold red]")
            continue

        # ✅ FIXED COMPARISON (int, not string)
        if choice == 1:
            theater_menu()

        elif choice == 2:
            console.print("\n[bold red]Thank You! Exiting Program...[/bold red]")
            break

        else:
            console.print("\n[bold red]Invalid Choice! Please Try Again.[/bold red]\n")


if __name__ == "__main__":
    main()