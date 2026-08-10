from rich.console import Console
from rich.panel import Panel
from menus.movie_menu import menu as movie_menu
from menus.theater_menu import theater_menu
from menus.show_menu import show_menu
from menus.seat_menu import seat_menu
from menus.ticket_cancellation_menu import ticket_menu
from menus.payment_menu import payment_menu
from menus.ticket_booking_menu import ticket_booking_menu

console = Console()

def admin_menu():
    while True:
        try:
            console.print(Panel.fit("[bold cyan]👨‍💼 ADMIN DASHBOARD[/bold cyan]", border_style="cyan"))
            console.print("1. Movie Management")
            console.print("2. Theater Management")
            console.print("3. Show Management")
            console.print("4. Seat Management")
            console.print("5. Ticket Management")
            console.print("6. Payment Management")
            console.print("7. Ticket Booking (On behalf of User)")
            console.print("8. Logout")

            choice = input("\nEnter your choice : ").strip()

            if choice == "1":
                movie_menu()
            elif choice == "2":
                theater_menu()
            elif choice == "3":
                show_menu()
            elif choice == "4":
                seat_menu()
            elif choice == "5":
                ticket_menu()
            elif choice == "6":
                payment_menu()
            elif choice == "7":
                # Admin needs to provide the User ID they are booking for
                user_id_str = input("Enter the User ID to book a ticket for : ").strip()
                if user_id_str.isdigit():
                    ticket_booking_menu(int(user_id_str))
                else:
                    console.print("[red]Invalid User ID! It must be a valid number.[/red]")
            elif choice == "8":
                console.print("\n[green]Logged out successfully![/green]")
                break
            else:
                console.print("[red]Invalid Choice! Try Again.[/red]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")