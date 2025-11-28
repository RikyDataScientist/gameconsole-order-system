from utils.json_helpers import load_data, save_data
from models.payment import Payment

class PayController:
    path = "database/payment.json"

    def __init__(self, booking):
        self.booking = booking
        self.price = booking.price

    def pay(self, amount):
        if not amount:
            raise ValueError("Input Bayar tidak boleh Kosong")
        if amount < self.price:
            raise ValueError("Jumlah Bayar kurang dari Harga Bayar")

        cashback = self.price - amount
        self.booking.status = "paid"

        self.payment = Payment(
            booking_id=self.booking.booking_id,
            username=self.booking.username,
            room_id=self.booking.room_id,
            console=self.booking.console,
            price=self.price,
            status=self.booking.status
        )
        return f"Transaksi Berhasil\n{cashback} adalah kembalian anda"

    def save(self):
        data = load_data(PayController.path)
        data.append(self.payment.get_dict())
        save_data(PayController.path, data)