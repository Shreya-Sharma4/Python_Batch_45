class SeatService:

    def __init__(self, connection):

        self.connection = connection


    # ==========================================
    # ADD SEAT
    # ==========================================

    def add_seat(self, seat):

        cursor = self.connection.cursor()

        # Check whether seat already exists
        check_query = """
        SELECT seat_id
        FROM seats
        WHERE theater_id = %s
        AND seat_number = %s
        """

        cursor.execute(
            check_query,
            (
                seat.theater_id,
                seat.seat_number
            )
        )

        existing_seat = cursor.fetchone()

        if existing_seat:

            print(
                "\nSeat "
                + seat.seat_number
                + " already exists."
            )

            cursor.close()

            return


        query = """
        INSERT INTO seats
        (
            theater_id,
            seat_number,
            seat_type,
            seat_price
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            seat.theater_id,
            seat.seat_number,
            seat.seat_type,
            seat.seat_price
        )

        cursor.execute(query, values)

        self.connection.commit()

        cursor.close()

        print("\nSeat added successfully.")


    # ==========================================
    # VIEW SEAT LAYOUT
    # ==========================================

    def view_seats(self, theater_id):

        cursor = self.connection.cursor()

        query = """
        SELECT
            seat_id,
            seat_number,
            seat_type,
            seat_price
        FROM seats
        WHERE theater_id = %s
        ORDER BY CAST(seat_number AS UNSIGNED)
        """

        cursor.execute(
            query,
            (theater_id,)
        )

        seats = cursor.fetchall()

        cursor.close()


        if not seats:

            print(
                "\nNo seats found for Theater ID "
                + str(theater_id)
            )

            return


        print("\n")
        print(
            "                         🎬 SCREEN"
        )

        print("=" * 75)

        print(
            "                         SEAT LAYOUT"
        )

        print("=" * 75)


        # 5 seats in each row
        seats_per_row = 5


        for i in range(
            0,
            len(seats),
            seats_per_row
        ):

            row_seats = seats[
                i:i + seats_per_row
            ]


            # --------------------------
            # Top border
            # --------------------------

            print("     ", end="")

            for seat in row_seats:

                print(
                    "┌──────────┐",
                    end=" "
                )

            print()


            # --------------------------
            # Seat number
            # --------------------------

            print("     ", end="")

            for seat in row_seats:

                seat_number = seat[1]

                print(
                    f"│ {seat_number:^8} │",
                    end=" "
                )

            print()


            # --------------------------
            # Seat type
            # --------------------------

            print("     ", end="")

            for seat in row_seats:

                seat_type = seat[2]

                print(
                    f"│ {seat_type:^8} │",
                    end=" "
                )

            print()


            # --------------------------
            # Seat price
            # --------------------------

            print("     ", end="")

            for seat in row_seats:

                price = seat[3]

                print(
                    f"│ ₹{price:<7.2f} │",
                    end=" "
                )

            print()


            # --------------------------
            # Bottom border
            # --------------------------

            print("     ", end="")

            for seat in row_seats:

                print(
                    "└──────────┘",
                    end=" "
                )

            print()

            print()


        print("=" * 75)

        print(
            "Normal  → ₹150"
        )

        print(
            "Premium → ₹250"
        )

        print(
            "Golden  → ₹350"
        )

        print("=" * 75)


    # ==========================================
    # CHECK SEAT AVAILABILITY
    # ==========================================

    def check_seat_availability(
        self,
        theater_id,
        seat_number
    ):

        cursor = self.connection.cursor()

        query = """
        SELECT
            seat_id,
            seat_type,
            seat_price
        FROM seats
        WHERE theater_id = %s
        AND seat_number = %s
        """

        cursor.execute(
            query,
            (
                theater_id,
                seat_number
            )
        )

        seat = cursor.fetchone()

        cursor.close()


        if seat:

            print("\nSeat found.")

            print(
                "Seat ID    :",
                seat[0]
            )

            print(
                "Seat Type  :",
                seat[1]
            )

            print(
                "Seat Price : ₹",
                seat[2]
            )

        else:

            print(
                "\nSeat "
                + seat_number
                + " not found."
            )


    # ==========================================
    # UPDATE SEAT
    # ==========================================

    def update_seat_type(
        self,
        seat_id,
        seat_type,
        seat_price
    ):

        cursor = self.connection.cursor()

        query = """
        UPDATE seats
        SET
            seat_type = %s,
            seat_price = %s
        WHERE seat_id = %s
        """

        cursor.execute(
            query,
            (
                seat_type,
                seat_price,
                seat_id
            )
        )

        self.connection.commit()


        if cursor.rowcount > 0:

            print(
                "\nSeat updated successfully."
            )

        else:

            print(
                "\nSeat ID not found."
            )


        cursor.close()


    # ==========================================
    # DELETE SEAT
    # ==========================================

    def delete_seat(self, seat_id):

        cursor = self.connection.cursor()

        query = """
        DELETE FROM seats
        WHERE seat_id = %s
        """

        cursor.execute(
            query,
            (seat_id,)
        )

        self.connection.commit()


        if cursor.rowcount > 0:

            print(
                "\nSeat deleted successfully."
            )

        else:

            print(
                "\nSeat ID not found."
            )


        cursor.close()

