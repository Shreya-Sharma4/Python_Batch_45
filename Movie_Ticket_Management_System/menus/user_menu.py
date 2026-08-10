from rich.console import Console
from db import cursor
from login.user_login import user_login
from services.user_services import register_user, view_profile, update_profile, update_user_credentials
from menus.ticket_booking_menu import ticket_booking_menu
from menus.payment_menu import payment_menu
from menus.ticket_generation_menu import ticket_generation_menu
from menus.ticket_cancellation_menu import ticket_menu

console = Console()

def user_dashboard(user_id):
    while True:
        try:
            console.print("\n[bold cyan]========== USER DASHBOARD ==========[/bold cyan]")
            console.print("1. View Profile")
            console.print("2. Update Profile")
            console.print("3. Change Password / Update Credentials")
            console.print("4. Ticket Booking")
            console.print("5. Make Payment")
            console.print("6. Ticket Generation")
            console.print("7. Ticket Cancellation")
            console.print("8. Logout")

            choice = input("\nEnter your choice : ")

            if choice == "1": 
                view_profile(user_id)
            elif choice == "2": 
                update_profile(user_id)
            elif choice == "3": 
                # Fetch email dynamically to use the existing update_user_credentials function
                cursor.execute("SELECT email FROM users WHERE user_id = %s", (user_id,))
                row = cursor.fetchone()
                if row:
                    update_user_credentials(row[0])
            elif choice == "4": 
                ticket_booking_menu(user_id)
            elif choice == "5": 
                payment_menu()
            elif choice == "6": 
                ticket_generation_menu()
            elif choice == "7": 
                ticket_menu()
            elif choice == "8":
                console.print("\n[green]Logged out successfully![/green]")
                break
            else:
                console.print("\n[red]Invalid Choice! Try Again.[/red]")
        except KeyboardInterrupt:
            console.print("\n[red]Program Interrupted.[/red]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")

def menu():
    while True:
        try:
            console.print("\n[bold cyan]========== USER MANAGEMENT SYSTEM ==========[/bold cyan]")
            console.print("1. Register")
            console.print("2. Login")
            console.print("3. Exit")

            choice = input("\nEnter your choice : ")

            if choice == "1":
                register_user()
            elif choice == "2":
                # Calls your user_login module instead of the old function
                user_id = user_login()
                if user_id is not None:
                    user_dashboard(user_id)
            elif choice == "3":
                console.print("\n[green]Thank you for using User Management System![/green]")
                break
            else:
                console.print("\n[red]Invalid Choice! Try Again.[/red]")
        except KeyboardInterrupt:
            console.print("\n[red]Program Interrupted.[/red]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")