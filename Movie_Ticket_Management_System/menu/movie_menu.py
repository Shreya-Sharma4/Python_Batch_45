

from rich.console import Console

from sevices.movie_management import (
    add_movie,
    view_movies,
    search_movie,
    update_movie,
    delete_movie
)

console = Console()


def menu():
    while True:
        try:
            console.print("\n[bold cyan]Movie Management System[/bold cyan]")
            console.print("1. Add Movie")
            console.print("2. View Movies")
            console.print("3. Search Movie")
            console.print("4. Update Movie")
            console.print("5. Delete Movie")
            console.print("6. Exit")

            choice = input("\nEnter your choice : ")

            if choice == "1":
                add_movie()

            elif choice == "2":
                view_movies()

            elif choice == "3":
                search_movie()

            elif choice == "4":
                update_movie()

            elif choice == "5":
                delete_movie()

            elif choice == "6":
                console.print("[green]Thank you for using Movie Management System[/green]")
                break

            else:
                console.print("[red]Invalid Choice! Try Again.[/red]")

        except KeyboardInterrupt:
            console.print("\n[red]Program Interrupted.[/red]")
            break

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    menu()