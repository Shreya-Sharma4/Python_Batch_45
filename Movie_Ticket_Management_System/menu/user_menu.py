from rich.console import Console

from services.user_services import (
    register_user,
    login_user,
    view_profile,
    update_profile,
    change_password,
    delete_account
)


console = Console()


# =========================================================
# USER DASHBOARD
# =========================================================

def user_dashboard(user_id):

    while True:

        try:

            console.print(
                "\n[bold cyan]========== USER DASHBOARD ==========[/bold cyan]"
            )

            console.print("1. View Profile")
            console.print("2. Update Profile")
            console.print("3. Change Password")
            console.print("4. Delete Account")
            console.print("5. Logout")

            choice = input("\nEnter your choice : ")

            if choice == "1":

                view_profile(user_id)

            elif choice == "2":

                update_profile(user_id)

            elif choice == "3":

                change_password(user_id)

            elif choice == "4":

                deleted = delete_account(user_id)

                if deleted:

                    break

            elif choice == "5":

                console.print(
                    "\n[green]Logged out successfully![/green]"
                )

                break

            else:

                console.print(
                    "\n[red]Invalid Choice! Try Again.[/red]"
                )

        except KeyboardInterrupt:

            console.print(
                "\n[red]Program Interrupted.[/red]"
            )

            break

        except Exception as e:

            console.print(
                f"\n[red]Error: {e}[/red]"
            )


# =========================================================
# USER MENU
# =========================================================

def menu():

    while True:

        try:

            console.print(
                "\n[bold cyan]========== USER MANAGEMENT SYSTEM ==========[/bold cyan]"
            )

            console.print("1. Register")
            console.print("2. Login")
            console.print("3. Exit")

            choice = input("\nEnter your choice : ")

            if choice == "1":

                register_user()

            elif choice == "2":

                user_id = login_user()

                if user_id is not None:

                    user_dashboard(user_id)

            elif choice == "3":

                console.print(
                    "\n[green]Thank you for using User Management System![/green]"
                )

                break

            else:

                console.print(
                    "\n[red]Invalid Choice! Try Again.[/red]"
                )

        except KeyboardInterrupt:

            console.print(
                "\n[red]Program Interrupted.[/red]"
            )

            break

        except Exception as e:

            console.print(
                f"\n[red]Error: {e}[/red]"
            )


if __name__ == "__main__":
    menu()