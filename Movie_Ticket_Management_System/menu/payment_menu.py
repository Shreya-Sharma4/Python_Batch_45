from services.payment_services import (
    make_payment,
    view_payments,
    generate_receipt
)


def payment_menu():

    while True:

        print("\n========== PAYMENT MANAGEMENT ==========")
        print("1. Make Payment")
        print("2. View Payment")
        print("3. Generate Receipt")
        print("4. Exit")

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

        # ---------------- VIEW PAYMENT ----------------

        elif choice == "2":

            view_payments()

        # ---------------- GENERATE RECEIPT ----------------

        elif choice == "3":

            generate_receipt()

        # ---------------- EXIT ----------------

        elif choice == "4":

            print(
                "\nThank you for using Payment Management."
            )

            break

        else:

            print(
                "\nInvalid choice. Please select 1, 2, 3, or 4."
            )


if __name__ == "__main__":
    payment_menu()

