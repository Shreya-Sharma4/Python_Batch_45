class Payment:

    def __init__(
        self,
        payment_id=None,
        booking_id=None,
        amount=0.0,
        payment_method="",
        status="Pending",
        payment_date=None
    ):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.payment_date = payment_date

    def display_payment(self):

        print("\n========== PAYMENT DETAILS ==========")
        print(f"Payment ID     : {self.payment_id}")
        print(f"Booking ID     : {self.booking_id}")
        print(f"Amount         : ₹{self.amount}")
        print(f"Payment Method : {self.payment_method}")
        print(f"Status         : {self.status}")
        print(f"Payment Date   : {self.payment_date}")