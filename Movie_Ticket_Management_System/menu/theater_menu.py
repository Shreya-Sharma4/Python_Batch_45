# from rich.console import Console
# from rich.panel import Panel

# from services.theater_services import (
#     add_theater,
#     view_theaters,
#     search_theater,
#     update_theater,
#     delete_theater
# )

# console = Console()


# def theater_menu():

#     while True:

#         console.print(
#             Panel.fit(
#                 "[bold cyan]THEATER MANAGEMENT[/bold cyan]",
#                 border_style="blue"
#             )
#         )

#         console.print("[bold yellow]1.[/bold yellow] Add Theater")
#         console.print("[bold yellow]2.[/bold yellow] View Theaters")
#         console.print("[bold yellow]3.[/bold yellow] Search Theater")
#         console.print("[bold yellow]4.[/bold yellow] Update Theater")
#         console.print("[bold yellow]5.[/bold yellow] Delete Theater")
#         console.print("[bold yellow]6.[/bold yellow] Back")

#         choice = console.input("\n[bold green]Enter your choice : [/bold green]")

#         if choice == "1":
#             add_theater()

#         elif choice == "2":
#             view_theaters()

#         elif choice == "3":
#             search_theater()

#         elif choice == "4":
#             update_theater()

#         elif choice == "5":
#             delete_theater()

#         elif choice == "6":
#             console.print("\n[bold cyan]Returning to Main Menu...[/bold cyan]\n")
#             break

#         else:
#             console.print("\n[bold red]Invalid Choice! Please Try Again.[/bold red]\n")

from rich.console import Console
from rich.panel import Panel

from services.theater_services import (
    add_theater,
    view_theaters,
    search_theater,
    update_theater,
    delete_theater,
)

console = Console()


def theater_menu():

    while True:

        console.print(
            Panel.fit(
                "[bold cyan]THEATER MANAGEMENT[/bold cyan]",
                border_style="green"
            )
        )

        console.print("[bold yellow]1.[/bold yellow] Add Theater")
        console.print("[bold yellow]2.[/bold yellow] View Theaters")
        console.print("[bold yellow]3.[/bold yellow] Search Theater")
        console.print("[bold yellow]4.[/bold yellow] Update Theater")
        console.print("[bold yellow]5.[/bold yellow] Delete Theater")
        console.print("[bold yellow]6.[/bold yellow] Back")

        try:
            choice = int(
                console.input(
                    "\n[bold green]Enter your choice : [/bold green]"
                )
            )
        except ValueError:
            console.print(
                "\n[bold red]Invalid Input! Please Enter a Number.[/bold red]\n"
            )
            continue

        if choice == 1:
            add_theater()

        elif choice == 2:
            view_theaters()

        elif choice == 3:
            search_theater()

        elif choice == 4:
            update_theater()

        elif choice == 5:
            delete_theater()

        elif choice == 6:
            break

        else:
            console.print(
                "\n[bold red]Invalid Choice! Please Try Again.[/bold red]\n"
            )


def main_menu():

    while True:

        console.print(
            Panel.fit(
                # "[bold blue]MOVIE TICKET BOOKING SYSTEM[/bold blue]\n"
                "[bold cyan]THEATER MANAGEMENT[/bold cyan]",
                border_style="green"
            )
        )

        console.print("[bold yellow]1.[/bold yellow] Theater Management")
        console.print("[bold yellow]2.[/bold yellow] Exit")

        try:
            choice = int(
                console.input(
                    "\n[bold green]Enter your choice : [/bold green]"
                )
            )
        except ValueError:
            console.print(
                "\n[bold red]Invalid Input! Please Enter a Number.[/bold red]\n"
            )
            continue

        if choice == 1:
            theater_menu()

        elif choice == 2:
            console.print(
                "\n[bold red]Thank You! Exiting Program...[/bold red]"
            )
            break

        else:
            console.print(
                "\n[bold red]Invalid Choice! Please Try Again.[/bold red]\n"
            )