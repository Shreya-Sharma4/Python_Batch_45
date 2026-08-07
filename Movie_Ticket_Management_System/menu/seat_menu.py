from models.seat import Seat
from services.seat_services import SeatService


def seat_menu(connection):

    seat_service = SeatService(connection)

    while True:

        print("\n========== SEAT MANAGEMENT ==========")
        print("1. Add Seat")
        print("2. View Seat Layout")
        print("3. Check Seat Availability")
        print("4. Update Seat Type")
        print("5. Delete Seat")
        print("6. Exit")
        print("=====================================")

        choice = input("Enter your choice: ")

        # 1. Add Seat
        if choice == "1":

            try:

                theater_id = int(
                    input("Enter Theater ID: ")
                )

                seat_number = input(
                    "Enter Seat Number: "
                ).strip().upper()

                print("\nSelect Seat Type:")
                print("1. Normal  - ₹150")
                print("2. Premium - ₹250")
                print("3. Golden  - ₹350")

                type_choice = input(
                    "Enter your choice: "
                )

                if type_choice == "1":
                    seat_type = "Normal"
                    seat_price = 150.00

                elif type_choice == "2":
                    seat_type = "Premium"
                    seat_price = 250.00

                elif type_choice == "3":
                    seat_type = "Golden"
                    seat_price = 350.00

                else:
                    print("Invalid seat type.")
                    continue

                seat = Seat(
                    theater_id=theater_id,
                    seat_number=seat_number,
                    seat_type=seat_type,
                    seat_price=seat_price
                )

                seat_service.add_seat(seat)

            except ValueError:
                print("Please enter valid values.")

        # 2. View Seat Layout
        elif choice == "2":

            try:

                theater_id = int(
                    input("Enter Theater ID: ")
                )

                seat_service.view_seats(
                    theater_id
                )

            except ValueError:
                print("Invalid Theater ID.")

        # 3. Check Seat Availability
        elif choice == "3":

            try:

                theater_id = int(
                    input("Enter Theater ID: ")
                )

                seat_number = input(
                    "Enter Seat Number: "
                ).strip().upper()

                seat_service.check_seat_availability(
                    theater_id,
                    seat_number
                )

            except ValueError:
                print("Invalid input.")

        # 4. Update Seat Type
        elif choice == "4":

            try:

                seat_id = int(
                    input("Enter Seat ID: ")
                )

                print("\nSelect New Seat Type:")
                print("1. Normal  - ₹150")
                print("2. Premium - ₹250")
                print("3. Golden  - ₹350")

                type_choice = input(
                    "Enter your choice: "
                )

                if type_choice == "1":
                    seat_type = "Normal"
                    seat_price = 150.00

                elif type_choice == "2":
                    seat_type = "Premium"
                    seat_price = 250.00

                elif type_choice == "3":
                    seat_type = "Golden"
                    seat_price = 350.00

                else:
                    print("Invalid seat type.")
                    continue

                seat_service.update_seat_type(
                    seat_id,
                    seat_type,
                    seat_price
                )

            except ValueError:
                print("Please enter valid values.")

        # 5. Delete Seat
        elif choice == "5":

            try:

                seat_id = int(
                    input("Enter Seat ID: ")
                )

                confirm = input(
                    "Are you sure you want to delete "
                    "this seat? (y/n): "
                ).lower()

                if confirm == "y":
                    seat_service.delete_seat(
                        seat_id
                    )
                else:
                    print(
                        "Delete operation cancelled."
                    )

            except ValueError:
                print("Invalid Seat ID.")

        # 6. Exit
        elif choice == "6":

            print(
                "Exiting Seat Management..."
            )

            break

        else:

            print(
                "Invalid choice. Please try again."
            )

