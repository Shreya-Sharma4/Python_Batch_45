from services.payment_services import (
    make_payment,
    view_payments
)


def payment_menu():

    while True:

        print("\n========== PAYMENT MANAGEMENT ==========")
        print("1. Make Payment")
        print("2. View Payment Records")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        # ---------------- MAKE PAYMENT ----------------

        if choice == "1":

            try:

                booking_id = int(
                    input("Enter Booking ID: ")
                )

                make_payment(booking_id)

            except ValueError:

                print("\nPlease enter a valid Booking ID.")

        # ---------------- VIEW PAYMENTS ----------------

        elif choice == "2":

            view_payments()

        # ---------------- EXIT ----------------

        elif choice == "3":

            print(
                "\nThank you for using Payment Management."
            )

            break

        else:

            print(
                "\nInvalid choice. Please select 1, 2, or 3."
            )


if __name__ == "__main__":
    payment_menu()