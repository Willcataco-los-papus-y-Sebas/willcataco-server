from enum import Enum

class PaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"

class ActionStatus(str, Enum):
    PAID = "paid"
    PENDING = "pending"
    UNPAID = "unpaid"
