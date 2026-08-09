
from services.ticket_cancellation import (
    view_tickets,
    search_ticket,
    cancel_ticket,
    view_cancelled_tickets
)


def ticket_menu():

    while True:

        print("""
========================================
             TICKET MANAGEMENT
========================================

1. View Tickets
2. Search Ticket
3. Cancel Ticket
4. View Cancelled Tickets
5. Back

========================================
""")

        choice = input("Enter Choice : ")

        if choice == "1":

            view_tickets()

        elif choice == "2":

            search_ticket()

        elif choice == "3":

            cancel_ticket()

        elif choice == "4":

            view_cancelled_tickets()

        elif choice == "5":

            break

        else:

            print("\n❌ Invalid Choice!")