from db import conn, cursor


console = Console()


# =========================================================
# 1. ADD SEATS
# =========================================================

def add_seat():

    try:
        console.print(
            "\n[bold cyan]===== Add Seat =====[/bold cyan]"
        )

        theater_id = int(
            input("Enter Theater ID : ").strip()
        )

        # Check theater exists
        cursor.execute(
            """
            SELECT theater_id, theater_name, location
            FROM theaters
            WHERE theater_id = %s
            """,
            (theater_id,)
        )

        theater = cursor.fetchone()

        if not theater:
            console.print(
                "[red]Theater not found![/red]"
            )
            return

        console.print(
            f"\n[green]Theater : {theater[1]}[/green]"
        )

        console.print(
            f"[green]Location: {theater[2]}[/green]"
        )

        # Seat number
        seat_number = input(
            "Seat Number : "
        ).strip().upper()

        if not seat_number:
            console.print(
                "[red]Seat number cannot be empty![/red]"
            )
            return

        if len(seat_number) > 5:
            console.print(
                "[red]Seat number must not exceed 5 characters![/red]"
            )
            return

        # Seat type
        seat_type = input(
            "Seat Type (Premium/Gold/Silver) : "
        ).strip().title()

        if not seat_type:
            console.print(
                "[red]Seat type cannot be empty![/red]"
            )
            return

        if len(seat_type) > 20:
            console.print(
                "[red]Seat type must not exceed 20 characters![/red]"
            )
            return

        # Seat price
        seat_price = float(
            input("Seat Price : ").strip()
        )

        if seat_price < 0:
            console.print(
                "[red]Seat price cannot be negative![/red]"
            )
            return

        # Check duplicate seat
        cursor.execute(
            """
            SELECT seat_id
            FROM seats
            WHERE theater_id = %s
            AND seat_number = %s
            """,
            (
                theater_id,
                seat_number
            )
        )

        if cursor.fetchone():
            console.print(
                "[red]This seat already exists in this theater![/red]"
            )
            return

        # Insert seat
        cursor.execute(
            """
            INSERT INTO seats
            (
                theater_id,
                seat_number,
                seat_type,
                seat_price
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                theater_id,
                seat_number,
                seat_type,
                seat_price
            )
        )

        conn.commit()

        console.print(
            "\n[green]Seat Added Successfully![/green]"
        )

    except ValueError:

        console.print(
            "[red]Please enter valid values.[/red]"
        )

    except mysql.connector.Error as e:

        console.print(
            f"[red]Database Error: {e}[/red]"
        )

    except Exception as e:

        console.print(
            f"[red]Error: {e}[/red]"
        )


# =========================================================
# 2. VIEW SEAT LAYOUT
# =========================================================

def view_seats():

    try:
        console.print(
            "\n[bold cyan]===== View Seat Layout =====[/bold cyan]"
        )

        show_id = int(
            input("Enter Show ID : ").strip()
        )

        theater_id = int(
            input("Enter Theater ID : ").strip()
        )

        # Check theater
        cursor.execute(
            """
            SELECT theater_id, theater_name, location
            FROM theaters
            WHERE theater_id = %s
            """,
            (theater_id,)
        )

        theater = cursor.fetchone()

        if not theater:
            console.print(
                "[red]Theater not found![/red]"
            )
            return

        console.print(
            f"\n[bold yellow]{theater[1]}[/bold yellow]"
        )

        console.print(
            f"[dim]{theater[2]}[/dim]"
        )

        # Get seats and booking status
        cursor.execute(
            """
            SELECT
                s.seat_id,
                s.seat_number,
                s.seat_type,
                s.seat_price,

                CASE
                    WHEN b.seat_id IS NULL
                    THEN 'Available'
                    ELSE 'Booked'
                END AS status

            FROM seats s

            LEFT JOIN bookings b
                ON s.seat_id = b.seat_id
                AND b.show_id = %s

            WHERE s.theater_id = %s

            ORDER BY s.seat_id
            """,
            (
                show_id,
                theater_id
            )
        )

        seats = cursor.fetchall()

        if not seats:

            console.print(
                "\n[yellow]No seats found for this theater.[/yellow]"
            )

            return

        # =================================================
        # MATRIX DISPLAY
        # =================================================

        console.print(
            "\n[bold white]                 SCREEN[/bold white]"
        )

        console.print(
            "[dim]------------------------------------------------[/dim]"
        )

        console.print(
            "\n[bold cyan]                 SEAT LAYOUT[/bold cyan]\n"
        )

        # 5 seats in each row
        for i in range(0, len(seats), 5):

            row = seats[i:i + 5]

            for seat in row:

                seat_number = seat[1]
                status = seat[4]

                if status == "Available":

                    console.print(
                        f"[black on green]  {seat_number:^5}  [/black on green]",
                        end=" "
                    )

                else:

                    console.print(
                        f"[white on red]  {seat_number:^5}  [/white on red]",
                        end=" "
                    )

            console.print()

        console.print(
            "\n[green]■ Available[/green]    "
            "[red]■ Booked[/red]"
        )

        # =================================================
        # SEAT DETAILS
        # =================================================

        console.print(
            "\n[bold cyan]===== Seat Details =====[/bold cyan]"
        )

        table = Table()

        table.add_column(
            "Seat ID",
            justify="center"
        )

        table.add_column(
            "Seat",
            justify="center"
        )

        table.add_column(
            "Type",
            justify="center"
        )

        table.add_column(
            "Price",
            justify="center"
        )

        table.add_column(
            "Status",
            justify="center"
        )

        for seat in seats:

            if seat[4] == "Available":

                status_text = "[green]Available[/green]"

            else:

                status_text = "[red]Booked[/red]"

            table.add_row(
                str(seat[0]),
                seat[1],
                seat[2],
                f"₹{seat[3]:.2f}",
                status_text
            )

        console.print(table)

    except ValueError:

        console.print(
            "[red]Show ID and Theater ID must be numbers.[/red]"
        )

    except mysql.connector.Error as e:

        console.print(
            f"[red]Database Error: {e}[/red]"
        )

    except Exception as e:

        console.print(
            f"[red]Error: {e}[/red]"
        )


# =========================================================
# 3. CHECK SEAT AVAILABILITY
# =========================================================

def check_seat_availability():

    try:

        console.print(
            "\n[bold cyan]===== Check Seat Availability =====[/bold cyan]"
        )

        show_id = int(
            input("Enter Show ID : ").strip()
        )

        theater_id = int(
            input("Enter Theater ID : ").strip()
        )

        seat_number = input(
            "Enter Seat Number : "
        ).strip().upper()

        # Check seat and booking status
        cursor.execute(
            """
            SELECT
                s.seat_id,
                s.seat_number,
                s.seat_type,
                s.seat_price,

                CASE
                    WHEN b.seat_id IS NULL
                    THEN 'Available'
                    ELSE 'Booked'
                END AS status

            FROM seats s

            LEFT JOIN bookings b
                ON s.seat_id = b.seat_id
                AND b.show_id = %s

            WHERE s.theater_id = %s
            AND s.seat_number = %s
            """,
            (
                show_id,
                theater_id,
                seat_number
            )
        )

        seat = cursor.fetchone()

        if not seat:

            console.print(
                "\n[red]Seat Not Found![/red]"
            )

            return

        console.print(
            "\n[bold cyan]----- Seat Details -----[/bold cyan]"
        )

        console.print(
            f"Seat ID     : {seat[0]}"
        )

        console.print(
            f"Seat Number : {seat[1]}"
        )

        console.print(
            f"Seat Type   : {seat[2]}"
        )

        console.print(
            f"Seat Price  : ₹{seat[3]:.2f}"
        )

        if seat[4] == "Available":

            console.print(
                "Status      : [green]AVAILABLE[/green]"
            )

        else:

            console.print(
                "Status      : [red]BOOKED[/red]"
            )

    except ValueError:

        console.print(
            "[red]Show ID and Theater ID must be numbers.[/red]"
        )

    except mysql.connector.Error as e:

        console.print(
            f"[red]Database Error: {e}[/red]"
        )

    except Exception as e:

        console.print(
            f"[red]Error: {e}[/red]"
        )


# =========================================================
# 4. UPDATE SEAT TYPE
# =========================================================

def update_seat():

    try:

        console.print(
            "\n[bold cyan]===== Update Seat Type =====[/bold cyan]"
        )

        seat_id = int(
            input("Seat ID : ").strip()
        )

        # Find seat
        cursor.execute(
            """
            SELECT
                seat_id,
                theater_id,
                seat_number,
                seat_type,
                seat_price
            FROM seats
            WHERE seat_id = %s
            """,
            (seat_id,)
        )

        seat = cursor.fetchone()

        if not seat:

            console.print(
                "[red]Seat Not Found![/red]"
            )

            return

        console.print(
            "\n[bold yellow]Current Seat Details[/bold yellow]"
        )

        console.print(
            f"Seat ID     : {seat[0]}"
        )

        console.print(
            f"Theater ID  : {seat[1]}"
        )

        console.print(
            f"Seat Number : {seat[2]}"
        )

        console.print(
            f"Seat Type   : {seat[3]}"
        )

        console.print(
            f"Seat Price  : ₹{seat[4]:.2f}"
        )

        # New seat type
        new_seat_type = input(
            "\nNew Seat Type : "
        ).strip().title()

        if not new_seat_type:

            console.print(
                "[red]Seat type cannot be empty![/red]"
            )

            return

        if len(new_seat_type) > 20:

            console.print(
                "[red]Seat type must not exceed 20 characters![/red]"
            )

            return

        # Update ONLY seat type
        cursor.execute(
            """
            UPDATE seats
            SET seat_type = %s
            WHERE seat_id = %s
            """,
            (
                new_seat_type,
                seat_id
            )
        )

        conn.commit()

        console.print(
            "\n[green]Seat Type Updated Successfully![/green]"
        )

    except ValueError:

        console.print(
            "[red]Seat ID must be a number.[/red]"
        )

    except mysql.connector.Error as e:

        console.print(
            f"[red]Database Error: {e}[/red]"
        )

    except Exception as e:

        console.print(
            f"[red]Error: {e}[/red]"
        )


# =========================================================
# 5. DELETE SEAT
# =========================================================

def delete_seat():

    try:

        console.print(
            "\n[bold cyan]===== Delete Seat =====[/bold cyan]"
        )

        seat_id = int(
            input("Seat ID : ").strip()
        )

        # Find seat
        cursor.execute(
            """
            SELECT
                seat_id,
                theater_id,
                seat_number,
                seat_type,
                seat_price
            FROM seats
            WHERE seat_id = %s
            """,
            (seat_id,)
        )

        seat = cursor.fetchone()

        if not seat:

            console.print(
                "[red]Seat Not Found![/red]"
            )

            return

        console.print(
            "\n[bold yellow]Seat Details[/bold yellow]"
        )

        console.print(
            f"Seat ID     : {seat[0]}"
        )

        console.print(
            f"Theater ID  : {seat[1]}"
        )

        console.print(
            f"Seat Number : {seat[2]}"
        )

        console.print(
            f"Seat Type   : {seat[3]}"
        )

        console.print(
            f"Seat Price  : ₹{seat[4]:.2f}"
        )

        confirm = input(
            "\nDelete this seat? (yes/no): "
        ).strip().lower()

        if confirm != "yes":

            console.print(
                "[yellow]Delete Cancelled.[/yellow]"
            )

            return

        cursor.execute(
            """
            DELETE FROM seats
            WHERE seat_id = %s
            """,
            (seat_id,)
        )

        conn.commit()

        console.print(
            "\n[green]Seat Deleted Successfully![/green]"
        )

    except ValueError:

        console.print(
            "[red]Seat ID must be a number.[/red]"
        )

    except mysql.connector.Error as e:

        console.print(
            f"[red]Database Error: {e}[/red]"
        )

    except Exception as e:

        console.print(
            f"[red]Error: {e}[/red]"
        )
