class Seat:

    def __init__(
        self,
        seat_id=None,
        theater_id=None,
        seat_number=None,
        seat_type=None,
        seat_price=None
    ):
        self.seat_id = seat_id
        self.theater_id = theater_id
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.seat_price = seat_price

    def __str__(self):
        return (
            f"Seat ID: {self.seat_id}, "
            f"Theater ID: {self.theater_id}, "
            f"Seat: {self.seat_number}, "
            f"Type: {self.seat_type}, "
            f"Price: ₹{self.seat_price}"
        )
