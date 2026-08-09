from menus.movie_menu import movie_menu
from menus.show_menu import show_menu
from menus.ticket_menu import ticket_menu



def main_menu():

    while True:

        print("""
=======================================
            MAIN MENU
=======================================

1. Movie Management
2. Show Management
3. Ticket Management
4. Exit

=======================================
""")

        choice = input("Enter Choice : ")

        if choice == "1":
            movie_menu()

        elif choice == "2":
            show_menu()

        elif choice == "3":
            ticket_menu()

        elif choice == "4":
            print("Thank you!")
            break

        else:
            print("Invalid Choice!")


