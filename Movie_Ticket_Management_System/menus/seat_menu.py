from rich.console import Console
from services.seat_services import add_seat, view_seats, check_seat_availability, update_seat, delete_seat

console = Console()

def seat_menu():
    while True:
        try:
            console.print("\n[bold cyan]===== Seat Management System =====[/bold cyan]")
            console.print("1. Add Seats")
            console.print("2. View Seat Layout")
            console.print("3. Check Seat Availability")
            console.print("4. Update Seat Type")
            console.print("5. Delete Seat")
            console.print("6. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1": add_seat()
            elif choice == "2": view_seats()
            elif choice == "3": check_seat_availability()
            elif choice == "4": update_seat()
            elif choice == "5": delete_seat()
            elif choice == "6":
                console.print("\n[green]Thank you for using Seat Management System[/green]")
                break
            else:
                console.print("[red]Invalid Choice! Try Again.[/red]")
        except KeyboardInterrupt:
            console.print("\n[red]Program Interrupted.[/red]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")