from utils.json_helpers import load_data, save_data
from models.payment import Payment

class PayController:
    path = "database/payment.json"

    def __init__(self, booking):
        self.booking = booking
        self.price = booking.price
        self.payment = None

    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Input Bayar harus lebih dari nol")
        if amount < self.price:
            raise ValueError("Jumlah Bayar kurang dari Harga Bayar")

        cashback = amount - self.price
        self.booking.status = "paid"

        data = load_data(PayController.path)
        Payment.sequence = len(data)

        self.payment = Payment(
            booking_id=self.booking.booking_id,
            username=self.booking.username,
            room_id=self.booking.room_id,
            times_book=self.booking.times,
            console=self.booking.console,
            price=self.price,
            status=self.booking.status
        )

        data.append(self.payment.get_dict())
        save_data(PayController.path, data)

        return f"Transaksi Berhasil\n{cashback} adalah kembalian anda"
