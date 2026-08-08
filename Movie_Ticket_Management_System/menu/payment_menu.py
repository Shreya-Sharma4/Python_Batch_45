from services.payment_services import make_payment, view_payments


def payment_menu():

    while True:

        print("\n========== PAYMENT MANAGEMENT ==========")
        print("1. Make Payment")
        print("2. View Payment Records")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            try:
                booking_id = int(input("Enter Booking ID: "))
                amount = float(input("Enter Payment Amount: ₹"))

                print("\n---------- PAYMENT METHODS ----------")
                print("1. UPI")
                print("2. Card")
                print("3. Cash")

                payment_choice = input("Select Payment Method: ")

                payment_methods = {
                    "1": "UPI",
                    "2": "Card",
                    "3": "Cash"
                }

                payment_method = payment_methods.get(payment_choice)

                if payment_method is None:
                    print("\nInvalid payment method.")
                    continue

                make_payment(
                    booking_id,
                    amount,
                    payment_method
                )

            except ValueError:
                print("\nPlease enter valid numeric values.")

        elif choice == "2":
            view_payments()

        elif choice == "3":
            print("\nThank you for using Payment Management.")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    payment_menu()