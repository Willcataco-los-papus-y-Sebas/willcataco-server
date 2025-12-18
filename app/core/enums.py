from enum import Enum

class PaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"
